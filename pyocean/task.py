from pyocean.framework.task import BaseTask, BaseQueueTask
from pyocean.framework.features import BaseQueueType
from pyocean.framework.collection import BaseList
from pyocean.types import OceanQueue
from pyocean.adapter.queue import Queue
from pyocean.adapter.collection import QueueTaskList

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

    _Queue_Task_List: QueueTaskList = None
    __Queue_Adapter = None

    def __add__(self, other) -> BaseList:
        if isinstance(other, QueueTaskList):
            other.append(self)
            _Queue_Task_List = other
        else:
            if self._Queue_Task_List is None:
                self._Queue_Task_List = QueueTaskList()
            self._Queue_Task_List.append(self)
            self._Queue_Task_List.append(other)
        return self._Queue_Task_List


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


    def get_queue(self) -> OceanQueue:
        self.__Queue_Adapter = Queue(name=self.name, qtype=self.queue_type)
        __queue_obj = self.__Queue_Adapter.get_instance()
        return __queue_obj


    def globalize(self, obj) -> None:
        self.__Queue_Adapter.globalize_instance(obj=obj)


    def init_queue_with_values(self) -> None:
        __queue = self.get_queue()
        for __value in self.value:
            __queue.put(__value)
        self.__Queue_Adapter.globalize_instance(obj=__queue)


    async def async_init_queue_with_values(self) -> None:
        __queue = self.get_queue()
        for __value in self.value:
            await __queue.put(__value)
        self.__Queue_Adapter.globalize_instance(obj=__queue)

