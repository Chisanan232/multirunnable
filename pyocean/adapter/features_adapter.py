from pyocean.framework.features import (
    PosixThreadLock, PosixThreadCommunication,
    BaseQueue, BaseQueueType,
    BaseGlobalizeAPI,
    BaseFeatureAdapterFactory)
from pyocean.mode import FeatureMode
from pyocean.api.manager import Globalize
from pyocean.types import (
    OceanLock, OceanRLock,
    OceanSemaphore, OceanBoundedSemaphore,
    OceanEvent, OceanCondition,
    OceanQueue)
from pyocean._import_utils import ImportPyocean

from typing import Dict, Iterable, Any, Type



class FeatureAdapterFactory(BaseFeatureAdapterFactory):

    def get_queue_adapter(self) -> BaseQueue:
        return QueueAdapter(mode=self._mode)


    def get_lock_adapter(self, **kwargs) -> PosixThreadLock:
        return LockAdapter(mode=self._mode, **kwargs)


    def get_communication_adapter(self, **kwargs) -> PosixThreadCommunication:
        return CommunicationAdapter(mode=self._mode, **kwargs)


    def get_globalization(self) -> Type[BaseGlobalizeAPI]:
        return Globalize



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

        self._mode = mode
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

    def __init__(self, mode: FeatureMode, **kwargs):
        super().__init__(mode=mode)
        self.__lock_cls_name: str = self._running_info.get("lock")
        self.lock_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__lock_cls_name)
        self.lock_instance: PosixThreadLock = self.lock_cls()

        if mode is FeatureMode.Asynchronous:
            self.__event_loop = kwargs.get("event_loop", None)
            if self.__event_loop is None:
                raise Exception("Async Event Loop object cannot be empty.")


    def get_lock(self) -> OceanLock:
        if self._mode is FeatureMode.Asynchronous:
            return self.lock_instance.get_lock(loop=self.__event_loop)
        else:
            return self.lock_instance.get_lock()


    def get_rlock(self) -> OceanRLock:
        if self._mode is FeatureMode.Asynchronous:
            return self.lock_instance.get_rlock(loop=self.__event_loop)
        else:
            return self.lock_instance.get_rlock()


    def get_semaphore(self, value: int, **kwargs) -> OceanSemaphore:
        if self._mode is FeatureMode.Asynchronous:
            return self.lock_instance.get_semaphore(value=value, loop=self.__event_loop)
        else:
            return self.lock_instance.get_semaphore(value=value)


    def get_bounded_semaphore(self, value: int, **kwargs) -> OceanBoundedSemaphore:
        if self._mode is FeatureMode.Asynchronous:
            return self.lock_instance.get_bounded_semaphore(value=value, loop=self.__event_loop)
        else:
            return self.lock_instance.get_bounded_semaphore(value=value)



class CommunicationAdapter(BaseAdapter, PosixThreadCommunication):

    def __init__(self, mode: FeatureMode, **kwargs):
        super().__init__(mode=mode)
        self.__communication_cls_name: str = self._running_info.get("communication")
        self.communication_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__communication_cls_name)
        self.communication_instance: PosixThreadCommunication = self.communication_cls()

        if mode is FeatureMode.Asynchronous:
            self.__event_loop = kwargs.get("event_loop", None)
            if self.__event_loop is None:
                raise Exception("Async Event Loop object cannot be empty.")


    def get_event(self, *args, **kwargs) -> OceanEvent:
        if self._mode is FeatureMode.Asynchronous:
            kwargs["loop"] = self.__event_loop
        return self.communication_instance.get_event(*args, **kwargs)


    def get_condition(self, *args, **kwargs) -> OceanCondition:
        if self._mode is FeatureMode.Asynchronous:
            if kwargs.get("lock", None):
                raise Exception("Async Lock object cannot be empty.")
            kwargs["loop"] = self.__event_loop
        return self.communication_instance.get_condition(*args, **kwargs)

