from pyocean.framework.task import BaseTask as _BaseTask, BaseQueueTask as _BaseQueueTask
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.mode import RunningMode as _RunningMode
from pyocean.persistence.interface import OceanPersistence as _OceanPersistence
import pyocean._utils as _utils

from abc import ABCMeta, abstractmethod
from typing import List, Iterable, Callable, Optional, Union



class BaseSystem(metaclass=ABCMeta):

    def __init__(self, mode: _RunningMode, worker_num: int):
        self._mode = mode
        self._worker_num = worker_num


    def __str__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(mode={self._mode}, " \
                               f"worker_num={self._worker_num})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    def __repr__(self):
        return f"{self.__str__()} at {id(self.__class__)}"


    @abstractmethod
    def run(self,
            task: _BaseTask,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
            saving_mode: bool = False,
            timeout: int = 0) -> [_OceanResult]:
        pass


    @abstractmethod
    def run_and_save(self,
                     task: _BaseTask,
                     persistence_strategy: _OceanPersistence,
                     db_connection_num: int,
                     queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                     features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                     saving_mode: bool = False,
                     timeout: int = 0) -> [_OceanResult]:
        pass


    @abstractmethod
    def map_by_params(self,
                      function: Callable,
                      args_iter: Iterable = [],
                      queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                      features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None):
        pass


    @abstractmethod
    def map_by_functions(self,
                         functions: List[Callable],
                         args_iter: Iterable = [],
                         queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                         features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None):
        pass


    # @abstractmethod
    def dispatcher(self):
        pass


    # @abstractmethod
    def terminate(self):
        pass
