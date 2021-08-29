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

from abc import ABCMeta, abstractmethod
from typing import Dict, Optional
import inspect



class AdapterOperator(metaclass=ABCMeta):

    # @abstractmethod
    # def _get_feature_instance(self):
    #     pass

    pass



class LockOperator(AdapterOperator):

    def __init__(self):
        from .manager import Running_Lock
        self.__lock: _OceanLock = Running_Lock


    def __repr__(self):
        return f"<Operator object for {repr(self.__lock)}>"


    def __enter__(self):
        self.__lock.__enter__()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__lock.__exit__(exc_type, exc_val, exc_tb)


    def acquire(self):
        self.__lock.acquire()


    def release(self):
        self.__lock.release()



class RLockOperator(AdapterOperator):

    def __init__(self):
        from .manager import Running_RLock
        self.__rlock: _OceanRLock = Running_RLock


    def __repr__(self):
        return f"<Operator object for {repr(self.__rlock)}>"


    def acquire(self, blocking: bool = True, timeout: int = -1):
        # # # # Parallel - multiprocessing doesn't have parameter 'blocking' and type is bool
        # # # # Concurrent - threading has parameter 'blocking' and type is bool
        # # # # Coroutine - gevent (greenlet framework) has parameter 'blocking' and type is int
        # # # # Async - asyncio doesn't have any parameter
        __acquire_parameter = inspect.signature(self.__rlock.acquire).parameters
        self.__rlock.acquire(blocking=blocking, timeout=timeout)

    __enter__ = acquire

    def release(self):
        self.__rlock.release()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__rlock.__exit__(exc_type, exc_val, exc_tb)



class SemaphoreOperator(AdapterOperator):

    def __init__(self):
        from .manager import Running_Semaphore
        self.__semaphore: _OceanSemaphore = Running_Semaphore


    def __repr__(self):
        return f"<Operator object for {repr(self.__semaphore)}>"


    def acquire(self, blocking: bool = True, timeout: int = None):
        # # # # Concurrent - threading has parameter 'blocking'
        # # # # Coroutine - gevent (greenlet framework) has parameter 'blocking'
        # self.__semaphore.acquire(blocking=blocking, timeout=timeout)

        # # # # Async - asyncio doesn't have any parameter

        # # # # Parallel - multiprocessing doesn't have parameter 'blocking'
        __acquire_parameter = inspect.signature(self.__semaphore.acquire).parameters
        self.__semaphore.acquire(timeout=timeout)

    __enter__ = acquire

    def release(self, n: int = 1):
        # Needs to double check
        self.__semaphore.release(n=n)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__semaphore.__exit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)



class BoundedSemaphoreOperator(AdapterOperator):

    def __init__(self):
        from .manager import Running_Bounded_Semaphore
        self.__bounded_semaphore: _OceanBoundedSemaphore = Running_Bounded_Semaphore


    def __repr__(self):
        return f"<Operator object for {repr(self.__bounded_semaphore)}>"


    def acquire(self, blocking: bool = True, timeout: int = None):
        # # # # Parallel - multiprocessing doesn't have parameter 'blocking'
        # # # # Concurrent - threading has parameter 'blocking'
        # # # # Coroutine - gevent (greenlet framework) has parameter 'blocking'
        # # # # Async - asyncio doesn't have any parameter
        __kwargs = {}
        print("Semaphore: ", self.__bounded_semaphore.acquire)
        __acquire_signature = inspect.signature(self.__bounded_semaphore.acquire)
        print("Semaphore signature: ", __acquire_signature)
        __acquire_parameter = __acquire_signature.parameters
        print("Semaphore parameter: ", __acquire_parameter)
        if "blocking" in __acquire_parameter.keys():
            __kwargs.get("blocking", blocking)
        if "timeout" in __acquire_parameter.keys():
            __kwargs.get("timeout", timeout)

        self.__bounded_semaphore.acquire(**__kwargs)
        # self.__bounded_semaphore.acquire(timeout=timeout)

    __enter__ = acquire

    # async def __aenter__(self):
    #     await self.acquire()
    #     return None
    #
    # async def __aexit__(self, exc_type, exc_val, exc_tb):
    #     self.release()

    # def __enter__(self):
    #     self.__bounded_semaphore.__enter__()

    def release(self):
        self.__bounded_semaphore.release()


    # # # # Error records:
    # # # # Parallel - multiprocessing
    # File "/.../apache-pyocean/pyocean/api/operator.py", line 118, in __exit__
    #     self.__bounded_semaphore.__exit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)
    # TypeError: __exit__() got an unexpected keyword argument 'exc_type'

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.__bounded_semaphore.__exit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)


    def __exit__(self, *args, **kwargs):
        self.__bounded_semaphore.__exit__(*args, **kwargs)



class EventOperator(AdapterOperator):

    def __init__(self):
        from .manager import Running_Event
        self.__event: _OceanEvent = Running_Event


    def __repr__(self):
        return f"<Operator object for {repr(self.__event)}>"


    def set(self) -> None:
        self.__event.set()


    def is_set(self) -> bool:
        return self.__event.is_set()


    def wait(self, timeout: int = None) -> bool:
        # # # # Parallel & Concurrent & Greenlet are the same -  have parameter
        # # # # Async - asyncio doesn't have any parameter
        return self.__event.wait(timeout)


    def clear(self) -> None:
        self.__event.clear()



class ConditionOperator(AdapterOperator):

    def __init__(self):
        from .manager import Running_Condition
        self.__condition: _OceanCondition = Running_Condition


    def __enter__(self):
        return self.__condition.__enter__()


    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.__condition.__exit(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)


    def __repr__(self):
        return f"<Operator object for {repr(self.__condition)}>"


    def acquire(self, blocking: bool = True, timeout: int = None) -> None:
        self.__condition.acquire(blocking=blocking, timeout=timeout)


    def release(self) -> None:
        self.__condition.release()


    def wait(self, timeout: int = None) -> None:
        # # # # Async - asyncio doesn't have any parameter
        # # # # Parallel & Concurrent are the same -  have parameter
        self.__condition.wait(timeout)


    def wait_for(self, predicate, timeout: int = None) -> bool:
        # # # # Async - asyncio only have one parameter 'predicate'
        # # # # Parallel & Concurrent are the same -  have parameter
        return self.__condition.wait_for(predicate=predicate, timeout=timeout)


    def notify(self, n: int = 1) -> None:
        self.__condition.notify(n=n)


    def notify_all(self) -> None:
        self.__condition.notify_all()



class QueueOperator(AdapterOperator):

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

