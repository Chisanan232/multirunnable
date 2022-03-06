import random

from multirunnable import get_current_mode, RunningMode, SimpleExecutor, PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from multirunnable.executor import AdapterExecutor
from multirunnable.parallel.strategy import ProcessStrategy
from multirunnable.parallel.share import Global_Manager
from multirunnable.concurrent.strategy import ThreadStrategy
from multirunnable.coroutine.strategy import GreenThreadStrategy, AsynchronousStrategy

from .test_config import Worker_Size, Running_Diff_Time, Test_Function_Sleep_Time

from typing import List, Any
import multiprocessing as mp
import threading
import asyncio
import gevent.lock
import pytest
import time
import os


_Worker_Size = Worker_Size

_Running_Diff_Time: int = Running_Diff_Time

_Test_Function_Sleep_Time = Test_Function_Sleep_Time

Running_Count = Global_Manager.Value(int, 0)
Running_Worker_IDs: List = Global_Manager.list()
Running_PPIDs: List = Global_Manager.list()
Running_Current_Workers: List = Global_Manager.list()
Running_Finish_Timestamp: List = Global_Manager.list()

_Worker_Lock = None
_Worker_RLock = None


def reset_running_flag() -> None:
    global Running_Count
    Running_Count.value = 0


def reset_running_timer() -> None:
    global Running_Worker_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp
    Running_Worker_IDs[:] = []
    Running_PPIDs[:] = []
    Running_Current_Workers[:] = []
    Running_Finish_Timestamp[:] = []


def initial_lock() -> None:
    global _Worker_Lock

    _rmode = get_current_mode(force=True)

    if _rmode is RunningMode.Parallel:
        _Worker_Lock = mp.Lock()
    elif _rmode is RunningMode.Concurrent:
        _Worker_Lock = threading.Lock()
    elif _rmode is RunningMode.GreenThread:
        _Worker_Lock = gevent.lock.RLock()
    elif _rmode is RunningMode.Asynchronous:
        _Worker_Lock = asyncio.Lock()
    else:
        raise ValueError("The RunningMode has the unexpected mode.")


def initial_rlock() -> None:
    global _Worker_RLock

    _rmode = get_current_mode(force=True)

    if _rmode is RunningMode.Parallel:
        _Worker_RLock = mp.RLock()
    elif _rmode is RunningMode.Concurrent:
        _Worker_RLock = threading.RLock()
    elif _rmode is RunningMode.GreenThread:
        _Worker_RLock = gevent.lock.RLock()
    else:
        raise ValueError("The RunningMode has the unexpected mode.")


def _get_current_worker() -> Any:
    _rmode = get_current_mode(force=True)

    if _rmode is RunningMode.Parallel:
        _current_worker = mp.current_process()
    elif _rmode is RunningMode.Concurrent:
        _current_worker = threading.current_thread()
    elif _rmode is RunningMode.GreenThread:
        _current_worker = gevent.getcurrent()
    elif _rmode is RunningMode.Asynchronous:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            _current_worker = asyncio.current_task()
        else:
            _current_worker = asyncio.Task.current_task()
    else:
        raise ValueError("The RunningMode has the unexpected mode.")

    return _current_worker


def _get_worker_id() -> str:
    _rmode = get_current_mode(force=True)

    if _rmode is RunningMode.Parallel:
        _worker_id = mp.current_process().ident
    elif _rmode is RunningMode.Concurrent:
        _worker_id = threading.current_thread().ident
    elif _rmode is RunningMode.GreenThread:
        _worker_id = id(gevent.getcurrent())
    elif _rmode is RunningMode.Asynchronous:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            _worker_id = id(asyncio.current_task())
        else:
            _worker_id = id(asyncio.Task.current_task())
    else:
        raise ValueError("The RunningMode has the unexpected mode.")

    return str(_worker_id)


def _sleep_time() -> None:
    _rmode = get_current_mode(force=True)

    if _rmode is RunningMode.Parallel or _rmode is RunningMode.Concurrent:
        time.sleep(Test_Function_Sleep_Time)
    elif _rmode is RunningMode.GreenThread:
        gevent.sleep(Test_Function_Sleep_Time)
    elif _rmode is RunningMode.Asynchronous:
        asyncio.sleep(Test_Function_Sleep_Time)
    else:
        raise ValueError("The RunningMode has the unexpected mode.")


@pytest.fixture(scope="function")
def instantiate_executor(request) -> SimpleExecutor:
    _executor = SimpleExecutor(mode=request.param, executors=_Worker_Size)
    initial_lock()
    return _executor


@pytest.fixture(scope="function")
def instantiate_adapter_executor() -> AdapterExecutor:
    _executor = AdapterExecutor(strategy=ThreadStrategy(executors=_Worker_Size))
    return _executor



class TestSimpleExecutor:

    """
    Description:
        Testing executor which may be as Process, Thread, Green Thread or Asynchronous object.
        The responsibility of this object is calling the mapping method(s) by the RunningMode.
        For example, it will use 'multiprocessing.Process.start' when you call 'run' with RunningMode.Parallel.

        For the testing concern, we should pay the attention to the feature of responsibility which means
        it should target at the feature about 'Procedure' and 'Adapter of features', doesn't working process.
    """

    @pytest.mark.parametrize(
        argnames="instantiate_executor",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous],
        indirect=True
    )
    def test_initial_running_strategy(self, instantiate_executor: SimpleExecutor):
        instantiate_executor._initial_running_strategy()

        from multirunnable.executor import General_Runnable_Strategy
        assert General_Runnable_Strategy is not None, "It should be assign running-strategy instance."
        _rmode = get_current_mode(force=True)
        if _rmode is RunningMode.Parallel:
            assert isinstance(General_Runnable_Strategy, ProcessStrategy), "It should be an sub-instance of 'ProcessStrategy'."
        elif _rmode is RunningMode.Concurrent:
            assert isinstance(General_Runnable_Strategy, ThreadStrategy), "It should be an sub-instance of 'ThreadStrategy'."
        elif _rmode is RunningMode.Parallel.GreenThread:
            assert isinstance(General_Runnable_Strategy, GreenThreadStrategy), "It should be an sub-instance of 'GreenThreadStrategy'."
        elif _rmode is RunningMode.Asynchronous:
            assert isinstance(General_Runnable_Strategy, AsynchronousStrategy), "It should be an sub-instance of 'AsynchronousStrategy'."
        else:
            raise ValueError("The RunningMode has the unexpected mode.")


    @pytest.mark.parametrize(
        argnames="instantiate_executor",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_start_new_worker(self, instantiate_executor: SimpleExecutor):

        TestSimpleExecutor._initial()
        initial_lock()

        def _target():
            global Running_Count, Running_Worker_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp

            with _Worker_Lock:
                Running_Count.value += 1

                _ppid = os.getppid()
                _ident = _get_worker_id()
                _current_worker = _get_current_worker()
                # _time = str(datetime.datetime.now())
                _time = int(time.time())

                Running_Worker_IDs.append(_ident)
                Running_PPIDs.append(_ppid)
                Running_Current_Workers.append(str(_current_worker))
                Running_Finish_Timestamp.append(_time)

            _sleep_time()
            return f"result_{_current_worker}"

        _workers = [instantiate_executor.start_new_worker(target=_target) for _ in range(_Worker_Size)]
        instantiate_executor.close(workers=_workers)
        _results = instantiate_executor.result()
        assert len(_results) == _Worker_Size, ""
        # Do some checking
        # 1. The amount of workers should be the same with the value of option *executors*.
        # 3. The amount of thread IDs should be the same with the value of option *executors*.
        # 2. The done-timestamp should be very close.
        TestSimpleExecutor._chk_run_record()


    @pytest.mark.parametrize(
        argnames="instantiate_executor",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_run(self, instantiate_executor: SimpleExecutor):

        TestSimpleExecutor._initial()
        initial_lock()

        def _target(*args, **kwargs):
            global Running_Count, Running_Worker_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp

            with _Worker_Lock:
                Running_Count.value += 1

                _ppid = os.getppid()
                _ident = _get_worker_id()
                _current_worker = _get_current_worker()
                # _time = str(datetime.datetime.now())
                _time = int(time.time())

                Running_Worker_IDs.append(_ident)
                Running_PPIDs.append(_ppid)
                Running_Current_Workers.append(str(_current_worker))
                Running_Finish_Timestamp.append(_time)

            _sleep_time()
            return f"result_{_current_worker}"

        instantiate_executor.run(function=_target)
        _results = instantiate_executor.result()
        assert len(_results) == _Worker_Size, ""
        # Do some checking
        # 1. The amount of workers should be the same with the value of option *executors*.
        # 3. The amount of thread IDs should be the same with the value of option *executors*.
        # 2. The done-timestamp should be very close.
        TestSimpleExecutor._chk_run_record()


    @pytest.mark.parametrize(
        argnames="instantiate_executor",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map(self, instantiate_executor: SimpleExecutor):

        TestSimpleExecutor._initial()
        initial_lock()

        # _args = ("index_1", "index_2", "index_3", "index_4", "index_5")    # Bug 1.
        _args = [("index_1",),  ("index_2",), ("index_3",), ("index_4",), ("index_5",)]

        def _target(*args, **kwargs):
            global Running_Count, Running_Worker_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp

            with _Worker_Lock:
                Running_Count.value += 1

                if args:
                    if len(args) == 1:
                        assert {args} <= set(_args), "The argument *args* should be one of element of the input outside."
                    else:
                        assert set(args) <= set(_args), "The argument *args* should be one of element of the input outside."
                    if len(args) > 1:
                        assert args == _args, "The argument *args* should be same as the global variable 'Test_Function_Args'."
                if kwargs:
                    assert kwargs is None or kwargs == {}, "The argument *kwargs* should be empty or None value."

                _ppid = os.getppid()
                _ident = _get_worker_id()
                _current_worker = _get_current_worker()
                # _time = str(datetime.datetime.now())
                _time = int(time.time())

                Running_Worker_IDs.append(_ident)
                Running_PPIDs.append(_ppid)
                Running_Current_Workers.append(str(_current_worker))
                Running_Finish_Timestamp.append(_time)

            _sleep_time()
            return f"result_{_current_worker}"

        instantiate_executor.map(function=_target, args_iter=_args)
        _results = instantiate_executor.result()
        assert len(_results) == len(_args), ""
        # Do some checking
        # 1. The amount of workers should be the same with the amount of parameters.
        # 3. The amount of thread IDs should be the same with the amount of parameters.
        # 2. The done-timestamp should be very close.
        TestSimpleExecutor._chk_map_record(len(_args))


    @pytest.mark.parametrize(
        argnames="instantiate_executor",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map_with_function(self, instantiate_executor: SimpleExecutor):

        TestSimpleExecutor._initial()
        initial_rlock()

        _function_a_flag = Global_Manager.Value(int, 0)
        _function_b_flag = Global_Manager.Value(int, 0)

        def _target_a(*args):
            global Running_Worker_IDs, Running_Current_Workers, Running_Finish_Timestamp
            nonlocal _function_a_flag

            _function_a_flag.value += 1
            _ident = _get_worker_id()
            _current_worker = _get_current_worker()

            Running_Worker_IDs.append(_ident)
            Running_Current_Workers.append(str(_current_worker))
            Running_Finish_Timestamp.append(int(time.time()))

            _sleep_time()

        def _target_b(*args):
            global Running_Worker_IDs, Running_Current_Workers, Running_Finish_Timestamp
            nonlocal _function_b_flag

            _function_b_flag.value += 1
            _ident = _get_worker_id()
            _current_worker = _get_current_worker()

            Running_Worker_IDs.append(_ident)
            Running_Current_Workers.append(str(_current_worker))
            Running_Finish_Timestamp.append(int(time.time()))

            _sleep_time()

        _functions = [_target_a, _target_b]
        instantiate_executor.map_with_function(functions=_functions)
        _results = instantiate_executor.result()
        assert len(_results) == len(_functions), ""
        # Do some checking
        # 1. The amount of workers should be the same with the amount of functions.
        # 3. The amount of thread IDs should be the same with the amount of functions.
        # 2. The done-timestamp should be very close.
        # TestSimpleExecutor._chk_map_with_function(_functions, _function_a_flag, _function_b_flag, _worker_ids, _workers, _done_timestamp)
        global Running_Worker_IDs, Running_Current_Workers, Running_Finish_Timestamp
        TestSimpleExecutor._chk_map_with_function(_functions, _function_a_flag, _function_b_flag, Running_Worker_IDs, Running_Current_Workers, Running_Finish_Timestamp)


    @pytest.mark.parametrize(
        argnames="instantiate_executor",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_result(self, instantiate_executor: SimpleExecutor):

        def _target(*args, **kwargs):
            _current_worker = _get_current_worker()
            return f"result_{_current_worker}"

        instantiate_executor.run(function=_target)
        _results = instantiate_executor.result()
        assert len(_results) == _Worker_Size, ""
        for _r in _results:
            assert "result_" in _r.data, ""
            assert _r.worker_name, ""
            assert _r.worker_ident, ""
            assert _r.state, ""
            assert _r.pid, ""
            assert _r.exception is None, ""


    @staticmethod
    def _initial():
        # Test for parameters with '**kwargs'
        reset_running_flag()
        reset_running_timer()


    @staticmethod
    def _chk_run_record():
        assert Running_Count.value == _Worker_Size, "The running count should be the same as the process pool size."

        _ppid_list = Running_PPIDs[:]
        _thread_id_list = Running_Worker_IDs[:]
        _current_thread_list = Running_Current_Workers[:]
        _timestamp_list = Running_Finish_Timestamp[:]

        # assert len(set(_ppid_list)) == 1, "The PPID of each process should be the same."
        assert len(_thread_id_list) == _Worker_Size, "The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_thread_id_list)) == _Worker_Size, "The count of PID (de-duplicate) should be the same as the count of processes."
        assert len(_thread_id_list) == len(_current_thread_list), "The count of current process name (no de-duplicate) should be equal to count of PIDs."
        assert len(set(_thread_id_list)) == len(set(_current_thread_list)), "The count of current process name (de-duplicate) should be equal to count of PIDs."

        _max_timestamp = max(_timestamp_list)
        _min_timestamp = min(_timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, "Processes should be run in the same time period."


    @staticmethod
    def _chk_map_record(_argument_size):
        assert Running_Count.value == _argument_size, "The running count should be the same as the process pool size."

        _ppid_list = Running_PPIDs[:]
        _thread_id_list = Running_Worker_IDs[:]
        _current_thread_list = Running_Current_Workers[:]
        _timestamp_list = Running_Finish_Timestamp[:]

        # assert len(set(_ppid_list)) == 1, "The PPID of each process should be the same."
        assert len(_thread_id_list) == _argument_size, "The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_thread_id_list)) == _argument_size, "The count of PID (de-duplicate) should be the same as the count of processes."
        assert len(_thread_id_list) == len(_current_thread_list), "The count of current process name (no de-duplicate) should be equal to count of PIDs."
        assert len(set(_thread_id_list)) == len(set(_current_thread_list)), "The count of current process name (de-duplicate) should be equal to count of PIDs."

        _max_timestamp = max(_timestamp_list)
        _min_timestamp = min(_timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, "Processes should be run in the same time period."


    @staticmethod
    def _chk_map_with_function(_functions, _function_a_flag, _function_b_flag, _thread_ids, _threads, _done_timestamp):
        assert _function_a_flag.value == 1, "The running count should be the same as the amount of function '_target_a'."
        assert _function_b_flag.value == 1, "The running count should be the same as the amount of function '_target_b'."

        _thread_id_list = _thread_ids[:]
        _current_thread_list = _threads[:]
        _timestamp_list = _done_timestamp[:]

        _function_amount = len(_functions)

        assert len(_thread_id_list) == _function_amount, "The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_thread_id_list)) == _function_amount, "The count of PID (de-duplicate) should be the same as the count of processes."
        assert len(_thread_id_list) == len(_current_thread_list), "The count of current process name (no de-duplicate) should be equal to count of PIDs."
        assert len(set(_thread_id_list)) == len(set(_current_thread_list)), "The count of current process name (de-duplicate) should be equal to count of PIDs."

        _max_timestamp = max(_timestamp_list)
        _min_timestamp = min(_timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, "Processes should be run in the same time period."



class TestAdapterExecutor:

    def test_start_new_worker(self, instantiate_adapter_executor: SimpleExecutor):

        TestSimpleExecutor._initial()
        _lock = threading.Lock()

        def _target():
            global Running_Count, Running_Worker_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp

            with _lock:
                Running_Count.value += 1

                _ppid = os.getppid()
                _ident = threading.current_thread().ident
                _current_worker = threading.current_thread()
                # _time = str(datetime.datetime.now())
                _time = int(time.time())

                Running_Worker_IDs.append(_ident)
                Running_PPIDs.append(_ppid)
                Running_Current_Workers.append(str(_current_worker))
                Running_Finish_Timestamp.append(_time)

            time.sleep(_Test_Function_Sleep_Time)
            return f"result_{_current_worker}"

        _workers = [instantiate_adapter_executor.start_new_worker(target=_target) for _ in range(_Worker_Size)]
        instantiate_adapter_executor.close(workers=_workers)
        _results = instantiate_adapter_executor.result()
        assert len(_results) == _Worker_Size, ""
        # Do some checking
        # 1. The amount of workers should be the same with the value of option *executors*.
        # 3. The amount of thread IDs should be the same with the value of option *executors*.
        # 2. The done-timestamp should be very close.
        TestSimpleExecutor._chk_run_record()


    def test_run(self, instantiate_adapter_executor: SimpleExecutor):

        TestSimpleExecutor._initial()
        _lock = threading.Lock()

        def _target(*args, **kwargs):
            global Running_Count, Running_Worker_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp

            with _lock:
                Running_Count.value += 1

                _ppid = os.getppid()
                _ident = threading.current_thread().ident
                _current_worker = threading.current_thread()
                # _time = str(datetime.datetime.now())
                _time = int(time.time())

                Running_Worker_IDs.append(_ident)
                Running_PPIDs.append(_ppid)
                Running_Current_Workers.append(str(_current_worker))
                Running_Finish_Timestamp.append(_time)

            time.sleep(_Test_Function_Sleep_Time)
            return f"result_{_current_worker}"

        instantiate_adapter_executor.run(function=_target)
        _results = instantiate_adapter_executor.result()
        assert len(_results) == _Worker_Size, ""
        # Do some checking
        # 1. The amount of workers should be the same with the value of option *executors*.
        # 3. The amount of thread IDs should be the same with the value of option *executors*.
        # 2. The done-timestamp should be very close.
        TestSimpleExecutor._chk_run_record()


    def test_map(self, instantiate_adapter_executor: SimpleExecutor):

        TestSimpleExecutor._initial()
        _lock = threading.Lock()

        # _args = ("index_1", "index_2", "index_3", "index_4", "index_5")    # Bug 1.
        _args = [("index_1",),  ("index_2",), ("index_3",), ("index_4",), ("index_5",)]

        def _target(*args, **kwargs):
            global Running_Count, Running_Worker_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp

            with _lock:
                Running_Count.value += 1

                if args:
                    if len(args) == 1:
                        assert {args} <= set(_args), "The argument *args* should be one of element of the input outside."
                    else:
                        assert set(args) <= set(_args), "The argument *args* should be one of element of the input outside."
                    if len(args) > 1:
                        assert args == _args, "The argument *args* should be same as the global variable 'Test_Function_Args'."
                if kwargs:
                    assert kwargs is None or kwargs == {}, "The argument *kwargs* should be empty or None value."

                _ppid = os.getppid()
                _ident = threading.current_thread().ident
                _current_worker = threading.current_thread()
                # _time = str(datetime.datetime.now())
                _time = int(time.time())

                Running_Worker_IDs.append(_ident)
                Running_PPIDs.append(_ppid)
                Running_Current_Workers.append(str(_current_worker))
                Running_Finish_Timestamp.append(_time)

            time.sleep(_Test_Function_Sleep_Time)
            return f"result_{_current_worker}"

        instantiate_adapter_executor.map(function=_target, args_iter=_args)
        _results = instantiate_adapter_executor.result()
        assert len(_results) == len(_args), ""
        # Do some checking
        # 1. The amount of workers should be the same with the amount of parameters.
        # 3. The amount of thread IDs should be the same with the amount of parameters.
        # 2. The done-timestamp should be very close.
        TestSimpleExecutor._chk_map_record(len(_args))


    def test_map_with_function(self, instantiate_adapter_executor: SimpleExecutor):

        TestSimpleExecutor._initial()

        _function_a_flag = Global_Manager.Value(int, 0)
        _function_b_flag = Global_Manager.Value(int, 0)

        def _target_a(*args):
            global Running_Worker_IDs, Running_Current_Workers, Running_Finish_Timestamp
            nonlocal _function_a_flag

            _function_a_flag.value += 1
            _ident = threading.current_thread().ident
            _current_worker = threading.current_thread()

            Running_Worker_IDs.append(_ident)
            Running_Current_Workers.append(str(_current_worker))
            Running_Finish_Timestamp.append(int(time.time()))

            time.sleep(_Test_Function_Sleep_Time)

        def _target_b(*args):
            global Running_Worker_IDs, Running_Current_Workers, Running_Finish_Timestamp
            nonlocal _function_b_flag

            _function_b_flag.value += 1
            _ident = threading.current_thread().ident
            _current_worker = threading.current_thread()

            Running_Worker_IDs.append(_ident)
            Running_Current_Workers.append(str(_current_worker))
            Running_Finish_Timestamp.append(int(time.time()))

            time.sleep(_Test_Function_Sleep_Time)

        _functions = [_target_a, _target_b]
        instantiate_adapter_executor.map_with_function(functions=_functions)
        _results = instantiate_adapter_executor.result()
        assert len(_results) == len(_functions), ""
        # Do some checking
        # 1. The amount of workers should be the same with the amount of functions.
        # 3. The amount of thread IDs should be the same with the amount of functions.
        # 2. The done-timestamp should be very close.
        # TestSimpleExecutor._chk_map_with_function(_functions, _function_a_flag, _function_b_flag, _worker_ids, _workers, _done_timestamp)
        global Running_Worker_IDs, Running_Current_Workers, Running_Finish_Timestamp
        TestSimpleExecutor._chk_map_with_function(_functions, _function_a_flag, _function_b_flag, Running_Worker_IDs, Running_Current_Workers, Running_Finish_Timestamp)


    def test_result(self, instantiate_adapter_executor: SimpleExecutor):

        def _target(*args, **kwargs):
            _current_worker = threading.current_thread()
            return f"result_{_current_worker}"

        instantiate_adapter_executor.run(function=_target)
        _results = instantiate_adapter_executor.result()
        assert len(_results) == _Worker_Size, ""
        for _r in _results:
            assert "result_" in _r.data, ""
            assert _r.worker_name, ""
            assert _r.worker_ident, ""
            assert _r.state, ""
            assert _r.pid, ""
            assert _r.exception is None, ""

