import threading
import pytest
import time

from multirunnable.concurrent.strategy import ThreadStrategy
from multirunnable.coroutine.strategy import GreenThreadStrategy, AsynchronousStrategy
from multirunnable.parallel.strategy import ProcessStrategy
from multirunnable.parallel.share import Global_Manager
from multirunnable.executor import AdapterExecutor
from multirunnable import get_current_mode, set_mode, RunningMode, SimpleExecutor

from ..test_config import Worker_Size, Running_Diff_Time, Test_Function_Sleep_Time, Test_Function_Args
from .._examples import (
    # # Import the falgs
    get_running_cnt, get_current_workers, get_running_workers_ids, get_running_done_timestamps,
    # # Import some common functions
    reset_running_flags, initial_lock, initial_rlock, _get_current_worker, _get_worker_id, _sleep_time,
    # # Import some target functions to run for Pool object
    target_function, target_function_for_map
)
from .framework.strategy import GeneralRunningTestSpec


_Worker_Size = Worker_Size
_Running_Diff_Time: int = Running_Diff_Time
_Test_Function_Sleep_Time = Test_Function_Sleep_Time


@pytest.fixture(scope="function")
def instantiate_executor(request) -> SimpleExecutor:
    set_mode(mode=request.param)
    _executor = SimpleExecutor(mode=request.param, executors=_Worker_Size)
    initial_lock()
    return _executor


@pytest.fixture(scope="function")
def instantiate_adapter_executor() -> AdapterExecutor:
    set_mode(mode=RunningMode.Concurrent)
    _executor = AdapterExecutor(strategy=ThreadStrategy(executors=_Worker_Size))
    initial_lock()
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

        _workers = [instantiate_executor.start_new_worker(target=target_function) for _ in range(_Worker_Size)]
        instantiate_executor.close(workers=_workers)
        _results = instantiate_executor.result()
        assert len(_results) == _Worker_Size, ""
        TestSimpleExecutor._chk_run_record(expected_size=Worker_Size)


    @pytest.mark.parametrize(
        argnames="instantiate_executor",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_run(self, instantiate_executor: SimpleExecutor):
        TestSimpleExecutor._initial()
        initial_lock()

        instantiate_executor.run(function=target_function)
        _results = instantiate_executor.result()
        assert len(_results) == _Worker_Size, ""
        TestSimpleExecutor._chk_run_record(expected_size=Worker_Size)


    @pytest.mark.parametrize(
        argnames="instantiate_executor",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map(self, instantiate_executor: SimpleExecutor):
        TestSimpleExecutor._initial()
        initial_lock()

        instantiate_executor.map(function=target_function_for_map, args_iter=Test_Function_Args)
        _results = instantiate_executor.result()
        assert len(_results) == len(Test_Function_Args), ""
        TestSimpleExecutor._chk_run_record(expected_size=len(Test_Function_Args), de_duplicate=False)


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

        _workers_ids = Global_Manager.list()
        _current_workers = Global_Manager.list()
        _done_timestamp = Global_Manager.list()

        def _target_a(*args):
            nonlocal _function_a_flag, _workers_ids, _current_workers, _done_timestamp

            _function_a_flag.value += 1
            _ident = _get_worker_id()
            _current_worker = _get_current_worker()

            _workers_ids.append(_ident)
            _current_workers.append(str(_current_worker))
            _done_timestamp.append(int(time.time()))

            _sleep_time()

        def _target_b(*args):
            nonlocal _function_b_flag, _workers_ids, _current_workers, _done_timestamp

            _function_b_flag.value += 1
            _ident = _get_worker_id()
            _current_worker = _get_current_worker()

            _workers_ids.append(_ident)
            _current_workers.append(str(_current_worker))
            _done_timestamp.append(int(time.time()))

            _sleep_time()

        _functions = [_target_a, _target_b]
        instantiate_executor.map_with_function(functions=_functions)
        _results = instantiate_executor.result()
        assert len(_results) == len(_functions), ""
        TestSimpleExecutor._chk_map_with_function(_functions, _function_a_flag, _function_b_flag, _workers_ids, _current_workers, _done_timestamp)


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
        reset_running_flags()


    @staticmethod
    def _chk_run_record(expected_size: int, de_duplicate: bool = True) -> None:
        GeneralRunningTestSpec._chk_process_record(
            running_cnt=get_running_cnt(),
            worker_size=expected_size,
            running_wokrer_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps(),
            de_duplicate=de_duplicate
        )


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

        _workers = [instantiate_adapter_executor.start_new_worker(target=target_function) for _ in range(_Worker_Size)]
        instantiate_adapter_executor.close(workers=_workers)
        _results = instantiate_adapter_executor.result()
        assert len(_results) == _Worker_Size, ""
        TestSimpleExecutor._chk_run_record(expected_size=Worker_Size)


    def test_run(self, instantiate_adapter_executor: SimpleExecutor):
        TestSimpleExecutor._initial()

        instantiate_adapter_executor.run(function=target_function)
        _results = instantiate_adapter_executor.result()
        assert len(_results) == _Worker_Size, ""
        TestSimpleExecutor._chk_run_record(expected_size=Worker_Size)


    def test_map(self, instantiate_adapter_executor: SimpleExecutor):
        TestSimpleExecutor._initial()

        instantiate_adapter_executor.map(function=target_function_for_map, args_iter=Test_Function_Args)
        _results = instantiate_adapter_executor.result()
        assert len(_results) == len(Test_Function_Args), ""
        TestSimpleExecutor._chk_run_record(expected_size=len(Test_Function_Args))


    def test_map_with_function(self, instantiate_adapter_executor: SimpleExecutor):

        TestSimpleExecutor._initial()

        _function_a_flag = Global_Manager.Value(int, 0)
        _function_b_flag = Global_Manager.Value(int, 0)

        _workers_ids = Global_Manager.list()
        _current_workers = Global_Manager.list()
        _done_timestamp = Global_Manager.list()

        def _target_a(*args):
            nonlocal _function_a_flag, _workers_ids, _current_workers, _done_timestamp

            _function_a_flag.value += 1
            _ident = threading.current_thread().ident
            _current_worker = threading.current_thread()

            _workers_ids.append(_ident)
            _current_workers.append(str(_current_worker))
            _done_timestamp.append(int(time.time()))

            time.sleep(_Test_Function_Sleep_Time)

        def _target_b(*args):
            nonlocal _function_b_flag, _workers_ids, _current_workers, _done_timestamp

            _function_b_flag.value += 1
            _ident = threading.current_thread().ident
            _current_worker = threading.current_thread()

            _workers_ids.append(_ident)
            _current_workers.append(str(_current_worker))
            _done_timestamp.append(int(time.time()))

            time.sleep(_Test_Function_Sleep_Time)

        _functions = [_target_a, _target_b]
        instantiate_adapter_executor.map_with_function(functions=_functions)
        _results = instantiate_adapter_executor.result()
        assert len(_results) == len(_functions), ""
        TestSimpleExecutor._chk_map_with_function(_functions, _function_a_flag, _function_b_flag, _workers_ids, _current_workers, _done_timestamp)


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

