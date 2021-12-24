from multirunnable.coroutine.strategy import CoroutineStrategy, GreenThreadStrategy, GreenThreadPoolStrategy, AsynchronousStrategy
from multirunnable import async_sleep

from ..framework.strategy import GeneralRunningTestSpec, PoolRunningTestSpec
from ..test_config import (
    Worker_Size, Worker_Pool_Size, Task_Size,
    Running_Diff_Time,
    Test_Function_Sleep_Time,
    Test_Function_Args, Test_Function_Multiple_Args, Test_Function_Kwargs)

from typing import List, Tuple, Dict
from gevent.threading import get_ident as get_green_thread_ident, getcurrent as get_current_green_thread, Lock as GeventLock
from asyncio.locks import Lock as AsyncLock
import datetime
import asyncio
import gevent
import pytest
import time
import os


Green_Thread_Size: int = Worker_Size
Pool_Size: int = Worker_Pool_Size
Task_Size: int = Task_Size

Running_Diff_Time: int = Running_Diff_Time

_GreenThread_Lock = GeventLock()
_Async_Lock = AsyncLock(loop=asyncio.get_event_loop())

Running_Parent_PID = None
Running_Count = 0
Running_GreenThread_IDs: List = []
Running_PPIDs: List = []
Running_Current_Threads: List = []
Running_Finish_Timestamp: List = []

Pool_Running_Count = 0


def reset_running_flag() -> None:
    global Running_Count
    Running_Count = 0


def reset_pool_running_value() -> None:
    global Pool_Running_Count
    Pool_Running_Count = 0


def reset_running_timer() -> None:
    global Running_GreenThread_IDs, Running_PPIDs, Running_Current_Threads, Running_Finish_Timestamp
    Running_GreenThread_IDs[:] = []
    Running_PPIDs[:] = []
    Running_Current_Threads[:] = []
    Running_Finish_Timestamp[:] = []


Test_Function_Sleep_Time = Test_Function_Sleep_Time
Test_Function_Args: Tuple = Test_Function_Args
Test_Function_Kwargs: Dict = Test_Function_Kwargs
Test_Function_Multiple_Args = Test_Function_Multiple_Args
Test_Function_Multiple_Diff_Args = ((1, 2, 3), (4, 5, 6), (7, "index_8", 9))


def target_fun(*args, **kwargs) -> str:
    global Running_Count

    with _GreenThread_Lock:
        Running_Count += 1

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        _ident = __get_current_thread_ident()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_GreenThread_IDs.append(_ident)
        Running_PPIDs.append(_ppid)
        Running_Current_Threads.append(__get_current_thread())
        Running_Finish_Timestamp.append(_time)

    gevent.sleep(Test_Function_Sleep_Time)
    return f"result_{__get_current_thread()}"


def pool_target_fun(*args, **kwargs) -> str:
    global Pool_Running_Count

    with _GreenThread_Lock:
        Pool_Running_Count += 1

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        _ident = __get_current_thread_ident()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_GreenThread_IDs.append(_ident)
        Running_PPIDs.append(_ppid)
        Running_Current_Threads.append(__get_current_thread())
        Running_Finish_Timestamp.append(_time)

    gevent.sleep(Test_Function_Sleep_Time)
    return f"result_{__get_current_thread()}"


def map_target_fun(*args, **kwargs):
    """
    Description:
        Test for 'map', 'starmap' methods.
    :param args:
    :param kwargs:
    :return:
    """
    global Pool_Running_Count

    with _GreenThread_Lock:
        Pool_Running_Count += 1

        if args:
            assert set(args) <= set(Test_Function_Args), f"The argument *args* should be one of element of the input outside."
            if len(args) > 1:
                assert args == Test_Function_Args, f"The argument *args* should be same as the global variable 'Test_Function_Args'."
        if kwargs:
            assert kwargs is None or kwargs == {}, f"The argument *kwargs* should be empty or None value."

        _pid = os.getpid()
        _ppid = os.getppid()
        _ident = __get_current_thread_ident()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_GreenThread_IDs.append(_ident)
        Running_PPIDs.append(_ppid)
        Running_Current_Threads.append(__get_current_thread())
        Running_Finish_Timestamp.append(_time)

    gevent.sleep(Test_Function_Sleep_Time)
    return f"result_{__get_current_thread()}"


def map_target_fun_with_diff_args(*args, **kwargs):
    """
    Description:
        Test for 'map', 'starmap' methods.
    :param args:
    :param kwargs:
    :return:
    """
    global Pool_Running_Count

    with _GreenThread_Lock:
        Pool_Running_Count += 1

        if args:
            assert {args} <= set(Test_Function_Multiple_Diff_Args), f"The argument *args* should be one of element of the input outside."
            # if len(args) > 1:
            #     assert args == Test_Function_Args, f"The argument *args* should be same as the global variable 'Test_Function_Args'."
        if kwargs:
            assert kwargs is None or kwargs == {}, f"The argument *kwargs* should be empty or None value."

        _pid = os.getpid()
        _ppid = os.getppid()
        _ident = __get_current_thread_ident()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_GreenThread_IDs.append(_ident)
        Running_PPIDs.append(_ppid)
        Running_Current_Threads.append(__get_current_thread())
        Running_Finish_Timestamp.append(_time)

    gevent.sleep(Test_Function_Sleep_Time)
    return f"result_{__get_current_thread()}"


def __get_current_thread_ident():
    # import gevent.threading as gthreading
    # return gthreading.get_ident()
    return get_green_thread_ident()


def __get_current_thread():
    # import gevent.threading as gthreading
    # return str(gthreading.getcurrent())
    return get_current_green_thread()


async def target_async_fun(*args, **kwargs) -> str:
    global Running_Count

    async with _Async_Lock:
        Running_Count += 1

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        _current_task = asyncio.current_task(loop=asyncio.get_event_loop())
        # _async_task_name = _current_task.get_name()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        # Running_GreenThread_IDs.append(_async_task_name)
        Running_PPIDs.append(_ppid)
        Running_Current_Threads.append(_current_task)
        Running_Finish_Timestamp.append(_time)

    # await async_sleep(Test_Function_Sleep_Time)
    await asyncio.sleep(Test_Function_Sleep_Time)
    return f"result_{_current_task}"


class TargetCls:

    def method(self, *args, **kwargs) -> None:
        target_fun(*args, **kwargs)


    @classmethod
    def classmethod_fun(cls, *args, **kwargs) -> None:
        target_fun(*args, **kwargs)


    @staticmethod
    def staticmethod_fun(*args, **kwargs) -> None:
        target_fun(*args, **kwargs)


class TargetPoolCls:

    def method(self, *args, **kwargs) -> None:
        pool_target_fun(*args, **kwargs)


    @classmethod
    def classmethod_fun(cls, *args, **kwargs) -> None:
        pool_target_fun(*args, **kwargs)


    @staticmethod
    def staticmethod_fun(*args, **kwargs) -> None:
        pool_target_fun(*args, **kwargs)


class TargetPoolMapCls:

    def method(self, *args, **kwargs) -> None:
        map_target_fun(*args, **kwargs)


    @classmethod
    def classmethod_fun(cls, *args, **kwargs) -> None:
        map_target_fun(*args, **kwargs)


    @staticmethod
    def staticmethod_fun(*args, **kwargs) -> None:
        map_target_fun(*args, **kwargs)


class TargetAsyncCls:

    async def method(self, *args, **kwargs) -> None:
        await target_async_fun(*args, **kwargs)


    @classmethod
    async def classmethod_fun(cls, *args, **kwargs) -> None:
        await target_async_fun(*args, **kwargs)


    @staticmethod
    async def staticmethod_fun(*args, **kwargs) -> None:
        await target_async_fun(*args, **kwargs)


@pytest.fixture(scope="class")
def strategy() -> GreenThreadStrategy:
    return GreenThreadStrategy(executors=Green_Thread_Size)


@pytest.fixture(scope="class")
def pool_strategy() -> GreenThreadPoolStrategy:
    _strategy = GreenThreadPoolStrategy(pool_size=Pool_Size, tasks_size=Task_Size)
    _strategy.initialization()
    return _strategy


@pytest.fixture(scope="class")
def async_strategy() -> AsynchronousStrategy:
    return AsynchronousStrategy(executors=Green_Thread_Size)


class TestGreenThread(GeneralRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_initialization(self, strategy: GreenThreadStrategy):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_start_new_worker(self, strategy: GreenThreadStrategy):
        pass


    def test_generate_worker_with_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # Test for no any parameters
        _threads = [strategy.generate_worker(target_fun) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_function_with_args(self, strategy: GreenThreadStrategy):
        # Test for parameters with '*args'
        _threads_with_args = [strategy.generate_worker(target_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads_with_args)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # Test for parameters with '**kwargs'
        _threads_with_kwargs = [strategy.generate_worker(target_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads_with_kwargs)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_bounded_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for no any parameters
        _tc = TargetCls()
        _threads = [strategy.generate_worker(_tc.method) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_bounded_function_with_args(self, strategy: GreenThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '*args'
        _tc = TargetCls()
        _threads_with_args = [strategy.generate_worker(_tc.method, *Test_Function_Args) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads_with_args)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_bounded_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '**kwargs'
        _tc = TargetCls()
        _threads_with_kwargs = [strategy.generate_worker(_tc.method, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads_with_kwargs)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_classmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for no any parameters
        _threads = [strategy.generate_worker(TargetCls.classmethod_fun) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_classmethod_function_with_args(self, strategy: GreenThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '*args'
        _threads_with_args = [strategy.generate_worker(TargetCls.classmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads_with_args)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_classmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '**kwargs'
        _threads_with_kwargs = [strategy.generate_worker(TargetCls.classmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads_with_kwargs)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_staticmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for no any parameters
        _threads = [strategy.generate_worker(TargetCls.staticmethod_fun) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_staticmethod_function_with_args(self, strategy: GreenThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '*args'
        _threads_with_args = [strategy.generate_worker(TargetCls.staticmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads_with_args)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_staticmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '**kwargs'
        _threads_with_kwargs = [strategy.generate_worker(TargetCls.staticmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
        _threads_chksums = map(TestGreenThread._chk_thread_instn, _threads_with_kwargs)
        assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    @staticmethod
    def _chk_thread_instn(_thread) -> bool:
        return isinstance(_thread, gevent.Greenlet)


    def test_activate_workers_with_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _threads = [strategy.generate_worker(target_fun) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads)
        strategy.close(_threads)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_function_with_args(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _threads_with_args = [strategy.generate_worker(target_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads_with_args)
        strategy.close(_threads_with_args)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_function_with_kwargs(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _threads_with_kwargs = [strategy.generate_worker(target_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads_with_kwargs)
        strategy.close(_threads_with_kwargs)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_bounded_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _tc = TargetCls()
        _threads = [strategy.generate_worker(_tc.method) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads)
        strategy.close(_threads)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_bounded_function_with_args(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _tc = TargetCls()
        _threads_with_args = [strategy.generate_worker(_tc.method, *Test_Function_Args) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads_with_args)
        strategy.close(_threads_with_args)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_bounded_function_with_kwargs(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _tc = TargetCls()
        _threads_with_kwargs = [strategy.generate_worker(_tc.method, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads_with_kwargs)
        strategy.close(_threads_with_kwargs)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_classmethod_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _threads = [strategy.generate_worker(TargetCls.classmethod_fun) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads)
        strategy.close(_threads)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_classmethod_function_with_args(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _threads_with_args = [strategy.generate_worker(TargetCls.classmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads_with_args)
        strategy.close(_threads_with_args)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_classmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _threads_with_kwargs = [strategy.generate_worker(TargetCls.classmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads_with_kwargs)
        strategy.close(_threads_with_kwargs)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_staticmethod_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _threads = [strategy.generate_worker(TargetCls.staticmethod_fun) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads)
        strategy.close(_threads)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_staticmethod_function_with_args(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _threads_with_args = [strategy.generate_worker(TargetCls.staticmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads_with_args)
        strategy.close(_threads_with_args)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    def test_activate_workers_with_staticmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        TestGreenThread._initial()

        _threads_with_kwargs = [strategy.generate_worker(TargetCls.staticmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
        strategy.activate_workers(_threads_with_kwargs)
        strategy.close(_threads_with_kwargs)

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_process_record()


    @staticmethod
    def _initial():
        # Test for parameters with '**kwargs'
        reset_running_flag()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_process_record():
        assert Running_Count == Green_Thread_Size, f"The running count should be the same as the amount of process."

        _ppid_list = Running_PPIDs[:]
        _thread_id_list = Running_GreenThread_IDs[:]
        _current_process_list = Running_Current_Threads[:]
        _timestamp_list = Running_Finish_Timestamp[:]

        # assert len(set(_ppid_list)) == 1, f"The PPID of each process should be the same."
        # assert _ppid_list[0] == Running_Parent_PID, f"The PPID should equal to {Running_Parent_PID}. But it got {_ppid_list[0]}."
        assert len(_thread_id_list) == Green_Thread_Size, f"The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_thread_id_list)) == Green_Thread_Size, f"The count of PID (de-duplicate) should be the same as the count of processes."
        assert len(_thread_id_list) == len(_current_process_list), f"The count of current process name (no de-duplicate) should be equal to count of PIDs."
        assert len(set(_thread_id_list)) == len(set(_current_process_list)), f"The count of current process name (de-duplicate) should be equal to count of PIDs."

        _max_timestamp = max(_timestamp_list)
        _min_timestamp = min(_timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, f"Processes should be run in the same time period."


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_close(self, strategy: GreenThreadStrategy):
        # Test for no any parameters
        # process_strategy.close(self.__Processes)
        # _active_children_list = mp.active_children()
        # print(len(_active_children_list) == 0)
        # # assert len(_active_children_list) == 0, f"Processes should be closed finely."
        #
        # # Test for parameters with '*args'
        # process_strategy.close(self.__Processes_With_Args)
        # _active_children_list = mp.active_children()
        # print(len(_active_children_list) == 0)
        # # assert len(_active_children_list) == 0, f"Processes should be closed finely."
        #
        # # Test for parameters with '**kwargs'
        # process_strategy.close(self.__Processes_With_Kwargs)
        # _active_children_list = mp.active_children()
        # print(len(_active_children_list) == 0)
        # assert len(_active_children_list) == 0, f"Processes should be closed finely."
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_terminal(self, strategy: GreenThreadStrategy):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_kill(self, strategy: GreenThreadStrategy):
        pass


    @pytest.mark.skip(reason="Not implement. The result feature not finish.")
    def test_get_result(self, strategy: GreenThreadStrategy):
        pass



class TestGreenThreadPool(PoolRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_initialization(self, pool_strategy: GreenThreadPoolStrategy):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_async_apply(self, pool_strategy: GreenThreadPoolStrategy):
        pass
        # TestGreenThreadPool._initial()
        #
        # pool_strategy.apply(function=pool_target_fun)
        #
        # TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        pool_strategy.async_apply(function=pool_target_fun)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        TestGreenThreadPool._initial()

        pool_strategy.async_apply(function=pool_target_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        TestGreenThreadPool._initial()

        pool_strategy.async_apply(function=pool_target_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_bounded_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        _tc = TargetPoolCls()
        pool_strategy.async_apply(function=_tc.method)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_bounded_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        TestGreenThreadPool._initial()

        _tc = TargetPoolCls()
        pool_strategy.async_apply(function=_tc.method, args=Test_Function_Args)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_bounded_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        TestGreenThreadPool._initial()

        _tc = TargetPoolCls()
        pool_strategy.async_apply(function=_tc.method, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_classmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        pool_strategy.async_apply(function=TargetPoolCls.classmethod_fun)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_classmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        TestGreenThreadPool._initial()

        pool_strategy.async_apply(function=TargetPoolCls.classmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_classmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        TestGreenThreadPool._initial()

        pool_strategy.async_apply(function=TargetPoolCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_staticmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        pool_strategy.async_apply(function=TargetPoolCls.staticmethod_fun)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_staticmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        TestGreenThreadPool._initial()

        pool_strategy.async_apply(function=TargetPoolCls.staticmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_process_record()


    def test_async_apply_with_staticmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        TestGreenThreadPool._initial()

        pool_strategy.async_apply(function=TargetPoolCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_process_record()


    def test_map_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.map(function=map_target_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()

        # Test for parameters with '*args'
        # process_pool_strategy.map(function=target_fun, args_iter=Test_Function_Args)


    def test_map_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        _tc = TargetPoolMapCls()
        pool_strategy.map(function=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_map_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.map(function=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_map_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.map(function=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_async_map_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.async_map(function=map_target_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        _tc = TargetPoolMapCls()
        pool_strategy.async_map(function=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_async_map_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.async_map(function=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_async_map_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.async_map(function=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_map_by_args_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        # With the multiple same parameters
        pool_strategy.map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestGreenThreadPool._chk_process_record_map()

        TestGreenThreadPool._initial()

        # With the multiple different parameters
        pool_strategy.map_by_args(function=map_target_fun_with_diff_args, args_iter=Test_Function_Multiple_Diff_Args)
        TestGreenThreadPool._chk_process_record_map()

        # Test for parameters with '*args'
        # process_pool_strategy.map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_map_by_args_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        _tc = TargetPoolMapCls()
        pool_strategy.map_by_args(function=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_map_by_args_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.map_by_args(function=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_map_by_args_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.map_by_args(function=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_async_map_by_args_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        # With the multiple same parameters
        pool_strategy.async_map_by_args(function=map_target_fun, args_iter=Test_Function_Multiple_Args)
        TestGreenThreadPool._chk_process_record_map()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map_by_args(function=target_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._initial()

        # With the multiple different parameters
        pool_strategy.async_map_by_args(function=map_target_fun_with_diff_args, args_iter=Test_Function_Multiple_Diff_Args)
        TestGreenThreadPool._chk_process_record_map()


    def test_async_map_by_args_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        _tc = TargetPoolMapCls()
        pool_strategy.async_map_by_args(function=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_async_map_by_args_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.async_map_by_args(function=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_async_map_by_args_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        TestGreenThreadPool._initial()

        pool_strategy.async_map_by_args(function=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_imap_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        pool_strategy.imap(function=map_target_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_imap_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        _tc = TargetPoolMapCls()
        pool_strategy.imap(function=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_imap_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        pool_strategy.imap(function=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_imap_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        pool_strategy.imap(function=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_imap_unordered_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        pool_strategy.imap_unordered(function=map_target_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_imap_unordered_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        _tc = TargetPoolMapCls()
        pool_strategy.imap_unordered(function=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_imap_unordered_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        pool_strategy.imap_unordered(function=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    def test_imap_unordered_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        TestGreenThreadPool._initial()

        pool_strategy.imap_unordered(function=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_process_record_map()


    @staticmethod
    def _initial():
        # Test for parameters with '**kwargs'
        reset_pool_running_value()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_process_record():
        assert Pool_Running_Count == Green_Thread_Size, f"The running count should be the same as the process pool size."

        _ppid_list = Running_PPIDs[:]
        _thread_id_list = Running_GreenThread_IDs[:]
        _current_thread_list = Running_Current_Threads[:]
        _timestamp_list = Running_Finish_Timestamp[:]

        # assert len(set(_ppid_list)) == 1, f"The PPID of each process should be the same."
        # assert _ppid_list[0] == Running_Parent_PID, f"The PPID should equal to {Running_Parent_PID}. But it got {_ppid_list[0]}."
        assert len(_thread_id_list) == Green_Thread_Size, f"The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_thread_id_list)) == Green_Thread_Size, f"The count of PID (de-duplicate) should be the same as the count of processes."
        assert len(_thread_id_list) == len(_current_thread_list), f"The count of current process name (no de-duplicate) should be equal to count of PIDs."
        assert len(set(_thread_id_list)) == len(set(_current_thread_list)), f"The count of current process name (de-duplicate) should be equal to count of PIDs."

        _max_timestamp = max(_timestamp_list)
        _min_timestamp = min(_timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, f"Processes should be run in the same time period."


    @staticmethod
    def _chk_process_record_map():
        _argument_size = len(Test_Function_Args)
        assert Pool_Running_Count == _argument_size, f"The running count should be the same as the process pool size."

        _ppid_list = Running_PPIDs[:]
        _thread_id_list = Running_GreenThread_IDs[:]
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


    def test_close(self, pool_strategy: GreenThreadPoolStrategy):
        """
        ValueError: Pool not running
        :param pool_strategy:
        :return:
        """
        try:
            pool_strategy.close()
        except Exception as e:
            assert e is not None, f"It should work finely without any issue."
        else:
            assert True, f"It work finely."


    def test_terminal(self, pool_strategy: GreenThreadPoolStrategy):
        try:
            pool_strategy.terminal()
        except Exception as e:
            assert e is not None, f"It should work finely without any issue."
        else:
            assert True, f"It work finely."


    @pytest.mark.skip(reason="Not implement. The result feature not finish.")
    def test_get_result(self, pool_strategy: GreenThreadPoolStrategy):
        pass



class TestAsynchronous(GeneralRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_initialization(self, async_strategy: AsynchronousStrategy):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_start_new_worker(self, async_strategy: AsynchronousStrategy):
        pass


    def test_generate_worker_with_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # Test for no any parameters
        async def __chk_type():
            _async_tasks = [async_strategy.generate_worker(target_async_fun) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _async_tasks)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_function_with_args(self, async_strategy: AsynchronousStrategy):
        # Test for parameters with '*args'
        async def __chk_type():
            _threads_with_args = [async_strategy.generate_worker(target_async_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads_with_args)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # Test for parameters with '**kwargs'
        async def __chk_type():
            _threads_with_kwargs = [async_strategy.generate_worker(target_async_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads_with_kwargs)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_bounded_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is bounded function.
        # Test for no any parameters
        async def __chk_type():
            _tc = TargetAsyncCls()
            _threads = [async_strategy.generate_worker(_tc.method) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_bounded_function_with_args(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '*args'
        async def __chk_type():
            _tc = TargetAsyncCls()
            _threads_with_args = [async_strategy.generate_worker(_tc.method, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads_with_args)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_bounded_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '**kwargs'
        async def __chk_type():
            _tc = TargetAsyncCls()
            _threads_with_kwargs = [async_strategy.generate_worker(_tc.method, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads_with_kwargs)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_classmethod_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is classmethod function.
        # Test for no any parameters
        async def __chk_type():
            _threads = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_classmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '*args'
        async def __chk_type():
            _threads_with_args = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads_with_args)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_classmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '**kwargs'
        async def __chk_type():
            _threads_with_kwargs = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads_with_kwargs)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_staticmethod_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is staticmethod function.
        # Test for no any parameters
        async def __chk_type():
            _threads = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_staticmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '*args'
        async def __chk_type():
            _threads_with_args = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads_with_args)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    def test_generate_worker_with_staticmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '**kwargs'
        async def __chk_type():
            _threads_with_kwargs = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            _threads_chksums = map(TestAsynchronous._chk_thread_instn, _threads_with_kwargs)
            assert False not in list(_threads_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."

        asyncio.run(__chk_type())


    @staticmethod
    def _chk_thread_instn(_thread) -> bool:
        return isinstance(_thread, asyncio.Task)


    def test_activate_workers_with_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_fun) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_function_with_args(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_bounded_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            _tc = TargetAsyncCls()
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(_tc.method) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_bounded_function_with_args(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            _tc = TargetAsyncCls()
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(_tc.method, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_bounded_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            _tc = TargetAsyncCls()
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(_tc.method, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_classmethod_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_classmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_classmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_staticmethod_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_staticmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    def test_activate_workers_with_staticmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        TestAsynchronous._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        asyncio.run(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_process_record()


    @staticmethod
    def _initial():
        # Test for parameters with '**kwargs'
        reset_running_flag()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_process_record():
        assert Running_Count == Green_Thread_Size, f"The running count should be the same as the amount of process."

        _ppid_list = Running_PPIDs[:]
        _thread_id_list = Running_GreenThread_IDs[:]
        _current_process_list = Running_Current_Threads[:]
        _timestamp_list = Running_Finish_Timestamp[:]

        # assert len(set(_ppid_list)) == 1, f"The PPID of each process should be the same."
        # assert _ppid_list[0] == Running_Parent_PID, f"The PPID should equal to {Running_Parent_PID}. But it got {_ppid_list[0]}."
        assert len(_current_process_list) == Green_Thread_Size, f"The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_current_process_list)) == Green_Thread_Size, f"The count of PID (de-duplicate) should be the same as the count of processes."
        # assert len(_thread_id_list) == len(_current_process_list), f"The count of current process name (no de-duplicate) should be equal to count of PIDs."
        # assert len(set(_thread_id_list)) == len(set(_current_process_list)), f"The count of current process name (de-duplicate) should be equal to count of PIDs."

        _max_timestamp = max(_timestamp_list)
        _min_timestamp = min(_timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, f"Processes should be run in the same time period."


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_close(self, strategy: GreenThreadStrategy):
        # Test for no any parameters
        # process_strategy.close(self.__Processes)
        # _active_children_list = mp.active_children()
        # print(len(_active_children_list) == 0)
        # # assert len(_active_children_list) == 0, f"Processes should be closed finely."
        #
        # # Test for parameters with '*args'
        # process_strategy.close(self.__Processes_With_Args)
        # _active_children_list = mp.active_children()
        # print(len(_active_children_list) == 0)
        # # assert len(_active_children_list) == 0, f"Processes should be closed finely."
        #
        # # Test for parameters with '**kwargs'
        # process_strategy.close(self.__Processes_With_Kwargs)
        # _active_children_list = mp.active_children()
        # print(len(_active_children_list) == 0)
        # assert len(_active_children_list) == 0, f"Processes should be closed finely."
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_terminal(self, async_strategy: AsynchronousStrategy):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_kill(self, async_strategy: AsynchronousStrategy):
        pass


    @pytest.mark.skip(reason="Not implement. The result feature not finish.")
    def test_get_result(self, async_strategy: AsynchronousStrategy):
        pass


