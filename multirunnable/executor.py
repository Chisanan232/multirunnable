from abc import ABC
from typing import Tuple, Dict, Optional, Union, List, Callable as CallableType, Iterable as IterableType
from collections.abc import Callable

from .framework import (
    BaseQueueTask as _BaseQueueTask,
    BaseExecutor as _BaseExecutor,
)
from .framework.runnable import (
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    Resultable as _Resultable,
    MRResult as _MRResult
)
from .framework.factory import (
    BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory,
    BaseList as _BaseList
)
from .mode import RunningMode as _RunningMode
from .factory.strategy import ExecutorStrategyAdapter as _ExecutorStrategyAdapter
from .types import MRTasks as _MRTasks
from ._config import set_mode
from ._utils import get_cls_name as _get_cls_name


_General_Runnable_Type = Union[_GeneralRunnableStrategy]
General_Runnable_Strategy: _General_Runnable_Type = None


class Executor(ABC, _BaseExecutor):

    ParameterCannotBeNoneError = TypeError("It should not pass 'None' value parameter(s).")
    InvalidParameterBePass = TypeError("The parameters data type is invalid. It should all be tuple or dict.")

    def __init__(self, executors: int):
        super(Executor, self).__init__(executors=executors)


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
        set_mode(mode=mode)
        self._mode = mode

        super().__init__(executors=executors)
        self._initial_running_strategy()


    def __repr__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(" \
                               f"mode={self._mode}, " \
                               f"worker_num={self._executors_number})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = _ExecutorStrategyAdapter(
            mode=self._mode,
            executors=self._executors_number)

        global General_Runnable_Strategy
        General_Runnable_Strategy = __running_strategy_adapter.get_simple()



class AdapterExecutor(Executor):

    def __init__(self, strategy: _General_Runnable_Type = None):
        super().__init__(executors=strategy.executors_number)
        self.__strategy = strategy
        self._initial_running_strategy()


    def _initial_running_strategy(self) -> None:
        global General_Runnable_Strategy
        General_Runnable_Strategy = self.__strategy

