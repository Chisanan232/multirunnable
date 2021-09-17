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
from multiprocessing import (Queue as MultiProcessingQueue,
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


__OceanTasks = Union[Thread, AsyncResult, ApplyResult, Greenlet, Task]
OceanTasks = NewType("OceanTasks", __OceanTasks)

__OceanQueue = Union[Queue, MultiProcessingQueue, GeventQueue, AsyncIOQueue]
OceanQueue = NewType("OceanQueue", __OceanQueue)

__OceanLock = Union[ThreadingLock, MultiProcessingLock, AsyncIOLock]
OceanLock = NewType("OceanLock", __OceanLock)

__OceanRLock = Union[ThreadingRLock, MultiProcessingRLock, GeventRLock]
OceanRLock = NewType("OceanRLock", __OceanRLock)

__OceanSemaphore = Union[ThreadingSemaphore, MultiProcessingSemaphore, GeventSemaphore, AsyncIOSemaphore]
OceanSemaphore = NewType("OceanSemaphore", __OceanSemaphore)

__OceanBoundedSemaphore = Union[ThreadingBoundedSemaphore, MultiProcessingBoundedSemaphore, GeventBoundedSemaphore, AsyncIOBoundedSemaphore]
OceanBoundedSemaphore = NewType("OceanBoundedSemaphore", __OceanBoundedSemaphore)

__OceanEvent = Union[ThreadingEvent, MultiProcessingEvent, GeventEvent, AsyncIOEvent]
OceanEvent = NewType("OceanEvent", __OceanEvent)

__OceanCondition = Union[ThreadingCondition, MultiProcessingCondition, AsyncIOCondition]
OceanCondition = NewType("OceanCondition", __OceanCondition)

__OceanFeature = Union[OceanLock, OceanRLock, OceanSemaphore, OceanBoundedSemaphore, OceanEvent, OceanCondition]
OceanFeature = NewType("OceanFeature", __OceanFeature)

