from multirunnable import RunningMode, SimplePool
from multirunnable.parallel.strategy import ProcessPoolStrategy
from multirunnable.concurrent.strategy import ThreadPoolStrategy
from multirunnable.coroutine.strategy import GreenThreadPoolStrategy

from .framework.strategy import PoolRunningTestSpec
from .test_config import (
    Worker_Pool_Size, Task_Size,
    Running_Diff_Time, Test_Function_Sleep_Time,
    Test_Function_Args, Test_Function_Kwargs, Test_Function_Multiple_Args)

from typing import List, Tuple, Dict
import threading
import pytest
import time
import os


_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size


Running_Diff_Time: int = Running_Diff_Time

_Thread_Lock = threading.Lock()

Running_Parent_PID = None
Running_Count = 0
Running_Thread_IDs: List = []
Running_PPIDs: List = []
Running_Current_Threads: List = []
Running_Finish_Timestamp: List = []

Pool_Running_Count = 0

Test_Function_Sleep_Time = Test_Function_Sleep_Time
Test_Function_Args: Tuple = Test_Function_Args
Test_Function_Kwargs: Dict = Test_Function_Kwargs
Test_Function_Multiple_Args = Test_Function_Multiple_Args


def reset_pool_running_value() -> None:
    global Pool_Running_Count
    Pool_Running_Count = 0


def reset_running_timer() -> None:
    global Running_Thread_IDs, Running_PPIDs, Running_Current_Threads, Running_Finish_Timestamp
    Running_Thread_IDs[:] = []
    Running_PPIDs[:] = []
    Running_Current_Threads[:] = []
    Running_Finish_Timestamp[:] = []


def pool_target_fun(*args, **kwargs) -> str:
    global Pool_Running_Count

    with _Thread_Lock:
        Pool_Running_Count += 1

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

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
        Pool_Running_Count += 1

        if args:
            assert set(args) <= set(Test_Function_Args), f"The argument *args* should be one of element of the input outside."
            if len(args) > 1:
                assert args == Test_Function_Args, f"The argument *args* should be same as the global variable 'Test_Function_Args'."
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


def target_funcs_iter():
    return [pool_target_fun for _ in range(_Task_Size)]


@pytest.fixture(scope="function")
def process_pool():
    return SimplePool(mode=RunningMode.Parallel, pool_size=_Worker_Pool_Size, tasks_size=_Task_Size)


@pytest.fixture(scope="function")
def thread_pool():
    return SimplePool(mode=RunningMode.Concurrent, pool_size=_Worker_Pool_Size, tasks_size=_Task_Size)


@pytest.fixture(scope="function")
def green_thread_pool():
    return SimplePool(mode=RunningMode.GreenThread, pool_size=_Worker_Pool_Size, tasks_size=_Task_Size)


class TestSimplePool:

    """
    Description:
        Testing executor which may be as Process, Thread, Green Thread or Asynchronous object.
        The responsibility of this object is calling the mapping method(s) by the RunningMode.
        For example, it will use 'multiprocessing.Process.start' when you call 'run' with RunningMode.Parallel.

        For the testing concern, we should pay the attention to the feature of responsibility which means
        it should target at the feature about 'Procedure' and 'Adapter of features', doesn't working process.
    """

    def test_initial_running_strategy_with_parallel(self, process_pool: SimplePool):
        process_pool._initial_running_strategy()

        from multirunnable.pool import Pool_Runnable_Strategy
        assert Pool_Runnable_Strategy is not None, f"It should be assign running-strategy instance."
        assert isinstance(Pool_Runnable_Strategy, ProcessPoolStrategy), f"It should be an sub-instance of 'ProcessPoolStrategy'."


    def test_initial_running_strategy_with_concurrent(self, thread_pool: SimplePool):
        thread_pool._initial_running_strategy()

        from multirunnable.pool import Pool_Runnable_Strategy
        assert Pool_Runnable_Strategy is not None, f"It should be assign running-strategy instance."
        assert isinstance(Pool_Runnable_Strategy, ThreadPoolStrategy), f"It should be an sub-instance of 'ThreadPoolStrategy'."


    def test_initial_running_strategy_with_coroutine(self, green_thread_pool: SimplePool):
        green_thread_pool._initial_running_strategy()

        from multirunnable.pool import Pool_Runnable_Strategy
        assert Pool_Runnable_Strategy is not None, f"It should be assign running-strategy instance."
        assert isinstance(Pool_Runnable_Strategy, GreenThreadPoolStrategy), f"It should be an sub-instance of 'GreenThreadPoolStrategy'."


    def test_apply(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.apply(function=pool_target_fun)
        TestSimplePool._chk_blocking_record()


    def test_apply_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.apply(function=pool_target_fun)
        TestSimplePool._chk_blocking_record()


    def test_async_apply(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.async_apply(function=pool_target_fun)
        TestSimplePool._chk_record()


    def test_async_apply_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.async_apply(function=pool_target_fun)
        TestSimplePool._chk_record()


    def test_apply_with_iter(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()


    def test_apply_with_iter_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()


    def test_async_apply_with_iter(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()


    def test_async_apply_with_iter_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()


    def test_map(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()


    def test_map_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()


    def test_async_map(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.async_map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()


    def test_async_map_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.async_map(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()


    def test_map_by_args(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()


    def test_map_by_args_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()


    def test_async_map_by_args(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.async_map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()


    def test_async_map_by_args_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.async_map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()


    def test_imap(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.imap(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()


    def test_imap_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.imap(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()


    def test_imap_unordered(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        thread_pool.initial()
        thread_pool.imap_unordered(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()


    def test_imap_unordered_by_pykeyword_with(self, thread_pool: SimplePool):
        TestSimplePool._initial()
        with thread_pool as _pool:
            _pool.imap_unordered(function=map_target_fun, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()


    def test_terminal(self, thread_pool: SimplePool):
        try:
            thread_pool.initial()
            thread_pool.async_apply(function=lambda a: a+a, args=(1,))
            thread_pool.terminal()
        except Exception as e:
            assert False, f"It should work finely without any issue. Please check it."
        else:
            assert True, f"It work finely without any issue."


    def test_close(self, thread_pool: SimplePool):
        try:
            thread_pool.initial()
            thread_pool.async_apply(function=lambda a: a+a, args=(1,))
            thread_pool.close()
        except Exception as e:
            assert False, f"It should work finely without any issue. Please check it."
        else:
            assert True, f"It work finely without any issue."


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_get_result(self, thread_pool: SimplePool):
        thread_pool.get_result()


    @staticmethod
    def _initial():
        # Test for parameters with '**kwargs'
        reset_pool_running_value()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_blocking_record():
        print(f"[DEBUG] Running_PPIDs: {Running_PPIDs}")
        print(f"[DEBUG] Running_Parent_PID: {Running_Parent_PID}")
        print(f"[DEBUG] Pool_Running_Count.value: {Pool_Running_Count}")
        print(f"[DEBUG] _Task_Size: {_Task_Size}")
        print(f"[DEBUG] Running_Thread_IDs: {Running_Thread_IDs}")
        print(f"[DEBUG] Running_Current_Threads: {Running_Current_Threads}")
        print(f"[DEBUG] Running_Finish_Timestamp: {Running_Finish_Timestamp}")
        # PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_blocking(
            pool_running_cnt=Pool_Running_Count,
            worker_size=_Task_Size,
            running_worker_ids=Running_Thread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp,
            de_duplicate=False
        )


    @staticmethod
    def _chk_record():
        print(f"[DEBUG] Running_PPIDs: {Running_PPIDs}")
        print(f"[DEBUG] Running_Parent_PID: {Running_Parent_PID}")
        print(f"[DEBUG] Pool_Running_Count.value: {Pool_Running_Count}")
        print(f"[DEBUG] _Task_Size: {_Task_Size}")
        print(f"[DEBUG] Running_Thread_IDs: {Running_Thread_IDs}")
        print(f"[DEBUG] Running_Current_Threads: {Running_Current_Threads}")
        print(f"[DEBUG] Running_Finish_Timestamp: {Running_Finish_Timestamp}")
        # PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record(
            pool_running_cnt=Pool_Running_Count,
            worker_size=_Task_Size,
            running_worker_ids=Running_Thread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    @staticmethod
    def _chk_map_record():
        # PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_map(
            pool_running_cnt=Pool_Running_Count,
            function_args=Test_Function_Args,
            running_worker_ids=Running_Thread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp
        )

