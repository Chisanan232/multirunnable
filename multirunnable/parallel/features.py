from multirunnable.framework.features import (
    PosixThreadLock as _PosixThreadLock,
    PosixThreadCommunication as _PosixThreadCommunication,
    BaseQueueType as _BaseQueueType)

from multiprocessing import Lock, RLock, Event, Condition, Semaphore, BoundedSemaphore
from multiprocessing import (
    Queue as Process_Queue,
    SimpleQueue as Process_SimpleQueue,
    JoinableQueue as Process_JoinableQueue)
from typing import Union


ProcessQueueDataType = Union[Process_Queue, Process_SimpleQueue, Process_JoinableQueue]


class MultiProcessingQueueType(_BaseQueueType):

    Queue = Process_Queue()
    SimpleQueue = Process_SimpleQueue()
    JoinableQueue = Process_JoinableQueue()



class ProcessLock(_PosixThreadLock):

    def get_lock(self) -> Lock:
        return Lock()


    def get_rlock(self) -> RLock:
        return RLock()


    def get_semaphore(self, value: int, **kwargs) -> Semaphore:
        return Semaphore(value=value)


    def get_bounded_semaphore(self, value: int, **kwargs) -> BoundedSemaphore:
        return BoundedSemaphore(value=value)



class ProcessCommunication(_PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> Event:
        return Event()


    def get_condition(self, *args, **kwargs) -> Condition:
        __lock: Union[Lock, RLock, None] = kwargs.get("lock", None)
        return Condition(lock=__lock)

