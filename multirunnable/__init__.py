#    This is a Python package which integrates APIs of parallel (multiprocessing),
#    concurrent (threading) and coroutine (gevent, asyncio).
#
#     __  ___      ____  _ ____                          __    __   
#    /  |/  /_  __/ / /_(_) __ \__  ______  ____  ____ _/ /_  / /__ 
#   / /|_/ / / / / / __/ / /_/ / / / / __ \/ __ \/ __ `/ __ \/ / _ \
#  / /  / / /_/ / / /_/ / _, _/ /_/ / / / / / / / /_/ / /_/ / /  __/
# /_/  /_/\__,_/_/\__/_/_/ |_|\__,_/_/ /_/_/ /_/\__,_/_.___/_/\___/ 
#


"""
Set the customized Python package to Python Interpreter Environment Variable Path  so that we could import it if we need.
"""

from sys import version_info
from types import FunctionType, MethodType
from typing import Tuple, Dict, Union
from functools import wraps

PYTHON_MAJOR_VERSION = int(version_info.major)
if PYTHON_MAJOR_VERSION < 3:
    from .exceptions import VersionError
    raise VersionError
PYTHON_MINOR_VERSION = int(version_info.minor)
PYTHON_VERSION = f"{PYTHON_MAJOR_VERSION}.{PYTHON_MINOR_VERSION}"

from multirunnable.__pkg_info__ import __version__, __github_tag_version__
from multirunnable.mode import RunningMode, FeatureMode
from multirunnable.tasks import QueueTask
from multirunnable.executor import SimpleExecutor
from multirunnable.pool import SimplePool
from multirunnable._import_utils import ImportMultiRunnable as _ImportMultiRunnable
from multirunnable._config import set_mode, get_current_mode



def multi_processes(processes: int):

    def __target(function: Union[FunctionType, MethodType]):

        @wraps(function)
        def _(*args, **kwargs):
            __result = __running(
                mode=RunningMode.Parallel,
                executors=processes,
                function=function,
                fun_args=args,
                fun_kwargs=kwargs)
            return __result

        return _

    return __target



def multi_threads(threads: int):

    def __target(function: Union[FunctionType, MethodType]):

        @wraps(function)
        def _(*args, **kwargs):
            __result = __running(
                mode=RunningMode.Concurrent,
                executors=threads,
                function=function,
                fun_args=args,
                fun_kwargs=kwargs)
            return __result

        return _

    return __target



def multi_green_threads(gthreads: int):

    def __target(function: Union[FunctionType, MethodType]):

        @wraps(function)
        def _(*args, **kwargs):
            __result = __running(
                mode=RunningMode.GreenThread,
                executors=gthreads,
                function=function,
                fun_args=args,
                fun_kwargs=kwargs)
            return __result

        return _

    return __target



def multi_executors(mode: RunningMode, executors: int):

    def __target(function: Union[FunctionType, MethodType]):

        @wraps(function)
        def _(*args, **kwargs):
            __result = __running(
                mode=mode,
                executors=executors,
                function=function,
                fun_args=args,
                fun_kwargs=kwargs)
            return __result

        return _

    return __target



def __running(mode: RunningMode, executors: int,
              function: Union[FunctionType, MethodType],
              fun_args: Tuple = (), fun_kwargs: Dict = {}):
    # # Handle parameters
    __args = ()
    if fun_args:
        __args = fun_args
    elif fun_kwargs:
        __args = tuple(fun_kwargs.values())

    # # Initial and run executor (executors)
    __executor = SimpleExecutor(mode=mode, executors=executors)
    __executor.run(function=function, args=__args)
    __result = __executor.result()
    return __result



def asynchronize(function: Union[FunctionType, MethodType]):

    @wraps(function)
    async def _(*args, **kwargs):
        value = function(*args, **kwargs)
        return value

    return _



def sleep(seconds: float, mode: RunningMode = None, **kwargs) -> None:
    import asyncio

    if mode is None:
        from multirunnable._config import get_current_mode
        mode = get_current_mode()

    if mode is RunningMode.Asynchronous:
        raise TypeError("It doesn't accept 'Asynchronous' running mode in this function.")

    def __get_instn():
        __cls = _ImportMultiRunnable.get_class(pkg_path=".coroutine.utils", cls_name=f"{mode.value.get('class_key')}Waiter")
        __instance = __cls()
        return __instance

    def __sleep(instance, param: Dict) -> None:
        instance.sleep(**param)

    async def __await_sleep(instance, param: Dict) -> None:
        await instance.sleep(**param)

    if mode is RunningMode.GreenThread:
        __seconds = int(seconds)
        __ref = kwargs.get("ref", True)
        __param = {"seconds": __seconds, "ref": __ref}

        __waiter_instance = __get_instn()
        __sleep(instance=__waiter_instance, param=__param)
    elif mode is RunningMode.Asynchronous:
        __seconds = seconds
        __result = kwargs.get("result", None)
        __loop = kwargs.get("loop", None)
        __param = {"delay": __seconds, "result": __result, "loop": __loop}

        __waiter_instance = __get_instn()
        # # # Not finish yet
        # __current_running_loop = asyncio.get_running_loop()
        # if __current_running_loop is None:
        #     raise RuntimeError("It should be used in coroutine function.")
        # asyncio.run(__await_sleep(instance=__waiter_instance, param=__param))
    else:
        import time
        time.sleep(seconds)



async def async_sleep(seconds: float, **kwargs) -> None:
    from multirunnable._config import RUNNING_MODE
    mode = RUNNING_MODE

    if mode is not RunningMode.Asynchronous:
        raise TypeError("It only accept 'Asynchronous' running mode in async function.")

    def __get_instn():
        __cls = _ImportMultiRunnable.get_class(pkg_path=".coroutine.utils", cls_name=f"{mode.value.get('class_key')}Waiter")
        __instance = __cls()
        return __instance

    async def __await_sleep(instance, param: Dict) -> None:
        await instance.sleep(**param)

    __seconds = seconds
    __result = kwargs.get("result", None)
    __loop = kwargs.get("loop", None)
    __param = {"delay": __seconds, "result": __result, "loop": __loop}

    __waiter_instance = __get_instn()
    await __await_sleep(instance=__waiter_instance, param=__param)


