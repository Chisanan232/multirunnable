from pyocean.framework.result import OceanResult
from pyocean.api.mode import RunningMode, FeatureMode

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Tuple, Dict, Callable, Union



class BaseTask(metaclass=ABCMeta):

    _Group = None
    _Function = None
    _Fun_Args = None
    _Fun_Kwargs = None
    _Initialization = None
    _Init_Args = None
    _Init_Kwargs = None
    _Done_Handler = None
    _Error_Handler = None
    _Running_Timeout = None

    def __init__(self):
        pass

    @property
    @abstractmethod
    def function(self) -> Callable:
        pass


    @abstractmethod
    def set_function(self, function: Callable):
        pass


    @property
    @abstractmethod
    def func_args(self) -> Tuple:
        pass


    @abstractmethod
    def set_func_args(self, args: Tuple):
        pass


    @property
    @abstractmethod
    def func_kwargs(self) -> Dict:
        pass


    @abstractmethod
    def set_func_kwargs(self, kwargs: Dict):
        pass


    @property
    @abstractmethod
    def initialization(self) -> Callable:
        pass


    @abstractmethod
    def set_initialization(self, init: Callable):
        pass


    @property
    @abstractmethod
    def init_args(self) -> Tuple:
        pass


    @abstractmethod
    def set_init_args(self, args: Tuple):
        pass


    @property
    @abstractmethod
    def init_kwargs(self) -> Dict:
        pass


    @abstractmethod
    def set_init_kwargs(self, kwargs: Dict):
        pass


    @property
    @abstractmethod
    def group(self) -> str:
        pass


    @abstractmethod
    def set_group(self, group: str):
        pass


    @property
    @abstractmethod
    def done_handler(self) -> Callable:
        pass


    @abstractmethod
    def set_done_handler(self, hdlr: Callable):
        pass


    @property
    @abstractmethod
    def error_handler(self) -> Callable:
        pass


    @abstractmethod
    def set_error_handler(self, hdlr: Callable):
        pass


    @property
    @abstractmethod
    def running_timeout(self) -> int:
        pass


    @abstractmethod
    def set_running_timeout(self, timeout: int):
        pass



class BaseWorker(metaclass=ABCMeta):

    _Running_Timeout = 3

    @property
    @abstractmethod
    def running_timeout(self) -> int:
        pass


    @running_timeout.setter
    @abstractmethod
    def running_timeout(self, timeout: int) -> None:
        pass


    @abstractmethod
    def start(self, task: BaseTask):
        pass


    @abstractmethod
    def pre_start(self):
        pass


    @abstractmethod
    def pre_stop(self, e: Exception):
        pass


    @abstractmethod
    def post_stop(self):
        pass


    @abstractmethod
    def post_done(self):
        pass


    @abstractmethod
    def get_result(self) -> List[OceanResult]:
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

