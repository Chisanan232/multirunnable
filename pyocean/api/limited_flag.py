from ..framework.strategy import Globalize as RunningGlobalize

from multiprocessing import Lock as ProcessLock, RLock as ProcessRLock, Semaphore as ProcessSemaphore, BoundedSemaphore as ProcessBoundedSemaphore
from threading import Lock as ThreadLock, RLock as ThreadRLock, Semaphore as ThreadSemaphore, BoundedSemaphore as ThreadBoundedSemaphore
from asyncio.locks import Lock as AsyncLock, Semaphore as AsyncSemaphore, BoundedSemaphore as AsyncBoundedSemaphore
from enum import Enum



class RunningLimitation(Enum):

    pass



class Lock(RunningLimitation):

    Process = ProcessLock
    Thread = ThreadLock
    Coroutine = ThreadLock
    Async = AsyncLock
    Globalize = RunningGlobalize.lock



class RLock(RunningLimitation):

    Process = ProcessRLock
    Thread = ThreadRLock
    Coroutine = ThreadRLock
    Globalize = RunningGlobalize.rlock



class Semaphore(RunningLimitation):

    Process = ProcessSemaphore
    Thread = ThreadSemaphore
    Coroutine = ThreadSemaphore
    Async = AsyncSemaphore
    Globalize = RunningGlobalize.semaphore



class BoundedSemaphore(RunningLimitation):

    Process = ProcessBoundedSemaphore
    Thread = ThreadBoundedSemaphore
    Coroutine = ThreadBoundedSemaphore
    Async = AsyncBoundedSemaphore
    Globalize = RunningGlobalize.semaphore
