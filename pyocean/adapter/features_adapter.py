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

from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple, Iterable, Any, Type



class _AdapterModuleFactory:

    @staticmethod
    def get_lock_adapter(mode: FeatureMode) -> PosixThreadLock:
        __module, __lock_cls_name = _AdapterModuleFactory.get_module(mode=mode, cls="lock")
        lock_cls = ImportPyocean.get_class(pkg_path=__module, cls_name=__lock_cls_name)
        return lock_cls()


    @staticmethod
    def get_communication_adapter(mode: FeatureMode) -> PosixThreadCommunication:
        __module, __lock_cls_name = _AdapterModuleFactory.get_module(mode=mode, cls="communication")
        lock_cls = ImportPyocean.get_class(pkg_path=__module, cls_name=__lock_cls_name)
        return lock_cls()


    @staticmethod
    def get_module(mode: FeatureMode, cls: str) -> Tuple[str, str]:
        _running_info: Dict[str, str] = mode.value
        __module: str = _running_info.get("module")
        __cls_name: str = _running_info.get(cls)
        return __module, __cls_name



class BaseAdapterFactory(metaclass=ABCMeta):

    def __init__(self, mode: FeatureMode, **kwargs):
        self._mode = mode
        self._kwargs = {}
        if self._mode is FeatureMode.Asynchronous:
            self._kwargs["loop"] = _AsyncUtils.check_event_loop(event_loop=kwargs.get("event_loop", None))


    @abstractmethod
    def get_instance(self):
        pass


    @abstractmethod
    def globalize_instance(self, obj) -> None:
        pass



class Lock(BaseAdapterFactory):

    def get_instance(self) -> OceanLock:
        lock_instance: PosixThreadLock = _AdapterModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_lock(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.lock(lock=obj)



class RLock(BaseAdapterFactory):

    def get_instance(self, **kwargs) -> OceanRLock:
        lock_instance: PosixThreadLock = _AdapterModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_rlock(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.rlock(rlock=obj)



class Semaphore(BaseAdapterFactory):
    
    def __init__(self, mode: FeatureMode, value: int, **kwargs):
        super(Semaphore, self).__init__(mode=mode, **kwargs)
        self.__semaphore_value = value


    def get_instance(self, **kwargs) -> OceanSemaphore:
        lock_instance: PosixThreadLock = _AdapterModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_semaphore(value=self.__semaphore_value, **self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.semaphore(smp=obj)



class BoundedSemaphore(BaseAdapterFactory):

    def __init__(self, mode: FeatureMode, value: int, **kwargs):
        super(BoundedSemaphore, self).__init__(mode=mode, **kwargs)
        self.__semaphore_value = value


    def get_instance(self, **kwargs) -> OceanBoundedSemaphore:
        lock_instance: PosixThreadLock = _AdapterModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_bounded_semaphore(value=self.__semaphore_value, **self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.bounded_semaphore(bsmp=obj)



class Event(BaseAdapterFactory):

    def get_instance(self) -> OceanEvent:
        communication_instance: PosixThreadCommunication = _AdapterModuleFactory.get_communication_adapter(mode=self._mode)
        return communication_instance.get_event(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.event(event=obj)



class Condition(BaseAdapterFactory):

    def __init__(self, mode: FeatureMode, **kwargs):
        super(Condition, self).__init__(mode=mode, **kwargs)
        if self._mode is FeatureMode.Asynchronous:
            self._kwargs["lock"] = _AsyncUtils.check_lock(lock=kwargs.get("lock", None))


    def get_instance(self) -> OceanCondition:
        communication_instance: PosixThreadCommunication = _AdapterModuleFactory.get_communication_adapter(mode=self._mode)
        return communication_instance.get_condition(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.condition(condition=obj)



class _AsyncUtils:

    @staticmethod
    def check_event_loop(event_loop):
        if event_loop is None:
            raise Exception("Async Event Loop object cannot be empty.")
        return event_loop


    @staticmethod
    def check_lock(lock):
        if lock:
            raise Exception("Async Lock object cannot be empty.")
        return lock


class FeatureList:

    __Max: int = -1
    __Feature_Adapter_Factory_List: List[BaseAdapterFactory] = []

    def __init__(self, max: int):
        if max == 0 or max < 0:
            raise ValueError("")

        if max > 0:
            self.__Max = max


    def __len__(self):
        return len(self.__Feature_Adapter_Factory_List)


    def index(self, index: int) -> BaseAdapterFactory:
        return self.__Feature_Adapter_Factory_List[index]


    def append(self, feature: BaseAdapterFactory) -> None:
        self.__Feature_Adapter_Factory_List.append(feature)


    def insert(self, index: int, value: BaseAdapterFactory) -> None:
        self.__Feature_Adapter_Factory_List.insert(index, value)


    def extend(self, __iterator) -> None:
        self.__Feature_Adapter_Factory_List.extend(__iterator)


    def pop(self, index: int) -> None:
        self.__Feature_Adapter_Factory_List.pop(index)


    def remove(self, value) -> None:
        self.__Feature_Adapter_Factory_List.remove(value)


    def clear(self) -> None:
        self.__Feature_Adapter_Factory_List.clear()


    def iterator(self):
        return FeatureIterator(factory_list=self)



class FeatureIterator:

    __Features_List = None

    def __init__(self, factory_list: FeatureList):
        self.__Features_List = factory_list
        self.__index = 0



    def has_next(self) -> bool:
        if self.__index < len(self.__Features_List):
            return True
        else:
            return False


    def next(self) -> BaseAdapterFactory:
        __feature = self.__Features_List.index(self.__index)
        self.__index += 1
        return __feature



class FeatureAdapterFactory(BaseFeatureAdapterFactory):

    def get_queue_adapter(self) -> BaseQueue:
        return QueueAdapter(mode=self._mode)


    def get_lock_adapter(self, **kwargs) -> PosixThreadLock:
        return LockAdapter(mode=self._mode, **kwargs)


    def get_communication_adapter(self, **kwargs) -> PosixThreadCommunication:
        return CommunicationAdapter(mode=self._mode, **kwargs)


    def get_globalization(self) -> Type[BaseGlobalizeAPI]:
        return Globalize



class BaseAdapter(metaclass=ABCMeta):

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
        if self._mode is FeatureMode.Asynchronous:
            return self.communication_instance.get_event(*args, **kwargs)
        else:
            return self.communication_instance.get_event()


    def get_condition(self, *args, **kwargs) -> OceanCondition:
        if self._mode is FeatureMode.Asynchronous:
            if kwargs.get("lock", None):
                raise Exception("Async Lock object cannot be empty.")
            kwargs["loop"] = self.__event_loop
        if self._mode is FeatureMode.Asynchronous:
            return self.communication_instance.get_condition(*args, **kwargs)
        else:
            return self.communication_instance.get_condition()

