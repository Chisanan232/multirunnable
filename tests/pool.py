from multirunnable import get_current_mode, set_mode, RunningMode, SimplePool
from multirunnable.pool import AdapterPool
from multirunnable.parallel.strategy import ProcessPoolStrategy
from multirunnable.parallel.share import Global_Manager
from multirunnable.concurrent.strategy import ThreadPoolStrategy
from multirunnable.coroutine.strategy import GreenThreadPoolStrategy

from .framework.strategy import PoolRunningTestSpec
from .test_config import (
    Worker_Pool_Size, Task_Size,
    Running_Diff_Time, Test_Function_Sleep_Time,
    Test_Function_Args, Test_Function_Kwargs, Test_Function_Multiple_Args)

from typing import List, Tuple, Dict, Any
import multiprocessing as mp
import threading
import gevent.lock
import gevent
import pytest
import time
import os


_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size


Running_Diff_Time: int = Running_Diff_Time

_Thread_Lock = threading.Lock()

Running_Parent_PID = None
Running_Count = Global_Manager.Value(int, 0)
Running_Workers_IDs: List = Global_Manager.list()
Running_PPIDs: List = Global_Manager.list()
Running_Current_Workers: List = Global_Manager.list()
Running_Finish_Timestamp: List = Global_Manager.list()

Pool_Running_Count = Global_Manager.Value(int, 0)

Test_Function_Sleep_Time = Test_Function_Sleep_Time
Test_Function_Args: Tuple = Test_Function_Args
Test_Function_Kwargs: Dict = Test_Function_Kwargs
Test_Function_Multiple_Args = Test_Function_Multiple_Args


def initial_lock() -> None:
    global _Worker_Lock

    _rmode = get_current_mode(force=True)

    if _rmode is RunningMode.Parallel:
        _Worker_Lock = mp.Lock()
    elif _rmode is RunningMode.Concurrent:
        _Worker_Lock = threading.Lock()
    elif _rmode is RunningMode.GreenThread:
        _Worker_Lock = gevent.lock.RLock()
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
    else:
        raise ValueError("The RunningMode has the unexpected mode.")

    return str(_worker_id)


def _sleep_time() -> None:
    _rmode = get_current_mode(force=True)

    if _rmode is RunningMode.Parallel or _rmode is RunningMode.Concurrent:
        time.sleep(Test_Function_Sleep_Time)
    elif _rmode is RunningMode.GreenThread:
        gevent.sleep(Test_Function_Sleep_Time)
    else:
        raise ValueError("The RunningMode has the unexpected mode.")


def reset_pool_running_value() -> None:
    global Pool_Running_Count
    Pool_Running_Count.value = 0


def reset_running_timer() -> None:
    global Running_Workers_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp
    Running_Workers_IDs[:] = []
    Running_PPIDs[:] = []
    Running_Current_Workers[:] = []
    Running_Finish_Timestamp[:] = []


def pool_target_fun(*args, **kwargs) -> str:
    global Pool_Running_Count

    with _Thread_Lock:
        Pool_Running_Count.value += 1

        if args:
            assert args == Test_Function_Args, "The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, "The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        _ident = _get_worker_id()
        _current_worker = _get_current_worker()
        # _ident = threading.get_ident()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_Workers_IDs.append(_ident)
        Running_PPIDs.append(_ppid)
        Running_Current_Workers.append(str(_current_worker))
        Running_Finish_Timestamp.append(_time)

    _sleep_time()
    return f"result_{_ident}"


def map_target_fun(*args, **kwargs):
    """
    Description:
        Test for 'map', 'starmap' methods.
    :param args:
    :param kwargs:
    :return:
    """
    global Pool_Running_Count

    with _Thread_Lock:
        Pool_Running_Count.value += 1

        if args:
            assert set(args) <= set(Test_Function_Args), "The argument *args* should be one of element of the input outside."
            if len(args) > 1:
                assert args == Test_Function_Args, "The argument *args* should be same as the global variable 'Test_Function_Args'."
        if kwargs:
            assert kwargs is None or kwargs == {}, "The argument *kwargs* should be empty or None value."

        _pid = os.getpid()
        _ppid = os.getppid()
        _ident = _get_worker_id()
        # _ident = threading.get_ident()
        # _time = str(datetime.datetime.now())
        _current_worker = _get_current_worker()
        _time = int(time.time())

        Running_Workers_IDs.append(_ident)
        Running_PPIDs.append(_ppid)
        Running_Current_Workers.append(str(_current_worker))
        Running_Finish_Timestamp.append(_time)

    _sleep_time()
    return f"result_{_current_worker}"


def target_funcs_iter():
    return [pool_target_fun for _ in range(_Task_Size)]


@pytest.fixture(scope="function")
def simple_pool(request) -> SimplePool:
    return SimplePool(mode=request.param, pool_size=_Worker_Pool_Size)


@pytest.fixture(scope="function")
def adapter_pool() -> AdapterPool:
    set_mode(RunningMode.Concurrent)
    return AdapterPool(strategy=ThreadPoolStrategy(pool_size=_Worker_Pool_Size))



class TestSimplePool:

    """
    Description:
        Testing executor which may be as Process, Thread, Green Thread or Asynchronous object.
        The responsibility of this object is calling the mapping method(s) by the RunningMode.
        For example, it will use 'multiprocessing.Process.start' when you call 'run' with RunningMode.Parallel.

        For the testing concern, we should pay the attention to the feature of responsibility which means
        it should target at the feature about 'Procedure' and 'Adapter of features', doesn't working process.
    """

    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_initial_running_strategy(self, simple_pool: SimplePool):
        simple_pool._initial_running_strategy()

        _rmode = get_current_mode(force=True)

        from multirunnable.pool import Pool_Runnable_Strategy
        if _rmode is RunningMode.Parallel:
            assert Pool_Runnable_Strategy is not None, "It should be assign running-strategy instance."
            assert isinstance(Pool_Runnable_Strategy, ProcessPoolStrategy), "It should be an sub-instance of 'ProcessPoolStrategy'."
        elif _rmode is RunningMode.Concurrent:
            assert Pool_Runnable_Strategy is not None, "It should be assign running-strategy instance."
            assert isinstance(Pool_Runnable_Strategy, ThreadPoolStrategy), "It should be an sub-instance of 'ThreadPoolStrategy'."
        elif _rmode is RunningMode.GreenThread:
            assert Pool_Runnable_Strategy is not None, "It should be assign running-strategy instance."
            assert isinstance(Pool_Runnable_Strategy, GreenThreadPoolStrategy), "It should be an sub-instance of 'GreenThreadPoolStrategy'."
        else:
            raise ValueError("The RunningMode has the unexpected mode.")


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_apply(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.apply(tasks_size=Task_Size, function=pool_target_fun)
        TestSimplePool._chk_blocking_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_apply_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.apply(tasks_size=Task_Size, function=pool_target_fun)
        TestSimplePool._chk_blocking_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_apply(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.async_apply(tasks_size=Task_Size, function=pool_target_fun)
        TestSimplePool._chk_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_apply_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.async_apply(tasks_size=Task_Size, function=pool_target_fun)
        TestSimplePool._chk_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_apply_with_iter(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_apply_with_iter_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_apply_with_iter(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_apply_with_iter_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_map(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.async_map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_map_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.async_map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map_by_args(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map_by_args_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_map_by_args(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.async_map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_map_by_args_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.async_map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_imap(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.imap(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_imap_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.imap(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_imap_unordered(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.imap_unordered(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_imap_unordered_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.imap_unordered(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_terminal(self, simple_pool: SimplePool):
        try:
            simple_pool.initial()
            simple_pool.async_apply(tasks_size=Task_Size, function=lambda a: a+a, args=(1,))
            simple_pool.terminal()
        except Exception as e:
            assert False, "It should work finely without any issue. Please check it."
        else:
            assert True, "It work finely without any issue."


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_close(self, simple_pool: SimplePool):
        try:
            simple_pool.initial()
            simple_pool.async_apply(tasks_size=Task_Size, function=lambda a: a+a, args=(1,))
            simple_pool.close()
        except Exception as e:
            assert False, "It should work finely without any issue. Please check it."
        else:
            assert True, "It work finely without any issue."


    @staticmethod
    def _initial():
        # Test for parameters with '**kwargs'
        reset_pool_running_value()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_blocking_record():
        # PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_blocking(
            pool_running_cnt=Pool_Running_Count.value,
            worker_size=_Task_Size,
            running_worker_ids=Running_Workers_IDs,
            running_current_workers=Running_Current_Workers,
            running_finish_timestamps=Running_Finish_Timestamp,
            de_duplicate=False
        )


    @staticmethod
    def _chk_record():
        # PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record(
            pool_running_cnt=Pool_Running_Count.value,
            worker_size=_Task_Size,
            running_worker_ids=Running_Workers_IDs,
            running_current_workers=Running_Current_Workers,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    @staticmethod
    def _chk_map_record():
        # PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_map(
            pool_running_cnt=Pool_Running_Count.value,
            function_args=Test_Function_Args,
            running_worker_ids=Running_Workers_IDs,
            running_current_workers=Running_Current_Workers,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    @staticmethod
    def chk_results(results, expected_size):
        assert results, "It should have something, it couldn't be empty or None."
        assert len(results) == expected_size, f"The result length should be equal to the expected value '{expected_size}'."
        for _r in results:
            assert "result_" in _r.data, "The result value should be same as the return value of target function."
            assert _r.exception is None, f"The exception should be nothing. But it got {_r.exception}."
            assert _r.is_successful is True, "It should work finely."



class TestAdapterPool:

    def test_apply(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.apply(tasks_size=Task_Size, function=pool_target_fun)
        TestSimplePool._chk_blocking_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_apply_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.apply(tasks_size=Task_Size, function=pool_target_fun)
        TestSimplePool._chk_blocking_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_async_apply(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.async_apply(tasks_size=Task_Size, function=pool_target_fun)
        TestSimplePool._chk_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_async_apply_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.async_apply(tasks_size=Task_Size, function=pool_target_fun)
        TestSimplePool._chk_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_apply_with_iter(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_apply_with_iter_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_async_apply_with_iter(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_async_apply_with_iter_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_map(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_map_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_async_map(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.async_map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_async_map_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.async_map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_map_by_args(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    def test_map_by_args_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    def test_async_map_by_args(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.async_map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    def test_async_map_by_args_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.async_map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    def test_imap(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.imap(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_imap_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.imap(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_imap_unordered(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.imap_unordered(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_imap_unordered_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.imap_unordered(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_terminal(self, adapter_pool: AdapterPool):
        try:
            adapter_pool.initial()
            adapter_pool.async_apply(tasks_size=Task_Size, function=lambda a: a+a, args=(1,))
            adapter_pool.terminal()
        except Exception as e:
            assert False, "It should work finely without any issue. Please check it."
        else:
            assert True, "It work finely without any issue."


    def test_close(self, adapter_pool: AdapterPool):
        try:
            adapter_pool.initial()
            adapter_pool.async_apply(tasks_size=Task_Size, function=lambda a: a+a, args=(1,))
            adapter_pool.close()
        except Exception as e:
            assert False, "It should work finely without any issue. Please check it."
        else:
            assert True, "It work finely without any issue."

