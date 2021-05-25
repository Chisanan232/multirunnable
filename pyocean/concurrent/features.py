from pyocean.framework.features import BaseAPI, BaseQueueType



class MultiThreadingQueueType(BaseQueueType):

    from queue import (Queue as _Queue, 
                       SimpleQueue as _SimpleQueue, 
                       LifoQueue as _LifoQueue, 
                       PriorityQueue as _PriorityQueue)

    Queue = _Queue()
    SimpleQueue = _SimpleQueue()
    LifoQueue = _LifoQueue()
    PriorityQueue = _PriorityQueue()



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
        return qtype.value
