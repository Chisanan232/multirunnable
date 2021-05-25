from threading import (Lock as ThreadingLock,
                       RLock as ThreadingRLock,
                       Semaphore as ThreadingSemaphore,
                       BoundedSemaphore as ThreadingBoundedSemaphore,
                       Event as ThreadingEvent,
                       Condition as ThreadingCondition)
from multiprocessing import (Queue as MultiProcessingQueue,
                             Lock as MultiProcessingLock,
                             RLock as MultiProcessingRLock,
                             BoundedSemaphore as MultiProcessingBoundedSemaphore,
                             Semaphore as MultiProcessingSemaphore,
                             Event as MultiProcessingEvent,
                             Condition as MultiProcessingCondition)
from gevent.queue import Queue as GeventQueue
from gevent.lock import RLock as GeventRLock, Semaphore as GeventSemaphore, BoundedSemaphore as GeventBoundedSemaphore
from gevent.event import Event as GeventEvent
from queue import Queue
from typing import Union


OceanQueue = Union[Queue, MultiProcessingQueue, GeventQueue]
OceanLock = Union[ThreadingLock, MultiProcessingLock]
OceanRLock = Union[ThreadingRLock, MultiProcessingRLock, GeventRLock]
OceanSemaphore = Union[ThreadingSemaphore, MultiProcessingSemaphore, GeventSemaphore]
OceanBoundedSemaphore = Union[ThreadingBoundedSemaphore, MultiProcessingBoundedSemaphore, GeventBoundedSemaphore]
OceanEvent = Union[ThreadingEvent, MultiProcessingEvent, GeventEvent]
OceanCondition = Union[ThreadingCondition, MultiProcessingCondition]
