from multirunnable.framework.task import BaseQueueTask as _BaseQueueTask
from multirunnable.framework.features import BaseQueueType as _BaseQueueType
from multirunnable.framework.adapter.collection import BaseList as _BaseList
from multirunnable.types import MRQueue as _MRQueue
from multirunnable.adapter.queue import Queue as _Queue, QueueAdapter as _QueueAdapter
from multirunnable.adapter.collection import QueueTaskList as _QueueTaskList

from typing import Iterable



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
    def queue_type(self) -> _BaseQueueType:
        return self._Queue_Type


    @queue_type.setter
    def queue_type(self, qtype: _BaseQueueType) -> None:
        self._Queue_Type = qtype


    @property
    def value(self) -> Iterable:
        return self._Value


    @value.setter
    def value(self, val: Iterable) -> None:
        self._Value = val


    def get_queue(self) -> _MRQueue:
        self.__Queue_Adapter = _QueueAdapter(name=self.name, qtype=self.queue_type)
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

