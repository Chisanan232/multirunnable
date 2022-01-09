from multirunnable.coroutine.strategy import CoroutineStrategy, GreenThreadStrategy, GreenThreadPoolStrategy, AsynchronousStrategy
from multirunnable.coroutine.result import CoroutineResult, GreenThreadPoolResult
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

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
import sys
import os
import re


Green_Thread_Size: int = Worker_Size
Pool_Size: int = Worker_Pool_Size
Task_Size: int = Task_Size

Running_Diff_Time: int = Running_Diff_Time

_GreenThread_Lock = GeventLock()
if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION == 10:
    _Async_Lock = AsyncLock()
else:
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
    return f"result_{_ident}"


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
    return f"result_{_ident}"


def target_error_fun(*args, **kwargs) -> str:
    raise Exception("Testing result raising an exception.")


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
    return f"result_{_ident}"


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
    return f"result_{_ident}"


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
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            _current_task = asyncio.current_task(loop=asyncio.get_event_loop())
        else:
            _current_task = asyncio.Task.current_task(loop=asyncio.get_event_loop())
        # _async_task_name = _current_task.get_name()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        # Running_GreenThread_IDs.append(_async_task_name)
        Running_PPIDs.append(_ppid)
        Running_Current_Threads.append(_current_task)
        Running_Finish_Timestamp.append(_time)

    # await async_sleep(Test_Function_Sleep_Time)
    await asyncio.sleep(Test_Function_Sleep_Time)
    return f"result_{id(_current_task)}"


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


_Generate_Worker_Error_Msg = f"" \
                             f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


class TestGreenThread(GeneralRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_initialization(self, strategy: GreenThreadStrategy):
        pass


    def test_start_new_worker_with_function_with_no_argument(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_function_with_args(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun,
            args=Test_Function_Args)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun,
            kwargs=Test_Function_Kwargs)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_no_argument(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_args(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            args=Test_Function_Args)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_kwargs(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_args(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_args(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_generate_worker_with_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # Test for no any parameters
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_function_with_args(self, strategy: GreenThreadStrategy):
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for no any parameters
        _tc = TargetCls()
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_args(self, strategy: GreenThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '*args'
        _tc = TargetCls()
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '**kwargs'
        _tc = TargetCls()
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for no any parameters
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_args(self, strategy: GreenThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for no any parameters
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_args(self, strategy: GreenThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def _chk_worker_instance_type(self, _thread) -> bool:
        return isinstance(_thread, gevent.Greenlet)


    def test_activate_workers_with_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_function_with_args(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_bounded_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_bounded_function_with_args(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_bounded_function_with_kwargs(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_classmethod_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_classmethod_function_with_args(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_classmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_staticmethod_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_staticmethod_function_with_args(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_staticmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_get_success_result(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_fun,
            args=Test_Function_Args)

        _result = strategy.get_result()
        assert _result is not None and _result != [], f"The running result should not be empty."
        assert type(_result) is list, f"The result should be a list type object."
        for _r in _result:
            assert isinstance(_r, CoroutineResult) is True, f"The element of result should be instance of object 'ConcurrentResult'."
            assert _r.pid, f"The PID should exists in list we record."
            assert _r.worker_name, f"It should have thread name."
            assert _r.worker_ident, f"It should have thread identity."
            # assert _r.loop, f""
            assert _r.parent, f""
            assert _r.args is not None, f""
            assert _r.kwargs is not None, f""
            assert _r.data == f"result_{_r.worker_ident}", f"Its data should be same as we expect 'result_{_r.pid}'."
            assert _r.state == "successful", f"Its state should be 'successful'."
            assert _r.exception is None, f"It should have nothing exception."


    # @pytest.mark.skip(reason="Consider this feature.")
    def test_get_failure_result(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_error_fun)

        _result = strategy.get_result()
        assert _result is not None and _result != [], f""
        assert type(_result) is list, f""
        for _r in _result:
            assert isinstance(_r, CoroutineResult) is True, f""
            assert _r.pid, f"It should have PID."
            assert _r.worker_name, f"It should have thread name."
            assert _r.worker_ident, f"It should have thread identity."
            # assert _r.loop, f""
            assert _r.parent, f""
            assert _r.args is not None, f""
            assert _r.kwargs is not None, f""
            assert _r.data is None, f"Its data should be None."
            assert _r.state == "fail", f"Its state should be 'fail'."
            print(f"[DEBUG] _r.exception: {_r.exception}")
            assert isinstance(_r.exception, Exception) and "Testing result raising an exception" in str(_r.exception), f"It should have an exception and error message is 'Testing result raising an exception'."


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


    def _initial(self):
        # Test for parameters with '**kwargs'
        reset_running_flag()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_record():
        GeneralRunningTestSpec._chk_process_record(
            running_cnt=Running_Count,
            worker_size=Green_Thread_Size,
            running_wokrer_ids=Running_GreenThread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp
        )



class TestGreenThreadPool(PoolRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_initialization(self, pool_strategy: GreenThreadPoolStrategy):
        pass


    def test_apply_with_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=pool_target_fun)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=pool_target_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=pool_target_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetPoolCls()
        self._apply(strategy=pool_strategy, target_fun=_tc.method)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetPoolCls()
        self._apply(strategy=pool_strategy, target_fun=_tc.method, args=Test_Function_Args)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetPoolCls()
        self._apply(strategy=pool_strategy, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_blocking_record()


    def test_async_apply_with_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=pool_target_fun)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=pool_strategy, target_fun=pool_target_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=pool_strategy, target_fun=pool_target_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_bounded_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetPoolCls()
        self._async_apply(strategy=pool_strategy, target_fun=_tc.method)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_bounded_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        _tc = TargetPoolCls()
        self._async_apply(strategy=pool_strategy, target_fun=_tc.method, args=Test_Function_Args)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_bounded_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        _tc = TargetPoolCls()
        self._async_apply(strategy=pool_strategy, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_classmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_classmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_classmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_record()


    def test_map_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map(function=target_fun, args_iter=Test_Function_Args)


    def test_map_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._map(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._async_map(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_by_args_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()

        self._map_by_args(strategy=pool_strategy, target_fun=map_target_fun_with_diff_args, args_iter=Test_Function_Multiple_Diff_Args)

        TestGreenThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_map_by_args_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._map_by_args(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_by_args_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_by_args_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_by_args_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()

        self._async_map_by_args(strategy=pool_strategy, target_fun=map_target_fun_with_diff_args, args_iter=Test_Function_Multiple_Diff_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_by_args_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._async_map_by_args(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_by_args_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_by_args_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetPoolMapCls()
        self._imap(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_unordered_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_unordered_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetPoolMapCls()
        self._imap_unordered(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_unordered_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_unordered_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_get_success_result_with_async_apply(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=pool_target_fun)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    @pytest.mark.skip(reason="Still consider about this feature.")
    def test_get_failure_result_with_async_apply(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=target_error_fun)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_failure_result(results=_results)


    def test_get_success_result_with_map(self, pool_strategy: GreenThreadPoolStrategy):
        self._map(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_async_map(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_map(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_map_by_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._map_by_args(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_async_map_by_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_map_by_args(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap_unordered(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


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


    def _initial(self):
        # Test for parameters with '**kwargs'
        reset_pool_running_value()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_blocking_record():
        PoolRunningTestSpec._chk_process_record_blocking(
            pool_running_cnt=Pool_Running_Count,
            worker_size=Pool_Size,
            running_worker_ids=Running_GreenThread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    @staticmethod
    def _chk_record():
        PoolRunningTestSpec._chk_process_record(
            pool_running_cnt=Pool_Running_Count,
            worker_size=Green_Thread_Size,
            running_worker_ids=Running_GreenThread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    @staticmethod
    def _chk_map_record():
        PoolRunningTestSpec._chk_process_record_map(
            pool_running_cnt=Pool_Running_Count,
            function_args=Test_Function_Args,
            running_worker_ids=Running_GreenThread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp
        )


_Async_Generate_Worker_Error_Msg = \
    f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


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
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=target_async_fun,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_function_with_args(self, async_strategy: AsynchronousStrategy):
        # Test for parameters with '*args'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=target_async_fun,
                args=Test_Function_Args,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # Test for parameters with '**kwargs'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=target_async_fun,
                kwargs=Test_Function_Kwargs,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_bounded_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is bounded function.
        # Test for no any parameters
        async def __chk_type():
            _tc = TargetAsyncCls()
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=_tc.method,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_bounded_function_with_args(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '*args'
        async def __chk_type():
            _tc = TargetAsyncCls()
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=_tc.method,
                args=Test_Function_Args,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_bounded_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '**kwargs'
        async def __chk_type():
            _tc = TargetAsyncCls()
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=_tc.method,
                kwargs=Test_Function_Kwargs,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_classmethod_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is classmethod function.
        # Test for no any parameters
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.classmethod_fun,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_classmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '*args'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.classmethod_fun,
                args=Test_Function_Args,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_classmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '**kwargs'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.classmethod_fun,
                kwargs=Test_Function_Kwargs,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_staticmethod_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is staticmethod function.
        # Test for no any parameters
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.staticmethod_fun,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_staticmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '*args'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.staticmethod_fun,
                args=Test_Function_Args,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_staticmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '**kwargs'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.staticmethod_fun,
                kwargs=Test_Function_Kwargs,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def _chk_worker_instance_type(self, _thread) -> bool:
        return isinstance(_thread, asyncio.Task)


    def test_activate_workers_with_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_fun) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_function_with_args(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_bounded_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            _tc = TargetAsyncCls()
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(_tc.method) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_bounded_function_with_args(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            _tc = TargetAsyncCls()
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(_tc.method, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_bounded_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            _tc = TargetAsyncCls()
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(_tc.method, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_classmethod_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_classmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_classmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_staticmethod_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_staticmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def test_activate_workers_with_staticmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()


    def _initial(self):
        # Test for parameters with '**kwargs'
        reset_running_flag()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_async_task_record():
        GeneralRunningTestSpec._chk_running_cnt(running_cnt=Running_Count, worker_size=Green_Thread_Size)

        _current_process_list = Running_Current_Threads[:]
        assert len(_current_process_list) == Green_Thread_Size, f"The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_current_process_list)) == Green_Thread_Size, f"The count of PID (de-duplicate) should be the same as the count of processes."

        GeneralRunningTestSpec._chk_done_timestamp(timestamp_list=Running_Finish_Timestamp[:])


    def test_get_async_result(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        _result = async_strategy.get_result()
        for _r in _result:
            assert _r.data, f""
            _chksum = re.search(r"result_[0-9]{1,64}", str(_r.data))
            assert _chksum is not None, f""


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


