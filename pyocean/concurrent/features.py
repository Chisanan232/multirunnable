from ..framework.features import BaseAPI, BaseQueueType, FeatureUtils

from deprecated.sphinx import deprecated



class MultiThreadingQueueType(BaseQueueType):

    from queue import Queue, SimpleQueue, LifoQueue, PriorityQueue

    Queue = Queue
    SimpleQueue = SimpleQueue
    LifoQueue = LifoQueue
    PriorityQueue = PriorityQueue



class MultiThreading(BaseAPI):

    def lock(self):
        from threading import Lock
        return Lock()


    def rlock(self):
        from threading import RLock
        return RLock()


    def event(self, **kwargs):
        from threading import Event
        return Event()


    def condition(self, **kwargs):
        from threading import Condition
        return Condition()


    def semaphore(self, value: int):
        from threading import Semaphore
        return Semaphore(value=value)


    def bounded_semaphore(self, value: int):
        from threading import BoundedSemaphore
        return BoundedSemaphore(value=value)


    def queue(self, qtype: MultiThreadingQueueType):
        return qtype.value()



class CoroutineQueueType(BaseQueueType):

    from gevent.queue import Queue, SimpleQueue, JoinableQueue, PriorityQueue, LifoQueue

    Queue = Queue
    SimpleQueue = SimpleQueue
    JoinableQueue = JoinableQueue
    PriorityQueue = PriorityQueue
    LifoQueue = LifoQueue



class Coroutine(BaseAPI):

    def lock(self):
        from gevent.threading import Lock
        return Lock()


    def rlock(self):
        from gevent.lock import RLock
        return RLock()


    def event(self, **kwargs):
        from gevent.event import Event
        return Event()


    def condition(self, **kwargs):
        raise Exception("Coroutine running strategy doesn't have method 'condition'. Please change to use 'event'.")


    def semaphore(self, value: int):
        from gevent.lock import Semaphore
        return Semaphore(value=value)


    def bounded_semaphore(self, value: int):
        from gevent.lock import BoundedSemaphore
        return BoundedSemaphore(value=value)


    def queue(self, qtype: CoroutineQueueType):
        return qtype.value()



class AsynchronousQueueType(BaseQueueType):

    from asyncio.queues import Queue, PriorityQueue, LifoQueue

    Queue = Queue
    PriorityQueue = PriorityQueue
    LifoQueue = LifoQueue



class Asynchronous(BaseAPI):

    def lock(self):
        from asyncio.locks import Lock
        return Lock()


    def event(self, **kwargs):
        from asyncio import Event
        __loop = FeatureUtils.chk_obj(param="loop", **kwargs)
        # __loop = self.__chk_loop_obj(**kwargs)
        return Event(loop=__loop)


    def condition(self, **kwargs):
        from asyncio import Condition
        __lock = FeatureUtils.chk_obj(param="lock", **kwargs)
        __loop = FeatureUtils.chk_obj(param="loop", **kwargs)
        # __lock = self.__chk_lock_obj(**kwargs)
        # __loop = self.__chk_loop_obj(**kwargs)
        return Condition(lock=__lock, loop=__loop)


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
        from asyncio.locks import Semaphore
        return Semaphore(value=value)


    def bounded_semaphore(self, value: int):
        from asyncio.locks import BoundedSemaphore
        return BoundedSemaphore(value=value)


    def queue(self, qtype: AsynchronousQueueType):
        return qtype.value()

