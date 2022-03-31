from collections.abc import Callable
from typing import List, Tuple, Dict, Optional, Union, Callable as CallableType, Iterable as IterableType
from abc import ABCMeta, abstractmethod

from .runnable.result import MRResult as _MRResult
from .factory import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory, BaseList as _BaseList
from .task import BaseQueueTask as _BaseQueueTask
from ..types import MRTasks as _MRTasks



class BaseExecutor(metaclass=ABCMeta):

    def __init__(self, executors: int):
        self._executors_number = executors


    def __str__(self):
        return f"{self.__str__()} at {id(self.__class__)}"


    @abstractmethod
    def _initial_running_strategy(self) -> None:
        """
        Description:
            Initialize and instantiate RunningStrategy.
        :return:
        """
        pass


    @abstractmethod
    def start_new_worker(self, target: Callable, *args, **kwargs) -> None:
        """
        Description:
            Initial and activate an executor to run.
        :param target:
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def run(self, function: CallableType, args: Optional[Union[Tuple, Dict]] = None,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        pass


    @abstractmethod
    def map(self, function: CallableType, args_iter: IterableType = [],
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        """
        Description:
            Receive a parameters (the arguments of target function) List
            object and distribute them to
            1. Multiple Worker (Process, Thread, etc) by the length of list object.
            2. Multiple Worker by an option value like 'worker_num' or something else.
        :param function:
        :param args_iter:
        :param queue_tasks:
        :param features:
        :return:
        """
        pass


    @abstractmethod
    def map_with_function(self, functions: IterableType[Callable], args_iter: IterableType = [],
                          queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                          features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        """
        Description:
            Receive a function (Callable object) List object and distribute
            them to
            1. Multiple Worker (Process, Thread, etc) by the length of list object.
            2. Multiple Worker by an option value like 'worker_num' or something else.
        :param functions:
        :param args_iter:
        :param queue_tasks:
        :param features:
        :return:
        """
        pass


    @abstractmethod
    def close(self, workers: Union[_MRTasks, List[_MRTasks]]) -> None:
        """
        Description:
            Close executor(s).
        :return:
        """
        pass


    @abstractmethod
    def result(self) -> List[_MRResult]:
        """
        Description:
            Get the running result.
        :return:
        """
        pass

