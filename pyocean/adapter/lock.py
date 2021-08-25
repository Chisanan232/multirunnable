from pyocean.framework.features import PosixThreadLock as _PosixThreadLock
from pyocean.mode import FeatureMode as _FeatureMode
from pyocean.api.manager import Globalize as _Globalize
from pyocean.types import (
    OceanLock as _OceanLock,
    OceanRLock as _OceanRLock,
    OceanSemaphore as _OceanSemaphore,
    OceanBoundedSemaphore as _OceanBoundedSemaphore)
from pyocean.adapter.base import FeatureAdapterFactory as _FeatureAdapterFactory
from pyocean.adapter._utils import _ModuleFactory



class Lock(_FeatureAdapterFactory):

    def __str__(self):
        return super(Lock, self).__str__().replace("TargetObject", "Lock")


    def __repr__(self):
        return super(Lock, self).__repr__().replace("TargetObject", "Lock")


    def get_instance(self) -> _OceanLock:
        lock_instance: _PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_lock(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.lock(lock=obj)



class RLock(_FeatureAdapterFactory):

    def __str__(self):
        return super(RLock, self).__str__().replace("TargetObject", "RLock")


    def __repr__(self):
        return super(RLock, self).__repr__().replace("TargetObject", "RLock")


    def get_instance(self, **kwargs) -> _OceanRLock:
        lock_instance: _PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_rlock(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.rlock(rlock=obj)



class Semaphore(_FeatureAdapterFactory):

    def __init__(self, mode: _FeatureMode, value: int, **kwargs):
        super(Semaphore, self).__init__(mode=mode, **kwargs)
        self.__semaphore_value = value


    def __str__(self):
        return super(Semaphore, self).__str__().replace("TargetObject", "Semaphore")


    def __repr__(self):
        __mode = self._mode
        __value = self.__semaphore_value
        if __mode is _FeatureMode.Asynchronous:
            __loop = self._kwargs["loop"]
            return f"<Semaphore(value={__value}, loop={__loop}) object with {__mode} mode at {id(self)}>"
        else:
            return f"<Semaphore(value={__value}) object with {__mode} mode at {id(self)}>"


    def get_instance(self, **kwargs) -> _OceanSemaphore:
        lock_instance: _PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_semaphore(value=self.__semaphore_value, **self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.semaphore(smp=obj)



class BoundedSemaphore(_FeatureAdapterFactory):

    def __init__(self, mode: _FeatureMode, value: int, **kwargs):
        super(BoundedSemaphore, self).__init__(mode=mode, **kwargs)
        self.__semaphore_value = value


    def __str__(self):
        return super(BoundedSemaphore, self).__str__().replace("TargetObject", "Bounded Semaphore")


    def __repr__(self):
        __mode = self._mode
        __value = self.__semaphore_value
        if __mode is _FeatureMode.Asynchronous:
            __loop = self._kwargs["loop"]
            return f"<BoundedSemaphore(value={__value}, loop={__loop}) object with {__mode} mode at {id(self)}>"
        else:
            return f"<BoundedSemaphore(value={__value}) object with {__mode} mode at {id(self)}>"


    def get_instance(self, **kwargs) -> _OceanBoundedSemaphore:
        lock_instance: _PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self._mode)
        return lock_instance.get_bounded_semaphore(value=self.__semaphore_value, **self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.bounded_semaphore(bsmp=obj)

