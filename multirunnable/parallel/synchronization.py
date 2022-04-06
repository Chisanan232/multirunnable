from multiprocessing import (
    Lock as _Process_Lock, RLock as _Process_RLock,
    Semaphore as _Process_Semaphore, BoundedSemaphore as _Process_BoundedSemaphore,
    Event as _Process_Event, Condition as _Process_Condition)
from typing import Union

from ..framework.runnable import (
    PosixThreadLock as _PosixThreadLock,
    PosixThreadCommunication as _PosixThreadCommunication)



class ProcessLock(_PosixThreadLock):

    def get_lock(self, **kwargs) -> _Process_Lock:
        return _Process_Lock()


    def get_rlock(self, **kwargs) -> _Process_RLock:
        return _Process_RLock()


    def get_semaphore(self, value: int, **kwargs) -> _Process_Semaphore:
        return _Process_Semaphore(value=value)


    def get_bounded_semaphore(self, value: int, **kwargs) -> _Process_BoundedSemaphore:
        return _Process_BoundedSemaphore(value=value)



class ProcessCommunication(_PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> _Process_Event:
        return _Process_Event()


    def get_condition(self, *args, **kwargs) -> _Process_Condition:
        __lock: Union[_Process_Lock, _Process_RLock, None] = kwargs.get("lock", None)
        return _Process_Condition(lock=__lock)

