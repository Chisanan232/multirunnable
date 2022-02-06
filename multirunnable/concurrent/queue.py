from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
# from multirunnable.framework.runnable.queue import BaseQueueType as _BaseQueueType

from typing import Union


if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
    from queue import (
        Queue as Thread_Queue,
        SimpleQueue as Thread_SimpleQueue,
        LifoQueue as Thread_LifoQueue,
        PriorityQueue as Thread_PriorityQueue)

    # class ThreadQueueType(_BaseQueueType):
    #     Queue = Thread_Queue()
    #     SimpleQueue = Thread_SimpleQueue()
    #     LifoQueue = Thread_LifoQueue()
    #     PriorityQueue = Thread_PriorityQueue()

    ThreadQueueDataType = Union[Thread_Queue, Thread_SimpleQueue, Thread_LifoQueue, Thread_PriorityQueue]

else:
    from queue import (
        Queue as Thread_Queue,
        LifoQueue as Thread_LifoQueue,
        PriorityQueue as Thread_PriorityQueue)

    # class ThreadQueueType(_BaseQueueType):
    #     Queue = Thread_Queue()
    #     LifoQueue = Thread_LifoQueue()
    #     PriorityQueue = Thread_PriorityQueue()

    ThreadQueueDataType = Union[Thread_Queue, Thread_LifoQueue, Thread_PriorityQueue]

