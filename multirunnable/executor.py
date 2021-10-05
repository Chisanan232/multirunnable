from multirunnable.framework.task import BaseQueueTask as _BaseQueueTask
from multirunnable.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from multirunnable.framework.adapter.collection import BaseList as _BaseList
from multirunnable.framework.executor import BaseExecutor
from multirunnable.framework.strategy import GeneralRunnableStrategy as _GeneralRunnableStrategy
from multirunnable.framework.result import OceanResult as _OceanResult
from multirunnable.mode import RunningMode as _RunningMode
from multirunnable.adapter.strategy import ExecutorStrategyAdapter as _ExecutorStrategyAdapter
from multirunnable.task import OceanPersistenceTask as _OceanPersistenceTask
from multirunnable.persistence.interface import OceanPersistence as _OceanPersistence
from multirunnable._config import set_mode

from abc import ABC
from typing import Tuple, Dict, Optional, Union, List, Callable as CallableType, Iterable as IterableType, NewType
from collections import Iterable, Callable


_General_Runnable_Type = Union[_GeneralRunnableStrategy]
General_Runnable_Strategy: _General_Runnable_Type = None


class Executor(ABC, BaseExecutor):

    ParameterCannotBeNoneError = TypeError("It should not pass 'None' value parameter(s).")
    InvalidParameterBePass = TypeError("The parameters data type is invalid. It should all be tuple or dict.")

    def __init__(self, mode: _RunningMode, executors: int):
        super(Executor, self).__init__(mode=mode, executors=executors)
        set_mode(mode=mode)


    def start_new_worker(self, target: Callable, *args, **kwargs) -> None:
        General_Runnable_Strategy.start_new_worker(target=target, *args, **kwargs)


    def run(self,
            function: CallableType,
            args: Optional[Union[Tuple, Dict]] = None,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        General_Runnable_Strategy.run(
            function=function,
            args=args,
            queue_tasks=queue_tasks,
            features=features)


    # def async_run(self,
    #               function: CallableType,
    #               args_iter: IterableType = [],
    #               queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
    #               features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
    #     pass


    def map(self,
            function: CallableType,
            args_iter: IterableType = [],
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        General_Runnable_Strategy.map(
            function=function,
            args_iter=args_iter,
            queue_tasks=queue_tasks,
            features=features)


    # def async_map(self) -> None:
    #     pass


    def map_with_function(self,
                          functions: IterableType[Callable],
                          args_iter: IterableType = [],
                          queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                          features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        General_Runnable_Strategy.map_with_function(
            functions=functions,
            args_iter=args_iter,
            queue_tasks=queue_tasks,
            features=features)


    def terminal(self) -> None:
        General_Runnable_Strategy.terminal()


    def kill(self) -> None:
        General_Runnable_Strategy.kill()


    def result(self) -> List[_OceanResult]:
        return General_Runnable_Strategy.get_result()



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



class AdapterExecutor(Executor):

    def __init__(self, strategy: _General_Runnable_Type = None):
        super().__init__(mode=None, executors=strategy.executors_number)
        self.__strategy = strategy
        self._initial_running_strategy()


    def _initial_running_strategy(self) -> None:
        global General_Runnable_Strategy
        General_Runnable_Strategy = self.__strategy

