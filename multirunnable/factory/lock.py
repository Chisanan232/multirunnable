from ..framework.runnable import PosixThreadLock as _PosixThreadLock
from ..factory._utils import _ModuleFactory
from ..factory.base import FeatureAdapterFactory as _FeatureAdapterFactory
from ..api.manage import Globalize as _Globalize
from ..types import (
    MRLock as _MRLock,
    MRRLock as _MRRLock,
    MRSemaphore as _MRSemaphore,
    MRBoundedSemaphore as _MRBoundedSemaphore)
from ..mode import FeatureMode as _FeatureMode
from .. import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION



class LockFactory(_FeatureAdapterFactory):

    def __str__(self):
        return super(LockFactory, self).__str__().replace("TargetObject", "Lock")


    def __repr__(self):
        return super(LockFactory, self).__repr__().replace("TargetObject", "Lock")


    def get_instance(self, **kwargs) -> _MRLock:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) < (3, 10):
            self._chk_param_by_mode(**kwargs)

        if self.feature_mode is None:
            raise ValueError("FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'.")

        lock_instance: _PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self.feature_mode)
        return lock_instance.get_lock(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.lock(lock=obj)



class RLockFactory(_FeatureAdapterFactory):

    def __str__(self):
        return super(RLockFactory, self).__str__().replace("TargetObject", "RLock")


    def __repr__(self):
        return super(RLockFactory, self).__repr__().replace("TargetObject", "RLock")


    def get_instance(self, **kwargs) -> _MRRLock:
        self._chk_param_by_mode(**kwargs)
        if self.feature_mode is None:
            raise ValueError("FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'.")

        lock_instance: _PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self.feature_mode)
        return lock_instance.get_rlock(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.rlock(rlock=obj)



class SemaphoreFactory(_FeatureAdapterFactory):

    def __init__(self, value: int = 1):
        super(SemaphoreFactory, self).__init__()
        self.__semaphore_value = value


    def __str__(self):
        return super(SemaphoreFactory, self).__str__().replace("TargetObject", "Semaphore")


    def __repr__(self):
        __mode = self._Mode
        __value = self.__semaphore_value
        if __mode is _FeatureMode.Asynchronous:
            __loop = self._kwargs["loop"]
            return f"<Semaphore(value={__value}, loop={__loop}) object with {__mode} mode at {id(self)}>"
        else:
            return f"<Semaphore(value={__value}) object with {__mode} mode at {id(self)}>"


    def get_instance(self, **kwargs) -> _MRSemaphore:
        self._chk_param_by_mode(**kwargs)
        if self.feature_mode is None:
            raise ValueError("FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'.")

        lock_instance: _PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self.feature_mode)
        return lock_instance.get_semaphore(value=self.__semaphore_value, **self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.semaphore(smp=obj)



class BoundedSemaphoreFactory(_FeatureAdapterFactory):

    def __init__(self, value: int = 1):
        super(BoundedSemaphoreFactory, self).__init__()
        self.__semaphore_value = value


    def __str__(self):
        return super(BoundedSemaphoreFactory, self).__str__().replace("TargetObject", "Bounded Semaphore")


    def __repr__(self):
        __mode = self._Mode
        __value = self.__semaphore_value
        if __mode is _FeatureMode.Asynchronous:
            __loop = self._kwargs.get("loop", None)
            return f"<BoundedSemaphore(value={__value}, loop={__loop}) object with {__mode} mode at {id(self)}>"
        else:
            return f"<BoundedSemaphore(value={__value}) object with {__mode} mode at {id(self)}>"


    def get_instance(self, **kwargs) -> _MRBoundedSemaphore:
        self._chk_param_by_mode(**kwargs)
        if self.feature_mode is None:
            raise ValueError("FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'.")

        lock_instance: _PosixThreadLock = _ModuleFactory.get_lock_adapter(mode=self.feature_mode)
        return lock_instance.get_bounded_semaphore(value=self.__semaphore_value, **self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.bounded_semaphore(bsmp=obj)

