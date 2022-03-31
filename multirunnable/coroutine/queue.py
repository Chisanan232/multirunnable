from ..framework.runnable.queue import BaseQueueType as _BaseQueueType
from .. import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
    from gevent.queue import (
        Queue as Greenlet_Queue,
        SimpleQueue as Greenlet_SimpleQueue,
        JoinableQueue as Greenlet_JoinableQueue,
        PriorityQueue as Greenlet_PriorityQueue,
        LifoQueue as Greenlet_LifoQueue)
else:
    from gevent.queue import (
        Queue as Greenlet_Queue,
        JoinableQueue as Greenlet_JoinableQueue,
        PriorityQueue as Greenlet_PriorityQueue,
        LifoQueue as Greenlet_LifoQueue)

from asyncio.queues import (
    Queue as Async_Queue,
    PriorityQueue as Async_PriorityQueue,
    LifoQueue as Async_LifoQueue)

