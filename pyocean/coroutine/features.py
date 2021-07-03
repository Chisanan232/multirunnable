from pyocean.types import OceanCondition, OceanEvent
from pyocean.framework.features import PosixThreadLock, PosixThreadCommunication, BaseQueue, BaseAPI, BaseQueueType, FeatureUtils
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
from asyncio.events import AbstractEventLoop

from typing import Union

from deprecated.sphinx import deprecated



class GeventQueueType(BaseQueueType):

    Queue = _Greenlet_Queue()
    SimpleQueue = _Greenlet_SimpleQueue()
    JoinableQueue = _Greenlet_JoinableQueue()
    PriorityQueue = _Greenlet_PriorityQueue()
    LifoQueue = _Greenlet_LifoQueue()



class GreenletQueue(BaseQueue):

    def get_queue(self, qtype: GeventQueueType):
        return qtype.value



@deprecated(version="0.7", reason="Classify the lock, event and queue to be different class.")
class GeventAPI(BaseAPI):

    def lock(self):
        return _Greenlet_Lock()


    def rlock(self):
        return _Greenlet_RLock()


    def event(self, **kwargs):
        return _Greenlet_Event()


    def condition(self, **kwargs):
        raise Exception("Coroutine running strategy doesn't have method 'condition'. Please change to use 'event'.")


    def semaphore(self, value: int):
        return _Greenlet_Semaphore(value=value)


    def bounded_semaphore(self, value: int):
        return _Greenlet_BoundedSemaphore(value=value)


    def queue(self, qtype: GeventQueueType):
        return qtype.value



class GreenletLock(PosixThreadLock):

    def get_lock(self) -> _Greenlet_Lock:
        return _Greenlet_Lock()


    def get_rlock(self) -> _Greenlet_RLock:
        return _Greenlet_RLock()


    def get_semaphore(self, value: int) -> _Greenlet_Semaphore:
        return _Greenlet_Semaphore(value=value)


    def get_bounded_semaphore(self, value: int) -> _Greenlet_BoundedSemaphore:
        return _Greenlet_BoundedSemaphore(value=value)



class GreenletCommunicationSpec(PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> OceanEvent:
        pass


    def get_condition(self, *args, **kwargs) -> OceanCondition:
        raise RuntimeError("Greenlet doesn't have condition attribute.")



class GreenletCommunication(GreenletCommunicationSpec):

    def get_event(self, *args, **kwargs) -> _Greenlet_Event:
        return _Greenlet_Event()



class AsynchronousQueueType(BaseQueueType):

    Queue = _Async_Queue()
    PriorityQueue = _Async_PriorityQueue()
    LifoQueue = _Async_LifoQueue()



class AsyncQueue(BaseQueue):

    def get_queue(self, qtype: AsynchronousQueueType):
        return qtype.value



@deprecated(version="0.7", reason="Classify the lock, event and queue to be different class.")
class AsynchronousAPI(BaseAPI):

    def lock(self):
        return _Async_Lock()


    def event(self, **kwargs):
        __loop = FeatureUtils.chk_obj(param="loop", **kwargs)
        # __loop = self.__chk_loop_obj(**kwargs)
        return _Async_Event(loop=__loop)


    def condition(self, **kwargs):
        __lock = FeatureUtils.chk_obj(param="lock", **kwargs)
        __loop = FeatureUtils.chk_obj(param="loop", **kwargs)
        # __lock = self.__chk_lock_obj(**kwargs)
        # __loop = self.__chk_loop_obj(**kwargs)
        return _Async_Condition(lock=__lock, loop=__loop)


    @deprecated(version="0.6", reason="Move the method into class 'FeatureUtils'")
    def __chk_lock_obj(self, **kwargs):
        __lock = kwargs.get("lock")
        if __lock is None:
            raise Exception("")
        return __lock


    @deprecated(version="0.6", reason="Move the method into class 'FeatureUtils'")
    def __chk_loop_obj(self, **kwargs):
        __loop = kwargs.get("loop")
        if __loop is None:
            raise Exception("")
        return __loop


    def semaphore(self, value: int):
        return _Async_Semaphore(value=value)


    def bounded_semaphore(self, value: int):
        return _Async_BoundedSemaphore(value=value)


    def queue(self, qtype: AsynchronousQueueType):
        return qtype.value



class AsyncLock(PosixThreadLock):

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



class AsyncCommunication(PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> _Async_Event:
        __loop = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Event(loop=__loop)


    def get_condition(self, *args, **kwargs) -> _Async_Condition:
        __lock = _AsyncUtils.chk_lock(lock=kwargs.get("lock", None))
        __loop = _AsyncUtils.chk_loop(loop=kwargs.get("loop", None))
        return _Async_Condition(lock=__lock, loop=__loop)



class _AsyncUtils:

    @classmethod
    def chk_lock(cls, **kwargs) -> Union[None, _Async_Lock]:
        __lock = kwargs.get("lock", None)
        if __lock is not None and isinstance(__lock, _Async_Lock):
            raise TypeError("Lock type is incorrect.")
        else:
            return __lock


    @classmethod
    def chk_loop(cls, **kwargs) -> Union[None, AbstractEventLoop]:
        __loop = kwargs.get("loop", None)
        if __loop is not None and isinstance(__loop, AbstractEventLoop):
            raise TypeError("Event loop type is incorrect.")
        else:
            return __loop

