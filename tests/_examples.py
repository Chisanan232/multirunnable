from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION, set_mode, get_current_mode
from multirunnable.mode import RunningMode
from multirunnable.adapter.context import context as _adapter_context
from multirunnable.factory import ExecutorStrategyAdapter, LockFactory, RLockFactory
from multirunnable.parallel.share import Global_Manager

from .test_config import (
    Worker_Size, Task_Size, Test_Function_Sleep_Time, Test_Function_Args, Test_Function_Kwargs, Test_Function_Multiple_Diff_Args
)

from typing import List, Tuple, Dict, Callable, Any
import multiprocessing as mp
import threading
import asyncio
import gevent.lock
import gevent.threading
import time
import os


_Worker_Size = Worker_Size

# # Some Global variables which are the flags to let testing items check
Running_Count = Global_Manager.Value(int, 0)
Running_Workers_IDs: List = Global_Manager.list()
Running_PPIDs: List = Global_Manager.list()
Running_Current_Workers: List = Global_Manager.list()
Running_Finish_Timestamp: List = Global_Manager.list()

_Worker_Lock = None
_Worker_RLock = None


def reset_running_flags() -> None:
    """
    Reset all flags it has to check.

    :return:
    """

    global Running_Count, Running_Workers_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp
    Running_Count.value = 0
    Running_Workers_IDs[:] = []
    Running_PPIDs[:] = []
    Running_Current_Workers[:] = []
    Running_Finish_Timestamp[:] = []


def get_running_cnt() -> int:
    return Running_Count.value


def get_running_workers_ids() -> List:
    return Running_Workers_IDs


def get_running_ppids() -> List:
    return Running_PPIDs


def get_current_workers() -> List:
    return Running_Current_Workers


def get_running_done_timestamps() -> List:
    return Running_Finish_Timestamp


def initial_lock(use_adapter_factory: bool = False):
    """
    Instantiate Lock object. It would initial via context of multirunnable if
    option *use_adapter_factory* is True, or it  would initial by their own native
    library or third party library.

    :param use_adapter_factory:
    :return:
    """

    global _Worker_Lock

    _rmode = get_current_mode(force=True)

    if use_adapter_factory is True:
        _lock_factory = LockFactory()
        _lock_factory.feature_mode = _rmode.value["feature"]
        _Worker_Lock = _lock_factory.get_instance()
    else:
        if _rmode is RunningMode.Parallel:
            _Worker_Lock = mp.Lock()
        elif _rmode is RunningMode.Concurrent:
            _Worker_Lock = threading.Lock()
        elif _rmode is RunningMode.GreenThread:
            _Worker_Lock = gevent.threading.Lock()
        elif _rmode is RunningMode.Asynchronous:
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) >= (3, 10):
                _Worker_Lock = asyncio.locks.Lock()
            else:
                _Worker_Lock = asyncio.locks.Lock(loop=asyncio.get_event_loop())
                # _Worker_Lock = asyncio.locks.Lock()
        else:
            raise ValueError("The RunningMode has the unexpected mode.")

    return _Worker_Lock


def set_lock(lock) -> None:
    global _Worker_Lock
    _Worker_Lock = lock


def initial_rlock(use_adapter_factory: bool = False):
    """
    It's same as function 'initial_lock' but this function instantiates RLock object.

    :param use_adapter_factory:
    :return:
    """

    global _Worker_RLock

    _rmode = get_current_mode(force=True)

    if use_adapter_factory is True:
        _rlock_factory = RLockFactory()
        _rlock_factory.feature_mode = _rmode.value["feature"]
        _Worker_RLock = _rlock_factory.get_instance()
    else:
        if _rmode is RunningMode.Parallel:
            _Worker_RLock = mp.RLock()
        elif _rmode is RunningMode.Concurrent:
            _Worker_RLock = threading.RLock()
        elif _rmode is RunningMode.GreenThread:
            _Worker_RLock = gevent.lock.RLock()
        else:
            raise ValueError("The RunningMode has the unexpected mode.")

    return _Worker_RLock


def initial_async_event_loop() -> None:
    _event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop=_event_loop)


def set_rlock(rlock) -> None:
    global _Worker_RLock
    _Worker_RLock = rlock


def _get_current_worker(use_adapter_context: bool = False) -> Any:
    """
    Get current worker instance.

    :param use_adapter_context:
    :return:
    """

    _rmode = get_current_mode(force=True)

    if use_adapter_context is True:
        _current_worker = _adapter_context.get_current_worker()
    else:
        if _rmode is RunningMode.Parallel:
            _current_worker = mp.current_process()
        elif _rmode is RunningMode.Concurrent:
            _current_worker = threading.current_thread()
        elif _rmode is RunningMode.GreenThread:
            _current_worker = gevent.threading.getcurrent()
        elif _rmode is RunningMode.Asynchronous:
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _current_worker = asyncio.current_task()
            else:
                _current_worker = asyncio.Task.current_task()
        else:
            raise ValueError("The RunningMode has the unexpected mode.")

    return _current_worker


def _get_worker_id(use_adapter_context: bool = False) -> str:
    """
    Get the identity of current worker instance.

    :param use_adapter_context:
    :return:
    """

    _rmode = get_current_mode(force=True)

    if use_adapter_context is True:
        _worker_id = _adapter_context.get_current_worker_ident()
    else:
        if _rmode is RunningMode.Parallel:
            _worker_id = mp.current_process().ident
        elif _rmode is RunningMode.Concurrent:
            _worker_id = threading.current_thread().ident
        elif _rmode is RunningMode.GreenThread:
            _worker_id = gevent.threading.get_ident()
        elif _rmode is RunningMode.Asynchronous:
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _worker_id = id(asyncio.current_task())
            else:
                _worker_id = id(asyncio.Task.current_task())
        else:
            raise ValueError("The RunningMode has the unexpected mode.")

    return str(_worker_id)


def _sleep_time() -> None:
    """
    Sleep by the RunningMode.

    :return:
    """

    _rmode = get_current_mode(force=True)

    if _rmode is RunningMode.Asynchronous:
        raise RuntimeError("This function doesn't support 'RunningMode.Asynchronous'.")

    if _rmode is RunningMode.Parallel or _rmode is RunningMode.Concurrent:
        time.sleep(Test_Function_Sleep_Time)
    elif _rmode is RunningMode.GreenThread:
        gevent.sleep(Test_Function_Sleep_Time)
    else:
        raise ValueError("The RunningMode has the unexpected mode.")


class RunByStrategy:

    @staticmethod
    def Parallel(_function):
        set_mode(mode=RunningMode.Parallel)

        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Parallel, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()

        RunByStrategy._run_with_multiple_workers(_strategy, _function)


    @staticmethod
    def Concurrent(_function):
        set_mode(mode=RunningMode.Concurrent)

        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Concurrent, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()

        RunByStrategy._run_with_multiple_workers(_strategy, _function)


    @staticmethod
    def CoroutineWithGreenThread(_function):
        set_mode(mode=RunningMode.GreenThread)

        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.GreenThread, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()

        RunByStrategy._run_with_multiple_workers(_strategy, _function)


    @staticmethod
    def CoroutineWithAsynchronous(_function, event_loop=None, _feature=None):
        set_mode(mode=RunningMode.Asynchronous)

        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()

        async def __process():
            await _strategy.initialization(queue_tasks=None, features=_feature, event_loop=event_loop)
            _ps = [_strategy.generate_worker(_function) for _ in range(_Worker_Size)]
            await _strategy.activate_workers(_ps)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__process())


    @staticmethod
    def _run_with_multiple_workers(_strategy, _function):
        _ps = [_strategy.generate_worker(_function) for _ in range(_Worker_Size)]
        _strategy.activate_workers(_ps)
        _strategy.close(_ps)



class MapByStrategy:

    @staticmethod
    def Parallel(_functions: List):
        set_mode(mode=RunningMode.Parallel)

        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Parallel, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()

        MapByStrategy._map_with_multiple_workers(_strategy, _functions)


    @staticmethod
    def Concurrent(_functions: List):
        set_mode(mode=RunningMode.Concurrent)

        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Concurrent, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()

        MapByStrategy._map_with_multiple_workers(_strategy, _functions)


    @staticmethod
    def CoroutineWithGreenThread(_functions: List):
        set_mode(mode=RunningMode.GreenThread)

        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.GreenThread, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()

        MapByStrategy._map_with_multiple_workers(_strategy, _functions)


    @staticmethod
    def CoroutineWithAsynchronous(_functions: List, _feature=None):
        set_mode(mode=RunningMode.Asynchronous)

        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()
        _strategy.map_with_function(functions=_functions, features=_feature)


    @staticmethod
    def _map_with_multiple_workers(_strategy, _functions: List):
        _ps = [_strategy.generate_worker(_f) for _f in _functions]
        _strategy.activate_workers(_ps)
        _strategy.close(_ps)


"""
Target functions or methods in class
"""


def __record_info_to_flags() -> str:
    _pid = os.getpid()
    _ppid = os.getppid()
    _ident = _get_worker_id()
    _current_worker = _get_current_worker()
    _time = int(time.time())

    Running_Workers_IDs.append(_ident)
    Running_PPIDs.append(_ppid)
    Running_Current_Workers.append(str(_current_worker))
    Running_Finish_Timestamp.append(_time)

    return str(_ident)


def target_function(*args, **kwargs) -> str:
    global Running_Count, Running_Workers_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp

    with _Worker_Lock:
        Running_Count.value += 1

        if args:
            assert args == Test_Function_Args, "The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, "The argument *kwargs* should be same as the input outside."

        _ident = __record_info_to_flags()

    _sleep_time()
    return f"result_{_ident}"


def target_error_function(*args, **kwargs) -> None:
    raise Exception("Testing result raising an exception.")


def target_function_for_map(*args, **kwargs) -> str:
    """
    Description:
        Test for 'map', 'starmap' methods.
    :param args:
    :param kwargs:
    :return:
    """
    global Running_Count, Running_Workers_IDs, Running_PPIDs, Running_Current_Workers, Running_Finish_Timestamp

    with _Worker_Lock:
        Running_Count.value += 1

        if args:
            assert set(args) <= set(Test_Function_Args), "The argument *args* should be one of element of the input outside."
            if len(args) > 1:
                assert args == Test_Function_Args, "The argument *args* should be same as the global variable 'Test_Function_Args'."
        if kwargs:
            assert kwargs is None or kwargs == {}, "The argument *kwargs* should be empty or None value."

        _ident = __record_info_to_flags()

    _sleep_time()
    return f"result_{_ident}"


def target_function_for_map_with_diff_args(*args, **kwargs):
    """
    Description:
        Test for 'map', 'starmap' methods.
    :param args:
    :param kwargs:
    :return:
    """
    global Running_Count

    with _Worker_Lock:
        Running_Count.value += 1

        if args:
            assert {args} <= set(Test_Function_Multiple_Diff_Args), "The argument *args* should be one of element of the input outside."
            # if len(args) > 1:
            #     assert args == Test_Function_Args, "The argument *args* should be same as the global variable 'Test_Function_Args'."
        if kwargs:
            assert kwargs is None or kwargs == {}, "The argument *kwargs* should be empty or None value."

        _ident = __record_info_to_flags()

    gevent.sleep(Test_Function_Sleep_Time)
    return f"result_{_ident}"


async def target_async_function(*args, **kwargs) -> str:
    global Running_Count

    async with _Worker_Lock:
        Running_Count.value += 1

        if args:
            assert args == Test_Function_Args, "The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, "The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            _current_task = asyncio.current_task(loop=asyncio.get_event_loop())
        else:
            _current_task = asyncio.Task.current_task(loop=asyncio.get_event_loop())
        _time = int(time.time())

        Running_PPIDs.append(_ppid)
        Running_Current_Workers.append(str(id(_current_task)))
        Running_Finish_Timestamp.append(_time)

    await asyncio.sleep(Test_Function_Sleep_Time)
    return f"result_{id(_current_task)}"


def target_funcs_iter() -> List:
    return [target_function for _ in range(Task_Size)]


def target_methods_iter() -> List[Callable]:
    _ts = TargetCls()
    return [_ts.method for _ in range(Task_Size)]


def target_classmethods_iter() -> List[Callable]:
    return [TargetCls.classmethod_fun for _ in range(Task_Size)]


def target_staticmethods_iter() -> List[Callable]:
    return [TargetCls.staticmethod_fun for _ in range(Task_Size)]


def target_func_args_iter() -> List[Tuple]:
    return [Test_Function_Args for _ in range(Task_Size)]


def target_funcs_kwargs_iter() -> List[Dict]:
    return [Test_Function_Kwargs for _ in range(Task_Size)]


class TargetCls:

    def method(self, *args, **kwargs) -> None:
        target_function(*args, **kwargs)


    @classmethod
    def classmethod_fun(cls, *args, **kwargs) -> None:
        target_function(*args, **kwargs)


    @staticmethod
    def staticmethod_fun(*args, **kwargs) -> None:
        target_function(*args, **kwargs)



class TargetMapCls:

    def method(self, *args, **kwargs) -> None:
        target_function_for_map(*args, **kwargs)


    @classmethod
    def classmethod_fun(cls, *args, **kwargs) -> None:
        target_function_for_map(*args, **kwargs)


    @staticmethod
    def staticmethod_fun(*args, **kwargs) -> None:
        target_function_for_map(*args, **kwargs)


class TargetAsyncCls:

    async def method(self, *args, **kwargs) -> None:
        await target_async_function(*args, **kwargs)


    @classmethod
    async def classmethod_fun(cls, *args, **kwargs) -> None:
        await target_async_function(*args, **kwargs)


    @staticmethod
    async def staticmethod_fun(*args, **kwargs) -> None:
        await target_async_function(*args, **kwargs)

