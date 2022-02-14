__all__ = ["Lock", "RLock", "Semaphore", "BoundedSemaphore"]

from ..framework.adapter import BaseLockAdapter, BaseAsyncLockAdapter
from ..factory import LockFactory, RLockFactory, SemaphoreFactory, BoundedSemaphoreFactory
from ..api import (
    LockOperator, RLockOperator, SemaphoreOperator, BoundedSemaphoreOperator,
    LockAsyncOperator, SemaphoreAsyncOperator, BoundedSemaphoreAsyncOperator
)



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
        return self._feature_operator.acquire(**__kwargs)


    def release(self, n: int = 1) -> None:
        return self._feature_operator.release(n=n)



class BoundedSemaphore(Semaphore):

    def _instantiate_factory(self) -> BoundedSemaphoreFactory:
        return BoundedSemaphoreFactory(value=self._value)


    def _instantiate_operator(self) -> BoundedSemaphoreOperator:
        return BoundedSemaphoreOperator()


    def release(self, n: int = 1) -> None:
        self._feature_operator.release()



class AsyncLock(BaseAsyncLockAdapter):

    def _instantiate_factory(self) -> LockAsyncOperator:
        return LockFactory()


    def _instantiate_operator(self) -> LockAsyncOperator:
        return LockAsyncOperator()


    async def acquire(self, *args, **kwargs) -> None:
        await self._feature_operator.acquire()


    def release(self, *args, **kwargs) -> None:
        self._feature_operator.release()



class AsyncSemaphore(BaseAsyncLockAdapter):

    def __init__(self, value: int = 1, **kwargs):
        self._value = value
        super().__init__(**kwargs)


    def _instantiate_factory(self) -> LockAsyncOperator:
        return SemaphoreFactory(value=self._value)


    def _instantiate_operator(self) -> LockAsyncOperator:
        return SemaphoreAsyncOperator()


    async def acquire(self, *args, **kwargs) -> None:
        await self._feature_operator.acquire()


    def release(self, *args, **kwargs) -> None:
        self._feature_operator.release()



class AsyncBoundedSemaphore(AsyncSemaphore):

    def _instantiate_factory(self) -> LockAsyncOperator:
        return BoundedSemaphoreFactory(value=self._value)


    def _instantiate_operator(self) -> LockAsyncOperator:
        return BoundedSemaphoreAsyncOperator()


    def release(self, *args, **kwargs) -> None:
        self._feature_operator.release()

