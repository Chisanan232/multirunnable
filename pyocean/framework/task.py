from pyocean.framework.features import BaseQueueType
from pyocean.framework.result import OceanResult
from pyocean.api.mode import RunningMode

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Iterable, Callable, Union



class BaseTaskFunction:

    @classmethod
    def function(cls, *args, **kwargs) -> List[OceanResult]:
        pass


    @classmethod
    def initialization(cls, *args, **kwargs) -> None:
        pass


    @classmethod
    def done_handler(cls, result: List[OceanResult]) -> List[OceanResult]:
        return result


    @classmethod
    def error_handler(cls, e: Exception) -> Union[List[OceanResult], Exception]:
        raise e



class BaseTaskAsyncFunction:

    @classmethod
    async def function(cls, *args, **kwargs) -> List[OceanResult]:
        pass


    @classmethod
    async def initialization(cls, *args, **kwargs) -> None:
        pass


    @classmethod
    async def done_handler(cls, result: List[OceanResult]) -> List[OceanResult]:
        return result


    @classmethod
    async def error_handler(cls, e: Exception) -> Union[List[OceanResult], Exception]:
        raise e



class BaseTask(metaclass=ABCMeta):

    _Group = None
    _Function = None
    _Fun_Args = ()
    _Fun_Kwargs = {}
    _Initialization = None
    _Init_Args = ()
    _Init_Kwargs = {}
    _Done_Handler = None
    _Error_Handler = None
    _Running_Timeout = 0

    def __init__(self, mode: RunningMode):
        if mode is RunningMode.Asynchronous:
            self._Function = BaseTaskAsyncFunction.function
            self._Initialization = BaseTaskAsyncFunction.initialization
            self._Done_Handler = BaseTaskAsyncFunction.done_handler
            self._Error_Handler = BaseTaskAsyncFunction.error_handler
        else:
            self._Function = BaseTaskFunction.function
            self._Initialization = BaseTaskFunction.initialization
            self._Done_Handler = BaseTaskFunction.done_handler
            self._Error_Handler = BaseTaskFunction.error_handler


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



class BaseQueueTask(metaclass=ABCMeta):

    _Queue_Type: BaseQueueType = None
    _Value: Iterable = None

    @property
    @abstractmethod
    def queue_type(self) -> BaseQueueType:
        pass


    @property
    @abstractmethod
    def value(self) -> Iterable:
        pass


