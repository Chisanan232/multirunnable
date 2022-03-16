__all__ = ["Event", "Condition"]

from ..framework.adapter import BaseCommunicationAdapter, BaseLockAdapter, BaseAsyncLockAdapter, BaseAsyncCommunicationAdapter
from ..factory import EventFactory, ConditionFactory
from ..api import (
    RLockOperator,
    EventOperator, ConditionOperator,
    EventAsyncOperator, ConditionAsyncOperator
)



class Event(BaseCommunicationAdapter):

    def _instantiate_factory(self) -> EventFactory:
        return EventFactory()


    def _instantiate_operator(self) -> EventOperator:
        return EventOperator()


    def set(self) -> None:
        self._feature_operator.set()


    def is_set(self) -> bool:
        return self._feature_operator.is_set()


    def wait(self, timeout: int = None) -> bool:
        return self._feature_operator.wait(timeout=timeout)


    def clear(self) -> None:
        self._feature_operator.clear()



class Condition(BaseLockAdapter, BaseCommunicationAdapter):

    def _instantiate_factory(self) -> ConditionFactory:
        return ConditionFactory()


    def _instantiate_operator(self) -> ConditionOperator:
        return ConditionOperator()


    def acquire(self, blocking: bool = True, timeout: int = None) -> None:
        _timeout = RLockOperator.converse_timeout_val(timeout=timeout)
        _args = (blocking, _timeout)
        self._feature_operator.acquire(*_args)


    def release(self) -> None:
        self._feature_operator.release()


    def wait(self, timeout: int = None) -> None:
        return self._feature_operator.wait(timeout=timeout)


    def wait_for(self, predicate, timeout: int = None) -> bool:
        return self._feature_operator.wait_for(predicate=predicate, timeout=timeout)


    def notify(self, n: int = 1) -> None:
        self._feature_operator.notify(n=n)


    def notify_all(self) -> None:
        self._feature_operator.notify_all()



class AsyncEvent(BaseAsyncCommunicationAdapter):

    def _instantiate_factory(self) -> EventFactory:
        return EventFactory()


    def _instantiate_operator(self) -> EventAsyncOperator:
        return EventAsyncOperator()


    def set(self) -> None:
        self._feature_operator.set()


    def is_set(self) -> bool:
        return self._feature_operator.is_set()


    async def wait(self) -> bool:
        return await self._feature_operator.wait()


    def clear(self) -> None:
        self._feature_operator.clear()



class AsyncCondition(BaseAsyncLockAdapter):

    def _instantiate_factory(self) -> ConditionFactory:
        return ConditionFactory()


    def _instantiate_operator(self) -> ConditionAsyncOperator:
        return ConditionAsyncOperator()


    async def acquire(self) -> None:
        await self._feature_operator.acquire()


    def release(self) -> None:
        self._feature_operator.release()


    async def wait(self) -> None:
        return await self._feature_operator.wait()


    async def wait_for(self, predicate) -> bool:
        return await self._feature_operator.wait_for(predicate=predicate)


    def notify(self, n: int = 1) -> None:
        self._feature_operator.notify(n=n)


    def notify_all(self) -> None:
        self._feature_operator.notify_all()


