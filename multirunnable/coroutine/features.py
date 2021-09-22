from multirunnable.framework.features import (
    PosixThreadLock as _PosixThreadLock,
    PosixThreadCommunication as _PosixThreadCommunication,
    BaseQueueType as _BaseQueueType)
from multirunnable.types import (
    OceanCondition as _OceanCondition,
    OceanEvent as _OceanEvent
)

from gevent.queue import (
    Queue as _Greenlet_Queue,
    SimpleQueue as _Greenlet_SimpleQueue,
    JoinableQueue as _Greenlet_JoinableQueue,
    PriorityQueue as _Greenlet_PriorityQueue,
    LifoQueue as _Greenlet_LifoQueue)
from gevent.threading import Lock as _Greenlet_Lock
from gevent.lock import (
    RLock as _Greenlet_RLock,
    Semaphore as _Greenlet_Semaphore,
    BoundedSemaphore as _Greenlet_BoundedSemaphore)
from gevent.event import Event as _Greenlet_Event

from asyncio.queues import (
    Queue as _Async_Queue,
    PriorityQueue as _Async_PriorityQueue,
    LifoQueue as _Async_LifoQueue)
from asyncio.locks import (
    Lock as _Async_Lock,
    Semaphore as _Async_Semaphore,
    BoundedSemaphore as _Async_BoundedSemaphore)
from asyncio import Event as _Async_Event, Condition as _Async_Condition

from typing import Optional, Union



class GeventQueueType(_BaseQueueType):

    Queue = _Greenlet_Queue()
    SimpleQueue = _Greenlet_SimpleQueue()
    JoinableQueue = _Greenlet_JoinableQueue()
    PriorityQueue = _Greenlet_PriorityQueue()
    LifoQueue = _Greenlet_LifoQueue()



class GreenThreadLock(_PosixThreadLock):

    def get_lock(self) -> _Greenlet_Lock:
        return _Greenlet_Lock()


    def get_rlock(self) -> _Greenlet_RLock:
        return _Greenlet_RLock()


    def get_semaphore(self, value: int, **kwargs) -> _Greenlet_Semaphore:
        return _Greenlet_Semaphore(value=value)


    def get_bounded_semaphore(self, value: int, **kwargs) -> _Greenlet_BoundedSemaphore:
        return _Greenlet_BoundedSemaphore(value=value)



class GreenThreadCommunicationSpec(_PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> _OceanEvent:
        pass


    def get_condition(self, *args, **kwargs) -> _OceanCondition:
        raise RuntimeError("Greenlet doesn't have condition attribute.")



class GreenThreadCommunication(GreenThreadCommunicationSpec):

    def get_event(self, *args, **kwargs) -> _Greenlet_Event:
        return _Greenlet_Event()



class AsynchronousQueueType(_BaseQueueType):

    Queue = _Async_Queue()
    PriorityQueue = _Async_PriorityQueue()
    LifoQueue = _Async_LifoQueue()



class AsynchronousLock(_PosixThreadLock):

    def get_lock(self, **kwargs) -> _Async_Lock:
        __loop = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Lock(loop=__loop)


    def get_rlock(self, **kwargs) -> _Async_Lock:
        __loop = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Lock(loop=__loop)


    def get_semaphore(self, value: int, **kwargs) -> _Async_Semaphore:
        __loop = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Semaphore(value=value, loop=__loop)


    def get_bounded_semaphore(self, value: int, **kwargs) -> _Async_BoundedSemaphore:
        __loop = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_BoundedSemaphore(value=value, loop=__loop)



class AsynchronousCommunication(_PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> _Async_Event:
        __loop = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Event(loop=__loop)


    def get_condition(self, *args, **kwargs) -> _Async_Condition:
        # __lock = _AsyncUtils.chk_lock(lock=kwargs.get("lock", None))
        __lock = kwargs.get("lock", None)
        __loop = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Condition(lock=__lock, loop=__loop)



class _AsyncUtils:

    @classmethod
    def chk_lock(cls, **kwargs) -> Optional[_Async_Lock]:
        __lock = kwargs.get("lock", None)
        if __lock is not None and isinstance(__lock, _Async_Lock):
            raise TypeError("Lock type is incorrect.")
        elif __lock is None:
            raise Exception("Async Lock object cannot be empty.")
        else:
            return __lock


    @classmethod
    def chk_loop(cls, **kwargs):
        __loop = kwargs.get("loop", None)
        # if __loop is not None and isinstance(__loop, SelectorEventLoop):
        #     raise TypeError("Event loop type is incorrect.")
        # elif __loop is None:
        #     raise Exception("Async Event Loop object cannot be empty.")
        # else:
        #     return __loop
        if __loop is not None:
            return __loop
        else:
            raise Exception("Async Event Loop object cannot be empty.")

