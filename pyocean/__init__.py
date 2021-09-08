"""
Set the customized Python package to Python Interpreter Environment Variable Path  so that we could import it if we need.
"""

from functools import wraps
from logging import getLogger
from typing import Tuple, Dict, Union
from types import FunctionType, MethodType
import getpass
import pathlib
import sys

# # Import pyocean package
__package_pyocean_path = str(pathlib.Path(__file__).parent.absolute())
sys.path.append(__package_pyocean_path)

# # Configure logging setting
__user = getpass.getuser()
PYOCEAN_LOGGER = getLogger(__user)


from pyocean.mode import RunningMode, FeatureMode
from pyocean.task import OceanTask, QueueTask
from pyocean.executor import SimpleExecutor, PersistenceExecutor
from pyocean.pool import SimplePool, PersistencePool
from pyocean.manager import (
    OceanSimpleManager,
    OceanPersistenceManager,
    OceanSimpleAsyncManager,
    OceanPersistenceAsyncManager)
from pyocean.system import OceanSystem



def multi_processes(processes: int):

    def __target(function: Union[FunctionType, MethodType]):

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


