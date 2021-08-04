from pyocean.framework.task import BaseTask, BaseQueueTask
from pyocean.framework.features import BaseQueueType

from typing import Tuple, Dict, Iterable, Callable



class OceanTask(BaseTask):

    @property
    def function(self) -> Callable:
        return self._Function


    def set_function(self, function: Callable) -> BaseTask:
        self._Function = function
        return self


    @property
    def func_args(self) -> Tuple:
        return self._Fun_Args


    def set_func_args(self, args: Tuple) -> BaseTask:
        self._Fun_Args = args
        return self


    @property
    def func_kwargs(self) -> Dict:
        return self._Fun_Kwargs


    def set_func_kwargs(self, kwargs: Dict) -> BaseTask:
        for key, value in kwargs.items():
            self._Fun_Kwargs[key] = value
        return self


    @property
    def initialization(self) -> Callable:
        return self._Initialization


    def set_initialization(self, init: Callable) -> BaseTask:
        self._Initialization = init
        return self


    @property
    def init_args(self) -> Tuple:
        return self._Init_Args


    def set_init_args(self, args: Tuple) -> BaseTask:
        self._Init_Args = args
        return self


    @property
    def init_kwargs(self) -> Dict:
        return self._Init_Kwargs


    def set_init_kwargs(self, kwargs: Dict) -> BaseTask:
        for key, value in kwargs.items():
            self._Init_Kwargs[key] = value
        return self


    @property
    def group(self) -> str:
        return self._Group


    def set_group(self, group: str) -> BaseTask:
        self._Group = group
        return self


    @property
    def done_handler(self) -> Callable:
        return self._Done_Handler


    def set_done_handler(self, hdlr: Callable) -> BaseTask:
        self._Done_Handler = hdlr
        return self


    @property
    def error_handler(self) -> Callable:
        return self._Error_Handler


    def set_error_handler(self, hdlr: Callable) -> BaseTask:
        self._Error_Handler = hdlr
        return self


    @property
    def running_timeout(self) -> int:
        return self._Running_Timeout


    def set_running_timeout(self, timeout: int) -> BaseTask:
        self._Running_Timeout = timeout
        return self



class QueueTask(BaseQueueTask):

    @property
    def name(self) -> str:
        return self._Name


    @name.setter
    def name(self, name: str) -> None:
        self._Name = name


    @property
    def queue_type(self) -> BaseQueueType:
        return self._Queue_Type


    @queue_type.setter
    def queue_type(self, qtype: BaseQueueType) -> None:
        self._Queue_Type = qtype


    @property
    def value(self) -> Iterable:
        return self._Value


    @value.setter
    def value(self, val: Iterable) -> None:
        self._Value = val

