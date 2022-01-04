from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from multirunnable.framework.features import (
    PosixThreadLock as _PosixThreadLock,
    PosixThreadCommunication as _PosixThreadCommunication,
    BaseQueueType as _BaseQueueType)
from multirunnable.types import (
    MRCondition as _MRCondition,
    MREvent as _MREvent
)

if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
    from gevent.queue import (
        Queue as _Greenlet_Queue,
        SimpleQueue as _Greenlet_SimpleQueue,
        JoinableQueue as _Greenlet_JoinableQueue,
        PriorityQueue as _Greenlet_PriorityQueue,
        LifoQueue as _Greenlet_LifoQueue)

    class GeventQueueType(_BaseQueueType):
        Queue = _Greenlet_Queue()
        SimpleQueue = _Greenlet_SimpleQueue()
        JoinableQueue = _Greenlet_JoinableQueue()
        PriorityQueue = _Greenlet_PriorityQueue()
        LifoQueue = _Greenlet_LifoQueue()

else:
    from gevent.queue import (
        Queue as _Greenlet_Queue,
        JoinableQueue as _Greenlet_JoinableQueue,
        PriorityQueue as _Greenlet_PriorityQueue,
        LifoQueue as _Greenlet_LifoQueue)

    class GeventQueueType(_BaseQueueType):
        Queue = _Greenlet_Queue()
        JoinableQueue = _Greenlet_JoinableQueue()
        PriorityQueue = _Greenlet_PriorityQueue()
        LifoQueue = _Greenlet_LifoQueue()

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

from typing import Dict, Optional, Union
import logging



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

    def get_event(self, *args, **kwargs) -> _MREvent:
        pass


    def get_condition(self, *args, **kwargs) -> _MRCondition:
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
        __param = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Lock(**__param)


    def get_rlock(self, **kwargs) -> _Async_Lock:
        __param = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Lock(**__param)


    def get_semaphore(self, value: int, **kwargs) -> _Async_Semaphore:
        __param = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        __param["value"] = value
        return _Async_Semaphore(**__param)


    def get_bounded_semaphore(self, value: int, **kwargs) -> _Async_BoundedSemaphore:
        __param = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        __param["value"] = value
        return _Async_BoundedSemaphore(**__param)



class AsynchronousCommunication(_PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> _Async_Event:
        __param = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Event(**__param)


    def get_condition(self, *args, **kwargs) -> _Async_Condition:
        # __lock = _AsyncUtils.chk_lock(lock=kwargs.get("lock", None))
        __lock = kwargs.get("lock", None)
        __param = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        __param["lock"] = __lock
        return _Async_Condition(**__param)



class _AsyncUtils:

    @classmethod
    def chk_lock(cls, **kwargs) -> Dict[str, Optional[_Async_Lock]]:
        __lock = kwargs.get("lock", None)
        if __lock is not None and isinstance(__lock, _Async_Lock):
            raise TypeError("Lock type is incorrect.")
        elif __lock is None:
            raise ValueError("Async Lock object cannot be empty.")
        else:
            return {"lock": __lock}


    @classmethod
    def chk_loop(cls, **kwargs) -> Dict:
        __loop = kwargs.get("loop", None)
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) >= (3, 10):
            logging.info("Doesn't pass parameter 'loop' in Python 3.10.")
            return {}
        else:
            if __loop is not None:
                return {"loop": __loop}
            else:
                raise ValueError("Async Event Loop object cannot be empty.")

