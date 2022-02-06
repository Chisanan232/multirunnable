from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from multirunnable.framework.runnable.queue import BaseQueueType as _BaseQueueType

if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
    from gevent.queue import (
        Queue as Greenlet_Queue,
        SimpleQueue as Greenlet_SimpleQueue,
        JoinableQueue as Greenlet_JoinableQueue,
        PriorityQueue as Greenlet_PriorityQueue,
        LifoQueue as Greenlet_LifoQueue)

    # class GeventQueueType(_BaseQueueType):
    #     Queue = _Greenlet_Queue()
    #     SimpleQueue = _Greenlet_SimpleQueue()
    #     JoinableQueue = _Greenlet_JoinableQueue()
    #     PriorityQueue = _Greenlet_PriorityQueue()
    #     LifoQueue = _Greenlet_LifoQueue()

else:
    from gevent.queue import (
        Queue as Greenlet_Queue,
        JoinableQueue as Greenlet_JoinableQueue,
        PriorityQueue as Greenlet_PriorityQueue,
        LifoQueue as Greenlet_LifoQueue)

    # class GeventQueueType(_BaseQueueType):
    #     Queue = _Greenlet_Queue()
    #     JoinableQueue = _Greenlet_JoinableQueue()
    #     PriorityQueue = _Greenlet_PriorityQueue()
    #     LifoQueue = _Greenlet_LifoQueue()

from asyncio.queues import (
    Queue as Async_Queue,
    PriorityQueue as Async_PriorityQueue,
    LifoQueue as Async_LifoQueue)



# class AsynchronousQueueType(_BaseQueueType):
#
#     Queue = _Async_Queue()
#     PriorityQueue = _Async_PriorityQueue()
#     LifoQueue = _Async_LifoQueue()


