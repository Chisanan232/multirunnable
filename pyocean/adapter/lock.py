from pyocean.framework.features import PosixThreadLock
from pyocean.mode import FeatureMode
from pyocean.api.manager import Globalize
from pyocean.types import (
    OceanLock, OceanRLock,
    OceanSemaphore, OceanBoundedSemaphore)
from pyocean.adapter.base import FeatureAdapterFactory, BaseAdapter
from pyocean.adapter._utils import _ModuleFactory
from pyocean._import_utils import ImportPyocean



class Lock(FeatureAdapterFactory):

    def __str__(self):
        return super(Lock, self).__str__().replace("TargetObject", "Lock")


    def __repr__(self):
        return super(Lock, self).__repr__().replace("TargetObject", "Lock")


    def get_instance(self) -> OceanLock:
        lock_instance: PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_lock(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.lock(lock=obj)



class RLock(FeatureAdapterFactory):

    def __str__(self):
        return super(RLock, self).__str__().replace("TargetObject", "RLock")


    def __repr__(self):
        return super(RLock, self).__repr__().replace("TargetObject", "RLock")


    def get_instance(self, **kwargs) -> OceanRLock:
        lock_instance: PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_rlock(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.rlock(rlock=obj)



class Semaphore(FeatureAdapterFactory):

    def __init__(self, mode: FeatureMode, value: int, **kwargs):
        super(Semaphore, self).__init__(mode=mode, **kwargs)
        self.__semaphore_value = value


    def __str__(self):
        return super(Semaphore, self).__str__().replace("TargetObject", "Semaphore")


    def __repr__(self):
        __mode = self._mode
        __value = self.__semaphore_value
        if __mode is FeatureMode.Asynchronous:
            __loop = self._kwargs["loop"]
            return f"<Semaphore(value={__value}, loop={__loop}) object with {__mode} mode at {id(self)}>"
        else:
            return f"<Semaphore(value={__value}) object with {__mode} mode at {id(self)}>"


    def get_instance(self, **kwargs) -> OceanSemaphore:
        lock_instance: PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_semaphore(value=self.__semaphore_value, **self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.semaphore(smp=obj)



class BoundedSemaphore(FeatureAdapterFactory):

    def __init__(self, mode: FeatureMode, value: int, **kwargs):
        super(BoundedSemaphore, self).__init__(mode=mode, **kwargs)
        self.__semaphore_value = value


    def __str__(self):
        return super(BoundedSemaphore, self).__str__().replace("TargetObject", "Bounded Semaphore")


    def __repr__(self):
        __mode = self._mode
        __value = self.__semaphore_value
        if __mode is FeatureMode.Asynchronous:
            __loop = self._kwargs["loop"]
            return f"<BoundedSemaphore(value={__value}, loop={__loop}) object with {__mode} mode at {id(self)}>"
        else:
            return f"<BoundedSemaphore(value={__value}) object with {__mode} mode at {id(self)}>"


    def get_instance(self, **kwargs) -> OceanBoundedSemaphore:
        lock_instance: PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_bounded_semaphore(value=self.__semaphore_value, **self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.bounded_semaphore(bsmp=obj)



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

