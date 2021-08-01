from pyocean.framework.features import (
    PosixThreadLock, PosixThreadCommunication,
    BaseQueue, BaseQueueType)
from pyocean.api.mode import FeatureMode
from pyocean.types import (
    OceanLock, OceanRLock,
    OceanSemaphore, OceanBoundedSemaphore,
    OceanEvent, OceanCondition,
    OceanQueue)
from pyocean._import_utils import ImportPyocean

from typing import Dict, Iterable, Any



class BaseAdapter:

    def __init__(self, mode: FeatureMode):
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

    def __init__(self, mode: FeatureMode):
        super().__init__(mode=mode)
        self.__queue_cls_name: str = self._running_info.get("queue")
        self.queue_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__queue_cls_name)
        self.queue_instance: BaseQueue = self.queue_cls()


    def get_queue(self, qtype: BaseQueueType) -> OceanQueue:
        return self.queue_instance.get_queue(qtype=qtype)


    def init_queue_with_values(self, qtype: BaseQueueType, values: Iterable[Any]) -> OceanQueue:
        __queue = self.get_queue(qtype=qtype)
        for value in values:
            __queue.put(value)
        return __queue


    async def async_init_queue_with_values(self, qtype: BaseQueueType, values: Iterable[Any]) -> OceanQueue:
        __queue = self.get_queue(qtype=qtype)
        for value in values:
            await __queue.put(value)
        return __queue


class LockAdapter(BaseAdapter, PosixThreadLock):

    def __init__(self, mode: FeatureMode):
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

    def __init__(self, mode: FeatureMode):
        super().__init__(mode=mode)
        self.__communication_cls_name: str = self._running_info.get("communication")
        self.communication_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__communication_cls_name)
        self.communication_instance: PosixThreadCommunication = self.communication_cls()


    def get_event(self, *args, **kwargs) -> OceanEvent:
        return self.communication_instance.get_event(*args, **kwargs)


    def get_condition(self, *args, **kwargs) -> OceanCondition:
        return self.communication_instance.get_condition(*args, **kwargs)

