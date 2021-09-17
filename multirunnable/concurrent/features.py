from multirunnable.framework.features import (
    PosixThreadLock as _PosixThreadLock,
    PosixThreadCommunication as _PosixThreadCommunication,
    BaseQueueType as _BaseQueueType)

from threading import Lock, RLock, Event, Condition, Semaphore, BoundedSemaphore
from queue import (
    Queue as Thread_Queue,
    SimpleQueue as Thread_SimpleQueue,
    LifoQueue as Thread_LifoQueue,
    PriorityQueue as Thread_PriorityQueue)
from typing import Union


ThreadQueueDataType = Union[Thread_Queue, Thread_SimpleQueue, Thread_LifoQueue, Thread_PriorityQueue]


class MultiThreadingQueueType(_BaseQueueType):

    Queue = Thread_Queue()
    SimpleQueue = Thread_SimpleQueue()
    LifoQueue = Thread_LifoQueue()
    PriorityQueue = Thread_PriorityQueue()



class ThreadLock(_PosixThreadLock):

    def get_lock(self) -> Lock:
        return Lock()


    def get_rlock(self) -> RLock:
        return RLock()


    def get_semaphore(self, value: int, **kwargs) -> Semaphore:
        return Semaphore(value=value)


    def get_bounded_semaphore(self, value: int, **kwargs) -> BoundedSemaphore:
        return BoundedSemaphore(value=value)



class ThreadCommunication(_PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> Event:
        return Event()


    def get_condition(self, *args, **kwargs) -> Condition:
        __lock: Union[Lock, RLock, None] = kwargs.get("lock", None)
        return Condition(lock=__lock)

