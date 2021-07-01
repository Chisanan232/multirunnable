from pyocean.framework.features import PosixThreadLock, PosixThreadCommunication, BaseQueue, BaseAPI, BaseQueueType

from threading import Lock, RLock, Event, Condition, Semaphore, BoundedSemaphore
from queue import (
    Queue as Thread_Queue,
    SimpleQueue as Thread_SimpleQueue,
    LifoQueue as Thread_LifoQueue,
    PriorityQueue as Thread_PriorityQueue)
from typing import Union

from deprecated.sphinx import deprecated



ThreadQueueDataType = Union[Thread_Queue, Thread_SimpleQueue, Thread_LifoQueue, Thread_PriorityQueue]


class MultiThreadingQueueType(BaseQueueType):

    Queue = Thread_Queue()
    SimpleQueue = Thread_SimpleQueue()
    LifoQueue = Thread_LifoQueue()
    PriorityQueue = Thread_PriorityQueue()



class ThreadQueue(BaseQueue):

    def get_queue(self, qtype: MultiThreadingQueueType) -> ThreadQueueDataType:
        return qtype.value



@deprecated(version="0.7", reason="Classify the lock, event and queue to be different class.")
class MultiThreading(BaseAPI):

    def lock(self):
        return Lock()


    def rlock(self):
        return RLock()


    def event(self, **kwargs):
        return Event()


    def condition(self, **kwargs):
        return Condition()


    def semaphore(self, value: int):
        return Semaphore(value=value)


    def bounded_semaphore(self, value: int):
        return BoundedSemaphore(value=value)


    def queue(self, qtype: MultiThreadingQueueType):
        return qtype.value



class ThreadLock(PosixThreadLock):

    def get_lock(self) -> Lock:
        return Lock()


    def get_rlock(self) -> RLock:
        return RLock()


    def get_semaphore(self, value: int) -> Semaphore:
        return Semaphore(value=value)


    def get_bounded_semaphore(self, value: int) -> BoundedSemaphore:
        return BoundedSemaphore(value=value)



class ThreadCommunication(PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> Event:
        return Event()


    def get_condition(self, *args, **kwargs) -> Condition:
        __lock: Union[Lock, RLock, None] = kwargs.get("lock", None)
        return Condition(lock=__lock)

