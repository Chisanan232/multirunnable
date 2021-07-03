from pyocean.framework.features import (
    PosixThreadLock, PosixThreadCommunication,
    BaseQueue, BaseAPI, BaseQueueType)
from pyocean.api.mode import RunningMode, NewRunningMode
from pyocean.types import (
    OceanLock, OceanRLock,
    OceanSemaphore, OceanBoundedSemaphore,
    OceanEvent, OceanCondition)
from pyocean._import_utils import ImportPyocean

from importlib import import_module
from typing import Dict, Callable
import logging

from deprecation import deprecated


_Package: str = "pyocean"


@deprecated(
    deprecated_in="0.7.3",
    removed_in="0.8.1",
    current_version="0.7.3",
    details="Classify the lock, event and queue to be different class.")
class RunningStrategyAPI(BaseAPI):

    def __init__(self, mode: RunningMode):
        """
        Description:
            It will import the target module and instancing the target class to be the instance object.
            In the other words, it will
              1. If it's parallel strategy, import pyocean.parallel.features.MultiProcessing.
              2. If it's concurrent strategy, import pyocean.concurrent.features.{MultiThreading, Coroutine or Asynchronous}.
        :param mode:
        """

        __running_info: Dict[str, str] = mode.value
        self.__module_info: str = __running_info.get("module")
        self.__class_info: str = __running_info.get("class")
        self.__package = import_module(name=self.__module_info, package=_Package)
        logging.debug(f"package obj: {self.__package}")
        self.__class: Callable = getattr(self.__package, self.__class_info)
        self.__class_instance = self.__class()
        logging.debug(f"__class: {self.__class}")
        logging.debug(f"__class_instance: {self.__class_instance}")


    def lock(self):
        return self.__class_instance.lock()


    def event(self, **kwargs):
        return self.__class_instance.event(**kwargs)


    def condition(self, **kwargs):
        return self.__class_instance.condition(**kwargs)


    def semaphore(self, value: int):
        return self.__class_instance.semaphore(value=value)


    def bounded_semaphore(self, value: int):
        return self.__class_instance.bounded_semaphore(value=value)


    def queue(self, qtype: BaseQueueType):
        if not isinstance(qtype, BaseQueueType):
            raise TypeError("Parameter 'qtype' should be one value of object 'BaseQueueType'.")
        return self.__class_instance.queue(qtype=qtype)



class BaseAdapter:

    def __init__(self, mode: NewRunningMode):
        """
        Description:
            It will import the target module and instancing the target class to be the instance object.
            In the other words, it will
              1. If it's parallel strategy, import pyocean.parallel.features.MultiProcessing.
              2. If it's concurrent strategy, import pyocean.concurrent.features.{MultiThreading, Coroutine or Asynchronous}.
        :param mode:
        """

        self._running_info: Dict[str, str] = mode.value
        self._module: str = self._running_info.get("module")



class QueueAdapter(BaseAdapter, BaseQueue):

    def __init__(self, mode: NewRunningMode):
        super().__init__(mode=mode)
        self.__queue_cls_name: str = self._running_info.get("queue")
        self.queue_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__queue_cls_name)
        self.queue_instance: BaseQueue = self.queue_cls()


    def get_queue(self, qtype: BaseQueueType):
        return self.queue_instance.get_queue(qtype=qtype)



class LockAdapter(BaseAdapter, PosixThreadLock):

    def __init__(self, mode: NewRunningMode):
        super().__init__(mode=mode)
        self.__lock_cls_name: str = self._running_info.get("lock")
        self.lock_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__lock_cls_name)
        self.lock_instance: PosixThreadLock = self.lock_cls()


    def get_lock(self) -> OceanLock:
        return self.lock_instance.get_lock()


    def get_rlock(self) -> OceanRLock:
        return self.lock_instance.get_rlock()


    def get_semaphore(self, value: int) -> OceanSemaphore:
        return self.lock_instance.get_semaphore(value=value)


    def get_bounded_semaphore(self, value: int) -> OceanBoundedSemaphore:
        return self.lock_instance.get_bounded_semaphore(value=value)



class CommunicationAdapter(BaseAdapter, PosixThreadCommunication):

    def __init__(self, mode: NewRunningMode):
        super().__init__(mode=mode)
        self.__communication_cls_name: str = self._running_info.get("communication")
        self.communication_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__communication_cls_name)
        self.communication_instance: PosixThreadCommunication = self.communication_cls()


    def get_event(self, *args, **kwargs) -> OceanEvent:
        return self.communication_instance.get_event(*args, **kwargs)


    def get_condition(self, *args, **kwargs) -> OceanCondition:
        return self.communication_instance.get_condition(*args, **kwargs)

