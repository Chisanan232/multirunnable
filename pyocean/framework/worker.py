from pyocean.framework.task import BaseTask
from pyocean.framework.result import OceanResult
from pyocean.api.mode import RunningMode
from pyocean.api.tool import Feature

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Optional



class BaseWorker(metaclass=ABCMeta):

    _Worker_Timeout = 3

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


    @abstractmethod
    def run(self, task: BaseTask):
        pass


    @abstractmethod
    def dispatcher(self):
        pass


    @abstractmethod
    def terminate(self):
        pass

