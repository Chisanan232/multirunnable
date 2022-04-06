from gevent.threading import Lock as _Greenlet_Lock
from gevent.lock import (
    RLock as _Greenlet_RLock,
    Semaphore as _Greenlet_Semaphore,
    BoundedSemaphore as _Greenlet_BoundedSemaphore)
from gevent.event import Event as _Greenlet_Event

from asyncio.locks import (
    Lock as _Async_Lock,
    Semaphore as _Async_Semaphore,
    BoundedSemaphore as _Async_BoundedSemaphore)
from asyncio import Event as _Async_Event, Condition as _Async_Condition

from typing import Dict, Optional
import logging

from ..framework.runnable.synchronization import (
    PosixThreadLock as _PosixThreadLock,
    PosixThreadCommunication as _PosixThreadCommunication)
from ..types import (
    MRCondition as _MRCondition,
    MREvent as _MREvent
)
from .. import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION



class GreenThreadLock(_PosixThreadLock):

    def get_lock(self, **kwargs) -> _Greenlet_Lock:
        return _Greenlet_Lock()


    def get_rlock(self, **kwargs) -> _Greenlet_RLock:
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

