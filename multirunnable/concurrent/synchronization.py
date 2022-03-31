from threading import (
    Lock as _Thread_Lock,
    RLock as _Thread_RLock,
    Semaphore as _Thread_Semaphore,
    BoundedSemaphore as _Thread_BoundedSemaphore,
    Event as _Thread_Event,
    Condition as _Thread_Condition)
from typing import Union

from ..framework.runnable.synchronization import (
    PosixThreadLock as _PosixThreadLock,
    PosixThreadCommunication as _PosixThreadCommunication)



class ThreadLock(_PosixThreadLock):

    def get_lock(self, **kwargs) -> _Thread_Lock:
        return _Thread_Lock()


    def get_rlock(self, **kwargs) -> _Thread_RLock:
        return _Thread_RLock()


    def get_semaphore(self, value: int, **kwargs) -> _Thread_Semaphore:
        return _Thread_Semaphore(value=value)


    def get_bounded_semaphore(self, value: int, **kwargs) -> _Thread_BoundedSemaphore:
        return _Thread_BoundedSemaphore(value=value)



class ThreadCommunication(_PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> _Thread_Event:
        return _Thread_Event()


    def get_condition(self, *args, **kwargs) -> _Thread_Condition:
        __lock: Union[_Thread_Lock, _Thread_RLock, None] = kwargs.get("lock", None)
        return _Thread_Condition(lock=__lock)

