from pyocean.framework.features import BaseQueueType
from pyocean.framework.result import OceanResult
from pyocean.mode import RunningMode
import pyocean._utils as _utils

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
        self._mode = mode
        __base_task_function_obj = None
        if mode is RunningMode.Asynchronous:
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
    _Queue_Type: BaseQueueType = None
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
    def queue_type(self) -> BaseQueueType:
        pass


    @property
    @abstractmethod
    def value(self) -> Iterable:
        pass


