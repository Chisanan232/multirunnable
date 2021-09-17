from pyocean.framework.task import BaseTask as _BaseTask, BaseQueueTask as _BaseQueueTask
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.mode import RunningMode as _RunningMode
from pyocean.types import OceanTasks as _OceanTasks
import pyocean._utils as _utils

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Callable, Iterable, Optional, Union



class BaseManager(metaclass=ABCMeta):

    _Worker_Timeout = 3
    _Ocean_Tasks_List: List[_OceanTasks] = []

    def __init__(self, mode: _RunningMode, worker_num: int):
        self._mode = mode
        self.worker_num = worker_num


    def __str__(self):
        return f"{self.__str__()} at {id(self.__class__)}"


    def __repr__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(mode={self._mode}, " \
                               f"worker_num={self.worker_num})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    @property
    @abstractmethod
    def running_timeout(self) -> int:
        pass


    @abstractmethod
    def _initial_running_strategy(self) -> None:
        pass


    @abstractmethod
    def start(self,
              task: _BaseTask,
              queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
              features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
              init_args: Tuple = (), init_kwargs: Dict = {}) -> None:
        pass


    @abstractmethod
    def pre_activate(self,
                     queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                     features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                     *args, **kwargs) -> None:
        pass


    @abstractmethod
    def activate(self, function: Callable, *args, **kwargs) -> None:
        pass


    @abstractmethod
    def pre_stop(self, e: Exception) -> None:
        pass


    @abstractmethod
    def post_stop(self) -> None:
        pass


    @abstractmethod
    def post_done(self) -> None:
        pass


    @abstractmethod
    def get_result(self) -> List[_OceanResult]:
        pass



class BaseAsyncManager(BaseManager):

    @abstractmethod
    def start(self,
              task: _BaseTask,
              queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
              features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
              init_args: Tuple = (), init_kwargs: Dict = {}) -> None:
        pass


    @abstractmethod
    async def pre_activate(self,
                           queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                           features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                           *args, **kwargs) -> None:
        pass


    @abstractmethod
    async def activate(self, function: Callable, *args, **kwargs) -> None:
        pass


    @abstractmethod
    async def run_task(self, task: _BaseTask) -> List[_OceanResult]:
        pass

