from multirunnable import RunningMode, SimpleExecutor
from multirunnable.parallel.strategy import ProcessStrategy
from multirunnable.concurrent.strategy import ThreadStrategy
from multirunnable.coroutine.strategy import GreenThreadStrategy, AsynchronousStrategy

from .test_config import Worker_Size, Running_Diff_Time, Test_Function_Sleep_Time

from abc import ABCMeta, abstractmethod
from typing import List
import threading
import pytest
import time
import os


_Worker_Size = Worker_Size

_Running_Diff_Time: int = Running_Diff_Time

_Test_Function_Sleep_Time = Test_Function_Sleep_Time

Running_Parent_PID = None
Running_Count = 0
Running_Thread_IDs: List = []
Running_PPIDs: List = []
Running_Current_Threads: List = []
Running_Finish_Timestamp: List = []

_Thread_Lock = threading.Lock()
_Thread_RLock = threading.RLock()


def reset_running_flag() -> None:
    global Running_Count
    Running_Count = 0


def reset_running_timer() -> None:
    global Running_Thread_IDs, Running_PPIDs, Running_Current_Threads, Running_Finish_Timestamp
    Running_Thread_IDs[:] = []
    Running_PPIDs[:] = []
    Running_Current_Threads[:] = []
    Running_Finish_Timestamp[:] = []


@pytest.fixture(scope="function")
def executor_as_process():
    return SimpleExecutor(mode=RunningMode.Parallel, executors=_Worker_Size)


@pytest.fixture(scope="function")
def executor_as_thread():
    return SimpleExecutor(mode=RunningMode.Concurrent, executors=_Worker_Size)


@pytest.fixture(scope="function")
def executor_as_green_thread():
    return SimpleExecutor(mode=RunningMode.GreenThread, executors=_Worker_Size)


@pytest.fixture(scope="function")
def executor_as_asynchronous():
    return SimpleExecutor(mode=RunningMode.Asynchronous, executors=_Worker_Size)



class TestSimpleExecutor:

    """
    Description:
        Testing executor which may be as Process, Thread, Green Thread or Asynchronous object.
        The responsibility of this object is calling the mapping method(s) by the RunningMode.
        For example, it will use 'multiprocessing.Process.start' when you call 'run' with RunningMode.Parallel.

        For the testing concern, we should pay the attention to the feature of responsibility which means
        it should target at the feature about 'Procedure' and 'Adapter of features', doesn't working process.
    """

    def test_initial_running_strategy_with_parallel(self, executor_as_process: SimpleExecutor):
        executor_as_process._initial_running_strategy()

        from multirunnable.executor import General_Runnable_Strategy
        assert General_Runnable_Strategy is not None, f"It should be assign running-strategy instance."
        assert isinstance(General_Runnable_Strategy, ProcessStrategy), f"It should be an sub-instance of 'ProcessStrategy'."


    def test_initial_running_strategy_with_concurrent(self, executor_as_thread: SimpleExecutor):
        executor_as_thread._initial_running_strategy()

        from multirunnable.executor import General_Runnable_Strategy
        assert General_Runnable_Strategy is not None, f"It should be assign running-strategy instance."
        assert isinstance(General_Runnable_Strategy, ThreadStrategy), f"It should be an sub-instance of 'ThreadStrategy'."


    def test_initial_running_strategy_with_coroutine(self, executor_as_green_thread: SimpleExecutor):
        executor_as_green_thread._initial_running_strategy()

        from multirunnable.executor import General_Runnable_Strategy
        assert General_Runnable_Strategy is not None, f"It should be assign running-strategy instance."
        assert isinstance(General_Runnable_Strategy, GreenThreadStrategy), f"It should be an sub-instance of 'GreenThreadStrategy'."


    def test_initial_running_strategy_with_asynchronous(self, executor_as_asynchronous: SimpleExecutor):
        executor_as_asynchronous._initial_running_strategy()

        from multirunnable.executor import General_Runnable_Strategy
        assert General_Runnable_Strategy is not None, f"It should be assign running-strategy instance."
        assert isinstance(General_Runnable_Strategy, AsynchronousStrategy), f"It should be an sub-instance of 'AsynchronousStrategy'."


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_start_new_worker(self, executor_as_thread: SimpleExecutor):

        def _target():
            pass

        executor_as_process.start_new_worker()


    def test_run(self, executor_as_thread: SimpleExecutor):

        TestSimpleExecutor._initial()

        def _target(*args, **kwargs):
            global Running_Count, Running_Thread_IDs, Running_PPIDs, Running_Current_Threads, Running_Finish_Timestamp

            with _Thread_Lock:
                Running_Count += 1

                _pid = os.getpid()
                _ppid = os.getppid()
                _ident = threading.get_ident()
                # _time = str(datetime.datetime.now())
                _time = int(time.time())

                Running_Thread_IDs.append(_ident)
                Running_PPIDs.append(_ppid)
                Running_Current_Threads.append(str(threading.current_thread()))
                Running_Finish_Timestamp.append(_time)

            time.sleep(Test_Function_Sleep_Time)
            return f"result_{threading.current_thread()}"

        executor_as_thread.run(function=_target)
        # Do some checking
        # 1. The amount of workers should be the same with the value of option *executors*.
        # 3. The amount of thread IDs should be the same with the value of option *executors*.
        # 2. The done-timestamp should be very close.
        TestSimpleExecutor._chk_run_record()


    def test_map(self, executor_as_thread: SimpleExecutor):

        TestSimpleExecutor._initial()
        # _args = ("index_1", "index_2", "index_3", "index_4", "index_5")    # Bug 1.
        _args = [("index_1",),  ("index_2",), ("index_3",), ("index_4",), ("index_5",)]

        def _target(*args, **kwargs):
            global Running_Count, Running_Thread_IDs, Running_PPIDs, Running_Current_Threads, Running_Finish_Timestamp

            with _Thread_Lock:
                Running_Count += 1

                if args:
                    if len(args) == 1:
                        assert {args} <= set(_args), f"The argument *args* should be one of element of the input outside."
                    else:
                        assert set(args) <= set(_args), f"The argument *args* should be one of element of the input outside."
                    if len(args) > 1:
                        assert args == _args, f"The argument *args* should be same as the global variable 'Test_Function_Args'."
                if kwargs:
                    assert kwargs is None or kwargs == {}, f"The argument *kwargs* should be empty or None value."

                _pid = os.getpid()
                _ppid = os.getppid()
                _ident = threading.get_ident()
                # _time = str(datetime.datetime.now())
                _time = int(time.time())

                Running_Thread_IDs.append(_ident)
                Running_PPIDs.append(_ppid)
                Running_Current_Threads.append(str(threading.current_thread()))
                Running_Finish_Timestamp.append(_time)

            time.sleep(Test_Function_Sleep_Time)
            return f"result_{threading.current_thread()}"

        executor_as_thread.map(function=_target, args_iter=_args)
        # Do some checking
        # 1. The amount of workers should be the same with the amount of parameters.
        # 3. The amount of thread IDs should be the same with the amount of parameters.
        # 2. The done-timestamp should be very close.
        TestSimpleExecutor._chk_map_record(len(_args))


    def test_map_with_function(self, executor_as_thread: SimpleExecutor):

        TestSimpleExecutor._initial()

        _function_a_flag = 0
        _function_b_flag = 0
        _thread_ids = []
        _threads = []
        _done_timestamp = []

        def _target_a():
            # with _Thread_RLock:
            nonlocal _function_a_flag
            _function_a_flag += 1
            _thread_ids.append(threading.get_ident())
            _threads.append(threading.current_thread())
            _done_timestamp.append(int(time.time()))
            time.sleep(Test_Function_Sleep_Time)

        def _target_b():
            # with _Thread_RLock:
            nonlocal _function_b_flag
            _function_b_flag += 1
            _thread_ids.append(threading.get_ident())
            _threads.append(threading.current_thread())
            _done_timestamp.append(int(time.time()))
            time.sleep(Test_Function_Sleep_Time)

        _functions = [_target_a, _target_b]
        executor_as_thread.map_with_function(functions=_functions)
        # Do some checking
        # 1. The amount of workers should be the same with the amount of functions.
        # 3. The amount of thread IDs should be the same with the amount of functions.
        # 2. The done-timestamp should be very close.
        TestSimpleExecutor._chk_map_with_function(_functions, _function_a_flag, _function_b_flag, _thread_ids, _threads, _done_timestamp)


    def test_terminal(self, executor_as_thread: SimpleExecutor):
        try:
            executor_as_thread.terminal()
        except Exception as e:
            assert False, f"It should work finely without any issue. Please check it."
        else:
            assert True, f"It work finely without any issue."


    def test_kill(self, executor_as_thread: SimpleExecutor):
        try:
            executor_as_thread.kill()
        except Exception as e:
            assert False, f"It should work finely without any issue. Please check it."
        else:
            assert True, f"It work finely without any issue."


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_result(self, executor_as_thread: SimpleExecutor):
        executor_as_thread.result()


    @staticmethod
    def _initial():
        # Test for parameters with '**kwargs'
        reset_running_flag()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_run_record():
        assert Running_Count == _Worker_Size, f"The running count should be the same as the process pool size."

        _ppid_list = Running_PPIDs[:]
        _thread_id_list = Running_Thread_IDs[:]
        _current_thread_list = Running_Current_Threads[:]
        _timestamp_list = Running_Finish_Timestamp[:]

        # assert len(set(_ppid_list)) == 1, f"The PPID of each process should be the same."
        # assert _ppid_list[0] == Running_Parent_PID, f"The PPID should equal to {Running_Parent_PID}. But it got {_ppid_list[0]}."
        assert len(_thread_id_list) == _Worker_Size, f"The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_thread_id_list)) == _Worker_Size, f"The count of PID (de-duplicate) should be the same as the count of processes."
        assert len(_thread_id_list) == len(_current_thread_list), f"The count of current process name (no de-duplicate) should be equal to count of PIDs."
        assert len(set(_thread_id_list)) == len(set(_current_thread_list)), f"The count of current process name (de-duplicate) should be equal to count of PIDs."

        _max_timestamp = max(_timestamp_list)
        _min_timestamp = min(_timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, f"Processes should be run in the same time period."


    @staticmethod
    def _chk_map_record(_argument_size):
        assert Running_Count == _argument_size, f"The running count should be the same as the process pool size."

        _ppid_list = Running_PPIDs[:]
        _thread_id_list = Running_Thread_IDs[:]
        _current_thread_list = Running_Current_Threads[:]
        _timestamp_list = Running_Finish_Timestamp[:]

        # assert len(set(_ppid_list)) == 1, f"The PPID of each process should be the same."
        # assert _ppid_list[0] == Running_Parent_PID, f"The PPID should equal to {Running_Parent_PID}. But it got {_ppid_list[0]}."
        assert len(_thread_id_list) == _argument_size, f"The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_thread_id_list)) == _argument_size, f"The count of PID (de-duplicate) should be the same as the count of processes."
        assert len(_thread_id_list) == len(_current_thread_list), f"The count of current process name (no de-duplicate) should be equal to count of PIDs."
        assert len(set(_thread_id_list)) == len(set(_current_thread_list)), f"The count of current process name (de-duplicate) should be equal to count of PIDs."

        _max_timestamp = max(_timestamp_list)
        _min_timestamp = min(_timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, f"Processes should be run in the same time period."


    @staticmethod
    def _chk_map_with_function(_functions, _function_a_flag, _function_b_flag, _thread_ids, _threads, _done_timestamp):
        assert _function_a_flag == 1, f"The running count should be the same as the amount of function '_target_a'."
        assert _function_b_flag == 1, f"The running count should be the same as the amount of function '_target_b'."

        _thread_id_list = _thread_ids[:]
        _current_thread_list = _threads[:]
        _timestamp_list = _done_timestamp[:]

        _function_amount = len(_functions)

        assert len(_thread_id_list) == _function_amount, f"The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_thread_id_list)) == _function_amount, f"The count of PID (de-duplicate) should be the same as the count of processes."
        assert len(_thread_id_list) == len(_current_thread_list), f"The count of current process name (no de-duplicate) should be equal to count of PIDs."
        assert len(set(_thread_id_list)) == len(set(_current_thread_list)), f"The count of current process name (de-duplicate) should be equal to count of PIDs."

        _max_timestamp = max(_timestamp_list)
        _min_timestamp = min(_timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, f"Processes should be run in the same time period."

