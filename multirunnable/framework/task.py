from multirunnable.framework.features import BaseQueueType as _BaseQueueType
from multirunnable.framework.result import OceanResult as _OceanResult
from multirunnable.mode import RunningMode as _RunningMode
from multirunnable.types import OceanQueue as _OceanQueue
from multirunnable.persistence.interface import OceanPersistence as _OceanPersistence
import multirunnable._utils as _utils

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Iterable, Callable, Union



class BaseTaskFunction:

    @classmethod
    def function(cls, *args, **kwargs) -> List[_OceanResult]:
        pass


    @classmethod
    def initialization(cls, *args, **kwargs) -> None:
        pass


    @classmethod
    def done_handler(cls, result: List[_OceanResult]) -> List[_OceanResult]:
        return result


    @classmethod
    def error_handler(cls, e: Exception) -> Union[List[_OceanResult], Exception]:
        raise e



class BaseTaskAsyncFunction:

    @classmethod
    async def function(cls, *args, **kwargs) -> List[_OceanResult]:
        pass


    @classmethod
    async def initialization(cls, *args, **kwargs) -> None:
        pass


    @classmethod
    async def done_handler(cls, result: List[_OceanResult]) -> List[_OceanResult]:
        return result


    @classmethod
    async def error_handler(cls, e: Exception) -> Union[List[_OceanResult], Exception]:
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

    def __init__(self, mode: _RunningMode):
        self._mode = mode
        __base_task_function_obj = None
        if mode is _RunningMode.Asynchronous:
            __base_task_function_obj = BaseTaskAsyncFunction
        else:
            __base_task_function_obj = BaseTaskFunction
        self._Function = __base_task_function_obj.function
        self._Initialization = __base_task_function_obj.initialization
        self._Done_Handler = __base_task_function_obj.done_handler
        self._Error_Handler = __base_task_function_obj.error_handler


    def __str__(self):
        __instance_brief = None
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(mode={self._mode})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    def __repr__(self):
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_info = f"{__cls_name}(mode={self._mode}) with " \
                              f"group={self.group}, " \
                              f"function={self.function}, " \
                              f"fun_args={self.func_args}, " \
                              f"fun_kwargs={self.func_kwargs}, " \
                              f"initialization={self.initialization}, " \
                              f"init_args={self.init_args}, " \
                              f"init_kwargs={self.init_kwargs}, " \
                              f"done_handler={self.done_handler}, " \
                              f"error_handler={self.error_handler}, " \
                              f"running_timeout={self.running_timeout}"
        else:
            __instance_info = __cls_str
        return __instance_info


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

    _Name: str = ""
    _Queue_Type: _BaseQueueType = None
    _Value: Iterable = None

    def __str__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}()"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    def __repr__(self):
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_info = f"{__cls_name} with " \
                              f"name={self.name}, " \
                              f"queue_type={self.queue_type}, " \
                              f"value={self.value}"
        else:
            __instance_info = __cls_str
        return __instance_info


    @property
    @abstractmethod
    def name(self) -> str:
        pass


    @property
    @abstractmethod
    def queue_type(self) -> _BaseQueueType:
        pass


    @property
    @abstractmethod
    def value(self) -> Iterable:
        pass


    @abstractmethod
    def get_queue(self) -> _OceanQueue:
        pass


    @abstractmethod
    def globalize(self, obj) -> None:
        pass


    @abstractmethod
    def init_queue_with_values(self) -> None:
        pass


    @abstractmethod
    async def async_init_queue_with_values(self) -> None:
        pass



class BasePersistenceTask(metaclass=ABCMeta):

    _Persistence_Strategy: _OceanPersistence = None
    _Database_Connection_Number: int = 0

    @property
    @abstractmethod
    def strategy(self) -> _OceanPersistence:
        pass


    @property
    @abstractmethod
    def connection_pool_size(self) -> int:
        pass

