from multirunnable.types import (
    OceanLock as _OceanLock,
    OceanRLock as _OceanRLock,
    OceanSemaphore as _OceanSemaphore,
    OceanBoundedSemaphore as _OceanBoundedSemaphore,
    OceanEvent as _OceanEvent,
    OceanCondition as _OceanCondition,
    OceanQueue as _OceanQueue)

from abc import ABCMeta, abstractmethod
from typing import Union, NewType


__OceanFeature = Union[_OceanLock, _OceanRLock, _OceanSemaphore, _OceanBoundedSemaphore, _OceanEvent, _OceanCondition, _OceanQueue]
_OceanFeatureType = NewType("OceanFeatureType", __OceanFeature)


class AdapterOperator(metaclass=ABCMeta):

    pass



class BaseLockAdapterOperator(AdapterOperator):

    _Feature_Instance: _OceanFeatureType = None

    def __init__(self, *args, **kwargs):
        pass


    def __repr__(self):
        return f"<Operator object for {repr(self._feature_instance)}>"


    def __enter__(self):
        self._feature_instance.__enter__()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._feature_instance.__exit__(exc_type, exc_val, exc_tb)


    @property
    def _feature_instance(self) -> _OceanFeatureType:
        if self._Feature_Instance is None:
            self._Feature_Instance = self._get_feature_instance()
            if self._Feature_Instance is None:
                __feature_opt_class = self.__class__.__name__
                __feature = __feature_opt_class.replace("Operator", "")
                raise ValueError(f"The {__feature} object not be initialed yet.")
        return self._Feature_Instance


    @_feature_instance.setter
    def _feature_instance(self, feature: _OceanFeatureType) -> None:
        self._Feature_Instance = feature


    @abstractmethod
    def _get_feature_instance(self) -> _OceanFeatureType:
        pass


    @abstractmethod
    def acquire(self, *args, **kwargs) -> None:
        pass


    @abstractmethod
    def release(self, *args, **kwargs) -> None:
        pass



class _AsyncContextManager:

    def __init__(self, lock):
        self._lock = lock


    def __enter__(self):
        return None


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()



class AsyncAdapterOperator(metaclass=ABCMeta):

    def __enter__(self):
        raise RuntimeError("")


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass




class BaseAsyncLockAdapterOperator(AsyncAdapterOperator):

    _Feature_Instance: _OceanFeatureType = None

    def __init__(self, *args, **kwargs):
        pass


    def __repr__(self):
        return f"<AsyncOperator object for {repr(self._feature_instance)}>"


    def __await__(self):
        return self.__acquire_ctx().__await__()


    async def __aenter__(self):
        await self._feature_instance.__aenter__()
        return None


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._feature_instance.__aexit__(exc_type, exc_val, exc_tb)


    async def __acquire_ctx(self):
        await self.acquire()
        return _AsyncContextManager(self)


    @property
    def _feature_instance(self) -> _OceanFeatureType:
        if self._Feature_Instance is None:
            self._Feature_Instance = self._get_feature_instance()
            if self._Feature_Instance is None:
                __feature_opt_class = self.__class__.__name__
                __feature = __feature_opt_class.replace("Operator", "")
                raise ValueError(f"The {__feature} object not be initialed yet.")
        return self._Feature_Instance


    @_feature_instance.setter
    def _feature_instance(self, feature: _OceanFeatureType) -> None:
        self._Feature_Instance = feature


    @abstractmethod
    def _get_feature_instance(self) -> _OceanFeatureType:
        pass


    @abstractmethod
    async def acquire(self, *args, **kwargs) -> None:
        pass


    @abstractmethod
    def release(self, *args, **kwargs) -> None:
        pass

