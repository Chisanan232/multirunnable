from typing import Iterable
from abc import ABCMeta, abstractmethod

import multirunnable._utils as _utils
from ..types import MRQueue as _MRQueue



class BaseQueueTask(metaclass=ABCMeta):

    _Name: str = ""
    _Queue_Instance: _MRQueue = None
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
                              f"queue_type={self.queue_instance}, " \
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
    def queue_instance(self) -> _MRQueue:
        pass


    @property
    @abstractmethod
    def value(self) -> Iterable:
        pass


    @abstractmethod
    def get_queue(self) -> _MRQueue:
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

