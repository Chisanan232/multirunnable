"""
Annotate all relative object (Queue, Lock, RLock, Semaphore, Bounded Semaphore, Event, Condition) of
'running-strategy' --- multi-threading, multiprocessing, multi-greenlet and asynchronous.

multi-threading:
  No Queue object.
    1. Lock
    2. RLock
    3. Semaphore
    4. Bounded Semaphore
    5. Event
    6. Condition

multiprocessing:
    1. Queue
    2. Lock
    3. RLock
    4. Semaphore
    5. Bounded Semaphore
    6. Event
    7. Condition

multi-greenlet:
  No Lock object.
    1. Queue
    2. RLock
    3. Semaphore
    4. Bounded Semaphore
    5. Event
    6. Condition

asynchronous:
  No RLock object.
    1. Queue
    2. Lock
    3. Semaphore
    4. Bounded Semaphore
    5. Event
    6. Condition

"""

from queue import Queue
from threading import (Thread,
                       Lock as ThreadingLock,
                       RLock as ThreadingRLock,
                       Semaphore as ThreadingSemaphore,
                       BoundedSemaphore as ThreadingBoundedSemaphore,
                       Event as ThreadingEvent,
                       Condition as ThreadingCondition)

from multiprocessing.pool import AsyncResult, ApplyResult
from multiprocessing import (
    Process,
    Queue as MultiProcessingQueue,
    Lock as MultiProcessingLock,
    RLock as MultiProcessingRLock,
    BoundedSemaphore as MultiProcessingBoundedSemaphore,
    Semaphore as MultiProcessingSemaphore,
    Event as MultiProcessingEvent,
    Condition as MultiProcessingCondition)

from gevent.greenlet import Greenlet
from gevent.queue import Queue as GeventQueue
from gevent.lock import (RLock as GeventRLock,
                         Semaphore as GeventSemaphore,
                         BoundedSemaphore as GeventBoundedSemaphore,
                         DummySemaphore as GeventDummySemaphore)
from gevent.event import Event as GeventEvent

from asyncio.tasks import Task
from asyncio.queues import Queue as AsyncIOQueue
from asyncio.locks import (Lock as AsyncIOLock,
                           Semaphore as AsyncIOSemaphore,
                           BoundedSemaphore as AsyncIOBoundedSemaphore,
                           Event as AsyncIOEvent,
                           Condition as AsyncIOCondition)

from typing import Union, NewType


__MRTasks = Union[Thread, Process, AsyncResult, ApplyResult, Greenlet, Task]
MRTasks = NewType("MRTasks", __MRTasks)

__MRQueue = Union[Queue, MultiProcessingQueue, GeventQueue, AsyncIOQueue]
MRQueue = NewType("MRQueue", __MRQueue)

__MRLock = Union[ThreadingLock, MultiProcessingLock, AsyncIOLock]
MRLock = NewType("MRLock", __MRLock)

__MRRLock = Union[ThreadingRLock, MultiProcessingRLock, GeventRLock]
MRRLock = NewType("MRRLock", __MRRLock)

__MRSemaphore = Union[ThreadingSemaphore, MultiProcessingSemaphore, GeventSemaphore, AsyncIOSemaphore]
MRSemaphore = NewType("MRSemaphore", __MRSemaphore)

__MRBoundedSemaphore = Union[ThreadingBoundedSemaphore, MultiProcessingBoundedSemaphore, GeventBoundedSemaphore, AsyncIOBoundedSemaphore]
MRBoundedSemaphore = NewType("MRBoundedSemaphore", __MRBoundedSemaphore)

__MREvent = Union[ThreadingEvent, MultiProcessingEvent, GeventEvent, AsyncIOEvent]
MREvent = NewType("MREvent", __MREvent)

__MRCondition = Union[ThreadingCondition, MultiProcessingCondition, AsyncIOCondition]
MRCondition = NewType("MRCondition", __MRCondition)

__MRFeature = Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]
MRFeature = NewType("MRFeature", __MRFeature)

