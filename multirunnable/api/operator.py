from typing import Dict, Optional

from ..framework.api.operator import (
    AdapterOperator as _AdapterOperator,
    BaseLockAdapterOperator as _BaseLockAdapterOperator,
    AsyncAdapterOperator as _AsyncAdapterOperator,
    BaseAsyncLockAdapterOperator as _BaseAsyncLockOperator)
from ..api.exceptions import QueueNotExistWithName as _QueueNotExistWithName
from ..exceptions import GlobalObjectIsNoneError as _GlobalObjectIsNoneError
from .._config import get_current_mode
from ..types import (
    MRLock as _MRLock,
    MRRLock as _MRRLock,
    MRSemaphore as _MRSemaphore,
    MRBoundedSemaphore as _MRBoundedSemaphore,
    MREvent as _MREvent,
    MRCondition as _MRCondition,
    MRQueue as _MRQueue)
from ..mode import RunningMode



class LockOperator(_BaseLockAdapterOperator):

    def _get_feature_instance(self) -> _MRLock:
        from .manage import Running_Lock
        return Running_Lock


    def acquire(self) -> None:
        self._feature_instance.acquire()


    def release(self) -> None:
        self._feature_instance.release()



class RLockOperator(_BaseLockAdapterOperator):

    def _get_feature_instance(self) -> _MRRLock:
        from .manage import Running_RLock
        return Running_RLock


    def acquire(self, blocking: bool = True, timeout: int = None) -> None:
        # # # # From document, Parallel, Concurrent and Gevent all has both 2 parameters 'blocking' and 'timeout'.
        # # # # Async - asyncio doesn't have any parameter
        _timeout = RLockOperator.converse_timeout_val(timeout=timeout)
        _args = (blocking, _timeout)
        self._feature_instance.acquire(*_args)

    # __enter__ = acquire

    def release(self) -> None:
        self._feature_instance.release()


    @staticmethod
    def converse_timeout_val(timeout: int) -> int:
        _rmode = get_current_mode(force=True)
        if _rmode is RunningMode.Concurrent and timeout is None:
            timeout = -1
        return timeout



class SemaphoreOperator(_BaseLockAdapterOperator):

    def _get_feature_instance(self) -> _MRSemaphore:
        from .manage import Running_Semaphore
        return Running_Semaphore


    def acquire(self, blocking: bool = True, timeout: int = None) -> None:
        """
        Note:
            Parallel -  multiprocessing doesn't have parameter 'blocking'
            Concurrent - threading has parameter 'blocking'
            Coroutine - gevent (greenlet framework) has parameter 'blocking'
            Async - asyncio doesn't have any parameter

        :param blocking:
        :param timeout:
        :return:
        """

        _kwargs = {"blocking": blocking, "timeout": timeout}
        return self._feature_instance.acquire(**_kwargs)

    # __enter__ = acquire

    def release(self, n: int = 1) -> None:
        # Needs to double check
        return self._feature_instance.release(n=n)



class BoundedSemaphoreOperator(SemaphoreOperator):

    def _get_feature_instance(self) -> _MRBoundedSemaphore:
        from .manage import Running_Bounded_Semaphore
        return Running_Bounded_Semaphore

    # __enter__ = acquire

    def release(self, n=1) -> None:
        self._feature_instance.release()



class EventOperator(_AdapterOperator):

    _Event_Instance: _MREvent = None

    def __repr__(self):
        return f"<Operator object for {repr(self._event_instance)}>"


    @property
    def _event_instance(self) -> _MREvent:
        if self._Event_Instance is None:
            self._Event_Instance = self._get_feature_instance()
            if self._Event_Instance is None:
                raise ValueError("The Event object not be initialed yet.")
        return self._Event_Instance


    @_event_instance.setter
    def _event_instance(self, event: _MREvent) -> None:
        self._Event_Instance = event


    def _get_feature_instance(self) -> _MREvent:
        from .manage import Running_Event
        return Running_Event


    def set(self) -> None:
        self._event_instance.set()


    def is_set(self) -> bool:
        return self._event_instance.is_set()


    def wait(self, timeout: int = None) -> bool:
        """
        Note:
            Parallel & Concurrent & Green Thread are the same -  have parameter
            Async - asyncio doesn't have any parameter

        :param timeout:
        :return:
        """

        return self._event_instance.wait(timeout)


    def clear(self) -> None:
        self._event_instance.clear()



class ConditionOperator(_BaseLockAdapterOperator):

    def _get_feature_instance(self) -> _MRCondition:
        from .manage import Running_Condition
        return Running_Condition


    def acquire(self, blocking: bool = True, timeout: int = None) -> None:
        # _kwargs = {"blocking": blocking, "timeout": timeout}
        _timeout = RLockOperator.converse_timeout_val(timeout=timeout)
        _args = (blocking, _timeout)
        self._feature_instance.acquire(*_args)


    def release(self) -> None:
        self._feature_instance.release()


    def wait(self, timeout: int = None) -> None:
        """
        Note:
            Parallel & Concurrent are the same -  have parameter
            Async - asyncio doesn't have any parameter

        :param timeout:
        :return:
        """

        self._feature_instance.wait(timeout)


    def wait_for(self, predicate, timeout: int = None) -> bool:
        """
        Note:
            Parallel & Concurrent are the same -  have parameter
            Async - asyncio only have one parameter 'predicate'

        :param predicate:
        :param timeout:
        :return:
        """

        return self._feature_instance.wait_for(predicate=predicate, timeout=timeout)


    def notify(self, n: int = 1) -> None:
        self._feature_instance.notify(n=n)


    def notify_all(self) -> None:
        self._feature_instance.notify_all()



class LockAsyncOperator(_BaseAsyncLockOperator):

    def _get_feature_instance(self) -> _MRLock:
        from .manage import Running_Lock
        return Running_Lock


    async def acquire(self):
        await self._feature_instance.acquire()


    def release(self):
        self._feature_instance.release()



class SemaphoreAsyncOperator(_BaseAsyncLockOperator):

    def _get_feature_instance(self) -> _MRSemaphore:
        from .manage import Running_Semaphore
        return Running_Semaphore


    async def acquire(self):
        await self._feature_instance.acquire()


    def release(self):
        self._feature_instance.release()



class BoundedSemaphoreAsyncOperator(SemaphoreAsyncOperator):

    def _get_feature_instance(self) -> _MRBoundedSemaphore:
        from .manage import Running_Bounded_Semaphore
        return Running_Bounded_Semaphore


    def release(self):
        self._feature_instance.release()



class EventAsyncOperator(_AsyncAdapterOperator):

    _Event_Instance: _MREvent = None

    def __repr__(self):
        return f"<AsyncOperator object for {repr(self._event_instance)}>"


    @property
    def _event_instance(self) -> _MREvent:
        if self._Event_Instance is None:
            self._Event_Instance = self._get_feature_instance()
            if self._Event_Instance is None:
                raise ValueError("The Event object not be initialed yet.")
        return self._Event_Instance


    @_event_instance.setter
    def _event_instance(self, event: _MREvent) -> None:
        self._Event_Instance = event


    def _get_feature_instance(self) -> _MREvent:
        from .manage import Running_Event
        return Running_Event


    def set(self) -> None:
        self._event_instance.set()


    def is_set(self) -> bool:
        return self._event_instance.is_set()


    async def wait(self) -> bool:
        # # # # Parallel & Concurrent & Greenlet are the same -  have parameter
        # # # # Async - asyncio doesn't have any parameter
        return await self._event_instance.wait()


    def clear(self) -> None:
        self._event_instance.clear()



class ConditionAsyncOperator(_BaseAsyncLockOperator):

    def _get_feature_instance(self) -> _MRCondition:
        from .manage import Running_Condition
        return Running_Condition


    async def acquire(self) -> None:
        await self._feature_instance.acquire()


    def release(self) -> None:
        self._feature_instance.release()


    async def wait(self) -> None:
        # # # # Async - asyncio doesn't have any parameter
        # # # # Parallel & Concurrent are the same -  have parameter
        return await self._feature_instance.wait()


    async def wait_for(self, predicate) -> bool:
        # # # # Async - asyncio only have one parameter 'predicate'
        # # # # Parallel & Concurrent are the same -  have parameter
        return await self._feature_instance.wait_for(predicate=predicate)


    def notify(self, n: int = 1) -> None:
        self._feature_instance.notify(n=n)


    def notify_all(self) -> None:
        self._feature_instance.notify_all()



class QueueOperator(_AdapterOperator):

    @classmethod
    def _checking_init(cls, target_obj: object) -> bool:
        if target_obj is None:
            raise _GlobalObjectIsNoneError
        return True


    @classmethod
    def has_queue(cls, name: str):
        from .manage import Running_Queue

        if name in Running_Queue.keys():
            return True
        else:
            return False


    @classmethod
    def get_queue(cls) -> Optional[Dict[str, _MRQueue]]:
        from .manage import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    def get_queue_with_name(cls, name: str) -> _MRQueue:
        from .manage import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        if cls.has_queue(name=name):
            return Running_Queue[name]
        else:
            raise _QueueNotExistWithName


