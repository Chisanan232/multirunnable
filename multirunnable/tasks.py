from typing import Iterable

from .framework.runnable import BaseQueueType as _BaseQueueType
from .framework.factory import BaseList as _BaseList
from .framework.task import BaseQueueTask as _BaseQueueTask
from .factory.collection import QueueTaskList as _QueueTaskList
from .factory.queue import QueueAdapter as _QueueAdapter
from .types import MRQueue as _MRQueue



class QueueTask(_BaseQueueTask):

    _Queue_Task_List: _QueueTaskList = None
    __Queue_Adapter = None

    def __add__(self, other) -> _BaseList:
        if isinstance(other, _QueueTaskList):
            other.append(self)
            _Queue_Task_List = other
        else:
            if self._Queue_Task_List is None:
                self._Queue_Task_List = _QueueTaskList()
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
    def queue_instance(self) -> _BaseQueueType:
        return self._Queue_Instance


    @queue_instance.setter
    def queue_instance(self, qinst: _BaseQueueType) -> None:
        self._Queue_Instance = qinst


    @property
    def value(self) -> Iterable:
        return self._Value


    @value.setter
    def value(self, val: Iterable) -> None:
        self._Value = val


    def get_queue(self) -> _MRQueue:
        self.__Queue_Adapter = _QueueAdapter(name=self.name, qtype=self.queue_instance)
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

