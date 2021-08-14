from pyocean.framework.task import BaseTask
from pyocean.framework.result import OceanResult
from pyocean.mode import RunningMode
from pyocean.tool import Feature
import pyocean._utils as _utils

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Optional



class BaseWorker(metaclass=ABCMeta):

    _Worker_Timeout = 3

    def __init__(self, mode: RunningMode, worker_num: int):
        self._mode = mode
        self.worker_num = worker_num


    def __str__(self):
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


    def __repr__(self):
        return


    @property
    @abstractmethod
    def running_timeout(self) -> int:
        pass


    @abstractmethod
    def _initial_running_strategy(self) -> None:
        pass


    @abstractmethod
    def start(self,
              task: BaseTask,
              queue_tasks: Optional[List[BaseTask]] = None,
              features: Optional[List[Feature]] = None,
              saving_mode: bool = False,
              init_args: Tuple = (), init_kwargs: Dict = {}) -> None:
        pass


    @abstractmethod
    def pre_activate(self, *args, **kwargs) -> None:
        pass


    @abstractmethod
    def activate(self, task: BaseTask, saving_mode: bool = False) -> None:
        pass


    @abstractmethod
    def run_task(self, task: BaseTask) -> List[OceanResult]:
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
    def get_result(self) -> List[OceanResult]:
        pass



class BaseAsyncWorker(BaseWorker):

    @abstractmethod
    async def start(self,
                    task: BaseTask,
                    queue_tasks: Optional[List[BaseTask]] = None,
                    features: Optional[List[Feature]] = None,
                    saving_mode: bool = False,
                    init_args: Tuple = (), init_kwargs: Dict = {}) -> None:
        pass


    @abstractmethod
    async def pre_activate(self, *args, **kwargs) -> None:
        pass


    @abstractmethod
    async def activate(self, task: BaseTask, saving_mode: bool = False) -> None:
        pass


    @abstractmethod
    async def run_task(self, task: BaseTask) -> List[OceanResult]:
        pass



class BaseSystem(metaclass=ABCMeta):

    def __init__(self, mode: RunningMode, worker_num: int):
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
        return


    @abstractmethod
    def run(self, task: BaseTask):
        pass


    @abstractmethod
    def dispatcher(self):
        pass


    @abstractmethod
    def terminate(self):
        pass

