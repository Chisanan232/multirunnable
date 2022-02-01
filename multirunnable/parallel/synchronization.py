from multirunnable.framework.synchronization import (
    PosixThreadLock as _PosixThreadLock,
    PosixThreadCommunication as _PosixThreadCommunication)

from multiprocessing import Lock, RLock, Event, Condition, Semaphore, BoundedSemaphore
from typing import Union



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

