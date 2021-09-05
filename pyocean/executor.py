from pyocean.framework.task import BaseQueueTask as _BaseQueueTask
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.executor import BaseExecutor
from pyocean.framework.strategy import (
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    Resultable as _Resultable)
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.mode import RunningMode as _RunningMode
from pyocean.adapter.strategy import ExecutorStrategyAdapter as _ExecutorStrategyAdapter
from pyocean.task import OceanPersistenceTask as _OceanPersistenceTask
from pyocean.persistence.interface import OceanPersistence as _OceanPersistence

from abc import ABC
from typing import List, Tuple, Dict, Optional, Union, List, Callable as CallableType, Iterable as IterableType, NewType
from types import MethodType, FunctionType
from collections import Iterable, Callable
from multipledispatch import dispatch
import inspect


_General_Runnable_Type = Union[_GeneralRunnableStrategy, _Resultable]
General_Runnable_Strategy: _General_Runnable_Type = None


class Executor(ABC, BaseExecutor):

    ParameterCannotBeNoneError = TypeError("It should not pass 'None' value parameter(s).")
    InvalidParameterBePass = TypeError("The parameters data type is invalid. It should all be tuple or dict.")

    def __init__(self, mode: _RunningMode, executors: int):
        super(Executor, self).__init__(mode=mode, executors=executors)
        # self._initial_running_strategy()


    def start_new_worker(self, target: Callable, *args, **kwargs) -> None:
        General_Runnable_Strategy.start_new_worker(target=target, *args, **kwargs)


    def run(self) -> None:
        pass


    def async_run(self) -> None:
        pass


    def map(self,
            function: CallableType,
            args_iter: IterableType = [],
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        General_Runnable_Strategy.initialization(queue_tasks=queue_tasks, features=features)
        __workers_list = [self._generate_worker(function, args) for args in args_iter]
        General_Runnable_Strategy.activate_workers(workers=__workers_list)
        General_Runnable_Strategy.close(workers=__workers_list)


    def async_map(self) -> None:
        pass


    def map_with_function(self,
                          functions: IterableType[Callable],
                          args_iter: IterableType = [],
                          queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                          features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        self.__chk_function_and_args(functions=functions, args_iter=args_iter)

        General_Runnable_Strategy.initialization(queue_tasks=queue_tasks, features=features)

        if args_iter is None or args_iter == []:
            args_iter = [() for _ in range(len(list(functions)))]

        __workers_list = []
        for fun, args in zip(functions, args_iter):
            print("CallableType: ", type(fun) is CallableType)
            print("MethodType: ", type(fun) is MethodType)
            print("FunctionType: ", type(fun) is FunctionType)
            print("fun: ", fun)
            print("args: ", args)
            __worker = self._generate_worker(fun, args)
            __workers_list.append(__worker)

        # __workers_list = [self.__generate_worker(fun, args) for fun, args in zip(functions, args_iter)]

        General_Runnable_Strategy.activate_workers(__workers_list)
        General_Runnable_Strategy.close(__workers_list)


    def terminal(self) -> None:
        General_Runnable_Strategy.terminal()


    def kill(self) -> None:
        General_Runnable_Strategy.kill()


    def result(self) -> List[_OceanResult]:
        return General_Runnable_Strategy.get_result()


    def __chk_args_content(self, args_iter: IterableType) -> List[Union[type, bool]]:
        """
        Description:
            The arguments only receive iterator of element which is
            tuple or dictionary object
        :param args_iter:
        :return:
        """

        if args_iter is None:
            raise self.ParameterCannotBeNoneError

        checksum_iter = map(lambda ele: type(ele) if (type(ele) is tuple or type(ele) is dict) else False, args_iter)
        checksum = all(checksum_iter)
        if checksum is False:
            raise self.InvalidParameterBePass
        return list(checksum_iter)


    @dispatch(MethodType, tuple)
    def _generate_worker(self, function: CallableType, args):
        __worker = General_Runnable_Strategy.generate_worker(function, *args)
        return __worker


    @dispatch(MethodType, dict)
    def _generate_worker(self, function: CallableType, args):
        __worker = General_Runnable_Strategy.generate_worker(function, **args)
        return __worker


    def __chk_function_and_args(self, functions: IterableType[Callable], args_iter: IterableType):
        if functions is None or args_iter is None:
            raise self.ParameterCannotBeNoneError

        self.__chk_args_content(args_iter=args_iter)
        self.__chk_fun_signature_and_param(functions=functions, args_iter=args_iter)


    def __chk_fun_signature_and_param(self, functions: IterableType[Callable], args_iter: IterableType) -> bool:
        for fun, args in zip(functions, args_iter):
            __fun_signature = inspect.signature(fun)
            __fun_parameter = __fun_signature.parameters
            if args != () and args != {} and len(__fun_parameter.keys()) != len(args):
                raise ValueError("The signature and parameter aren't mapping.")
        return True



class SimpleExecutor(Executor):

    def __init__(self, mode: _RunningMode, executors: int):
        super().__init__(mode=mode, executors=executors)
        self._initial_running_strategy()


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = _ExecutorStrategyAdapter(
            mode=self._mode,
            executors=self._executors_number)
        global General_Runnable_Strategy
        General_Runnable_Strategy = __running_strategy_adapter.get_simple()



class PersistenceExecutor(Executor):

    def __init__(self,
                 mode: _RunningMode,
                 executors: int,
                 persistence_strategy: _OceanPersistence,
                 db_connection_pool_size: int):
        super().__init__(mode=mode, executors=executors)
        self.persistence_strategy = persistence_strategy
        self.db_connection_pool_size = db_connection_pool_size
        self._initial_running_strategy()


    def _initial_running_strategy(self) -> None:
        __persistence_task = _OceanPersistenceTask()
        __persistence_task.strategy = self.persistence_strategy
        __persistence_task.connection_pool_size = self.db_connection_pool_size

        __running_strategy_adapter = _ExecutorStrategyAdapter(
            mode=self._mode,
            executors=self._executors_number)
        global General_Runnable_Strategy
        General_Runnable_Strategy = __running_strategy_adapter.get_persistence(persistence=__persistence_task)


