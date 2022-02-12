__all__ = ["Lock", "RLock", "Semaphore", "BoundedSemaphore"]

from typing import Union

from ..framework.adapter import BaseLockAdapter, BaseAsyncLockAdapter
from ..factory import LockFactory, RLockFactory, SemaphoreFactory, BoundedSemaphoreFactory
from ..api import (
    LockOperator, RLockOperator, SemaphoreOperator, BoundedSemaphoreOperator,
    LockAsyncOperator, SemaphoreAsyncOperator, BoundedSemaphoreAsyncOperator
)
from ..framework.api import BaseLockAdapterOperator, BaseAsyncLockAdapterOperator
from ..framework.factory import BaseFeatureAdapterFactory
from ..types import MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition


class Lock(BaseLockAdapter):

    def _instantiate_factory(self) -> LockFactory:
        return LockFactory()


    def _instantiate_operator(self) -> LockOperator:
        return LockOperator()


    def acquire(self) -> None:
        self._feature_operator.acquire()


    def release(self) -> None:
        self._feature_operator.release()



class RLock(BaseLockAdapter):

    def _instantiate_factory(self) -> RLockFactory:
        return RLockFactory()


    def _instantiate_operator(self) -> RLockOperator:
        return RLockOperator()


    def acquire(self, blocking: bool = True, timeout: int = -1) -> None:
        __kwargs = {}
        __kwargs.get("blocking", blocking)
        __kwargs.get("timeout", timeout)
        self._feature_operator.acquire(**__kwargs)


    def release(self) -> None:
        self._feature_operator.release()



class Semaphore(BaseLockAdapter):

    def __init__(self, value: int = 1, **kwargs):
        self._value = value
        super().__init__(**kwargs)


    def _instantiate_factory(self) -> SemaphoreFactory:
        return SemaphoreFactory(value=self._value)


    def _instantiate_operator(self) -> SemaphoreOperator:
        return SemaphoreOperator()


    def acquire(self, blocking: bool = True, timeout: int = None) -> None:
        __kwargs = {}
        __kwargs.get("blocking", blocking)
        __kwargs.get("timeout", timeout)
        self._feature_operator.acquire(**__kwargs)


    def release(self, n: int = 1) -> None:
        self._feature_operator.release(n=n)



class BoundedSemaphore(Semaphore):

    def _instantiate_factory(self) -> BoundedSemaphoreFactory:
        return BoundedSemaphoreFactory(value=self._value)


    def _instantiate_operator(self) -> BoundedSemaphoreOperator:
        return BoundedSemaphoreOperator()


    def release(self, n: int = 1) -> None:
        self._feature_operator.release()



class AsyncLock(BaseAsyncLockAdapter):

    async def acquire(self, *args, **kwargs) -> None:
        pass


    def release(self, *args, **kwargs) -> None:
        pass


    def _instantiate_factory(self) -> BaseFeatureAdapterFactory:
        pass


    def _instantiate_operator(self) -> Union[BaseLockAdapterOperator, BaseAsyncLockAdapterOperator]:
        pass


    def get_instance(self) -> Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]:
        pass


    def globalize(self, obj: Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]) -> None:
        pass

