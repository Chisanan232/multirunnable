from pyocean.framework.api.operator import (
    AdapterOperator as _AdapterOperator,
    BaseLockAdapterOperator as _BaseLockAdapterOperator,
    AsyncAdapterOperator as _AsyncAdapterOperator,
    BaseAsyncLockAdapterOperator as _BaseAsyncLockOperator)
from pyocean.types import (
    OceanLock as _OceanLock,
    OceanRLock as _OceanRLock,
    OceanSemaphore as _OceanSemaphore,
    OceanBoundedSemaphore as _OceanBoundedSemaphore,
    OceanEvent as _OceanEvent,
    OceanCondition as _OceanCondition,
    OceanQueue as _OceanQueue)
from pyocean.exceptions import GlobalObjectIsNoneError as _GlobalObjectIsNoneError
from pyocean.api.exceptions import QueueNotExistWithName as _QueueNotExistWithName

from typing import Dict, Optional
import inspect



class LockAdapterOperator(_BaseLockAdapterOperator):

    def __init__(self):
        _BaseLockAdapterOperator.__init__(self)
        self.__lock: _OceanLock = self._feature_instance


    def __repr__(self):
        return f"<Operator object for {repr(self.__lock)}>"


    def _get_feature_instance(self) -> _OceanLock:
        from .manager import Running_Lock
        return Running_Lock


    def acquire(self) -> None:
        self.__lock.acquire()


    def release(self) -> None:
        self.__lock.release()



class RLockOperator(_BaseLockAdapterOperator):

    def __init__(self):
        _BaseLockAdapterOperator.__init__(self)
        self.__rlock: _OceanRLock = self._feature_instance


    def __repr__(self):
        return f"<Operator object for {repr(self.__rlock)}>"


    def _get_feature_instance(self) -> _OceanRLock:
        from .manager import Running_RLock
        return Running_RLock


    def acquire(self, blocking: bool = True, timeout: int = -1) -> None:
        # # # # From document, Parallel, Concurrent and Gevent all has both 2 parameters 'blocking' and 'timeout'.
        # # # # Parallel - multiprocessing doesn't have parameter 'blocking' and type is bool
        # # # # Concurrent - threading has parameter 'blocking' and type is bool
        # # # # Coroutine - gevent (greenlet framework) has parameter 'blocking' and type is int
        # # # # Async - asyncio doesn't have any parameter
        self.__rlock.acquire(blocking=blocking, timeout=timeout)

    # __enter__ = acquire

    def release(self) -> None:
        self.__rlock.release()



class SemaphoreOperator(_BaseLockAdapterOperator):

    def __init__(self):
        _BaseLockAdapterOperator.__init__(self)
        self.__semaphore: _OceanSemaphore = self._feature_instance


    def __repr__(self):
        return f"<Operator object for {repr(self.__semaphore)}>"


    def _get_feature_instance(self) -> _OceanSemaphore:
        from .manager import Running_Semaphore
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

        __kwargs = {}
        __kwargs.get("blocking", blocking)
        __kwargs.get("timeout", timeout)
        self.__semaphore.acquire(**__kwargs)

    # __enter__ = acquire

    def release(self, n: int = 1) -> None:
        # Needs to double check
        self.__semaphore.release(n=n)



class BoundedSemaphoreOperator(_BaseLockAdapterOperator):

    def __init__(self):
        _BaseLockAdapterOperator.__init__(self)
        self.__bounded_semaphore: _OceanBoundedSemaphore = self._feature_instance


    def __repr__(self):
        return f"<Operator object for {repr(self.__bounded_semaphore)}>"


    def _get_feature_instance(self) -> _OceanBoundedSemaphore:
        from .manager import Running_Bounded_Semaphore
        return Running_Bounded_Semaphore


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

        __kwargs = {}
        # __acquire_signature = inspect.signature(self.__bounded_semaphore.acquire)
        # __acquire_parameter = __acquire_signature.parameters
        # if "blocking" in __acquire_parameter.keys():
        #     __kwargs.get("blocking", blocking)
        # if "timeout" in __acquire_parameter.keys():
        #     __kwargs.get("timeout", timeout)

        __kwargs.get("blocking", blocking)
        __kwargs.get("timeout", timeout)

        self.__bounded_semaphore.acquire(**__kwargs)

    # __enter__ = acquire

    def release(self) -> None:
        self.__bounded_semaphore.release()



class EventOperator(_AdapterOperator):

    def __init__(self):
        _AdapterOperator.__init__(self)
        self.__event: _OceanEvent = self._get_feature_instance()


    def __repr__(self):
        return f"<Operator object for {repr(self.__event)}>"


    def _get_feature_instance(self) -> _OceanEvent:
        from .manager import Running_Event
        return Running_Event


    def set(self) -> None:
        self.__event.set()


    def is_set(self) -> bool:
        return self.__event.is_set()


    def wait(self, timeout: int = None) -> bool:
        """
        Note:
            Parallel & Concurrent & Green Thread are the same -  have parameter
            Async - asyncio doesn't have any parameter

        :param timeout:
        :return:
        """

        return self.__event.wait(timeout)


    def clear(self) -> None:
        self.__event.clear()



class ConditionOperator(_BaseLockAdapterOperator):

    def __init__(self):
        _BaseLockAdapterOperator.__init__(self)
        self.__condition: _OceanCondition = self._feature_instance


    def __repr__(self):
        return f"<Operator object for {repr(self.__condition)}>"


    def _get_feature_instance(self) -> _OceanCondition:
        from .manager import Running_Condition
        return Running_Condition


    def acquire(self, blocking: bool = True, timeout: int = None) -> None:
        self.__condition.acquire(blocking=blocking, timeout=timeout)


    def release(self) -> None:
        self.__condition.release()


    def wait(self, timeout: int = None) -> None:
        """
        Note:
            Parallel & Concurrent are the same -  have parameter
            Async - asyncio doesn't have any parameter

        :param timeout:
        :return:
        """

        self.__condition.wait(timeout)


    def wait_for(self, predicate, timeout: int = None) -> bool:
        """
        Note:
            Parallel & Concurrent are the same -  have parameter
            Async - asyncio only have one parameter 'predicate'

        :param predicate:
        :param timeout:
        :return:
        """

        return self.__condition.wait_for(predicate=predicate, timeout=timeout)


    def notify(self, n: int = 1) -> None:
        self.__condition.notify(n=n)


    def notify_all(self) -> None:
        self.__condition.notify_all()



class LockAsyncOperator(_BaseAsyncLockOperator):

    def __init__(self):
        _BaseAsyncLockOperator.__init__(self)
        self.__lock: _OceanLock = self._feature_instance


    def __repr__(self):
        return f"<AsyncOperator object for {repr(self.__lock)}>"


    def _get_feature_instance(self) -> _OceanLock:
        from .manager import Running_Lock
        return Running_Lock


    async def acquire(self):
        await self.__lock.acquire()


    def release(self):
        self.__lock.release()



class SemaphoreAsyncOperator(_BaseAsyncLockOperator):

    def __init__(self):
        _BaseAsyncLockOperator.__init__(self)
        self.__semaphore: _OceanSemaphore = self._feature_instance


    def __repr__(self):
        return f"<AsyncOperator object for {repr(self.__semaphore)}>"


    def _get_feature_instance(self) -> _OceanSemaphore:
        from .manager import Running_Semaphore
        return Running_Semaphore


    async def acquire(self):
        await self.__semaphore.acquire()


    def release(self):
        self.__semaphore.release()



class BoundedSemaphoreAsyncOperator(_BaseAsyncLockOperator):

    def __init__(self):
        _BaseAsyncLockOperator.__init__(self)
        self.__bounded_semaphore: _OceanBoundedSemaphore = self._feature_instance


    def __repr__(self):
        return f"<AsyncOperator object for {repr(self.__bounded_semaphore)}>"


    def _get_feature_instance(self) -> _OceanBoundedSemaphore:
        from .manager import Running_Bounded_Semaphore
        return Running_Bounded_Semaphore


    async def acquire(self):
        await self.__bounded_semaphore.acquire()


    def release(self):
        self.__bounded_semaphore.release()



class EventAsyncOperator(_AsyncAdapterOperator):

    def __init__(self):
        _AsyncAdapterOperator.__init__(self)
        self.__event: _OceanEvent = self._get_feature_instance()


    def __repr__(self):
        return f"<AsyncOperator object for {repr(self.__event)}>"


    def _get_feature_instance(self) -> _OceanEvent:
        from .manager import Running_Event
        return Running_Event


    def set(self) -> None:
        self.__event.set()


    def is_set(self) -> bool:
        return self.__event.is_set()


    async def wait(self, timeout: int = None) -> bool:
        # # # # Parallel & Concurrent & Greenlet are the same -  have parameter
        # # # # Async - asyncio doesn't have any parameter
        return await self.__event.wait(timeout)


    def clear(self) -> None:
        self.__event.clear()



class ConditionAsyncOperator(_BaseAsyncLockOperator):

    def __init__(self):
        _BaseAsyncLockOperator.__init__(self)
        self.__condition: _OceanCondition = self._feature_instance


    def __repr__(self):
        return f"<AsyncOperator object for {repr(self.__condition)}>"


    def _get_feature_instance(self) -> _OceanCondition:
        from .manager import Running_Condition
        return Running_Condition


    async def acquire(self) -> None:
        await self.__condition.acquire()


    def release(self) -> None:
        self.__condition.release()


    async def wait(self, timeout: int = None) -> None:
        # # # # Async - asyncio doesn't have any parameter
        # # # # Parallel & Concurrent are the same -  have parameter
        return await self.__condition.wait(timeout)


    async def wait_for(self, predicate) -> bool:
        # # # # Async - asyncio only have one parameter 'predicate'
        # # # # Parallel & Concurrent are the same -  have parameter
        return await self.__condition.wait_for(predicate=predicate)


    def notify(self, n: int = 1) -> None:
        self.__condition.notify(n=n)


    def notify_all(self) -> None:
        self.__condition.notify_all()



class QueueOperator(_AdapterOperator):

    @classmethod
    def _checking_init(cls, target_obj: object) -> bool:
        if target_obj is None:
            raise _GlobalObjectIsNoneError
        return True


    @classmethod
    def has_queue(cls, name: str):
        from .manager import Running_Queue

        if name in Running_Queue.keys():
            return True
        else:
            return False


    @classmethod
    def get_queue(cls) -> Optional[Dict[str, _OceanQueue]]:
        from .manager import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    def get_queue_with_name(cls, name: str) -> _OceanQueue:
        from .manager import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        if cls.has_queue(name=name):
            return Running_Queue[name]
        else:
            raise _QueueNotExistWithName


