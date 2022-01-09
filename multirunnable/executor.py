from abc import ABC
from typing import Tuple, Dict, Optional, Union, List, Callable as CallableType, Iterable as IterableType, NewType
from collections.abc import Callable

from .framework import (
    BaseList as _BaseList,
    BaseQueueTask as _BaseQueueTask,
    BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory,
    BaseExecutor as _BaseExecutor,
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    Resultable as _Resultable,
    MRResult as _MRResult
)
from .mode import RunningMode as _RunningMode
from .adapter.strategy import ExecutorStrategyAdapter as _ExecutorStrategyAdapter
from .types import MRTasks as _MRTasks
from ._config import set_mode


_General_Runnable_Type = Union[_GeneralRunnableStrategy]
General_Runnable_Strategy: _General_Runnable_Type = None


class Executor(ABC, _BaseExecutor):

    ParameterCannotBeNoneError = TypeError("It should not pass 'None' value parameter(s).")
    InvalidParameterBePass = TypeError("The parameters data type is invalid. It should all be tuple or dict.")

    def __init__(self, mode: _RunningMode, executors: int):
        super(Executor, self).__init__(mode=mode, executors=executors)
        set_mode(mode=mode)


    def start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}):
        _worker = General_Runnable_Strategy.start_new_worker(target, args=args, kwargs=kwargs)
        return _worker


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


    def close(self, workers: Union[_MRTasks, List[_MRTasks]]) -> None:
        General_Runnable_Strategy.close(workers)


    def terminal(self) -> None:
        General_Runnable_Strategy.terminal()


    def kill(self) -> None:
        General_Runnable_Strategy.kill()


    def result(self) -> List[_MRResult]:
        if isinstance(General_Runnable_Strategy, _Resultable):
            return General_Runnable_Strategy.get_result()
        else:
            raise ValueError("This running strategy isn't a Resultable object.")



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



class AdapterExecutor(Executor):

    def __init__(self, strategy: _General_Runnable_Type = None):
        super().__init__(mode=None, executors=strategy.executors_number)
        self.__strategy = strategy
        self._initial_running_strategy()


    def _initial_running_strategy(self) -> None:
        global General_Runnable_Strategy
        General_Runnable_Strategy = self.__strategy

