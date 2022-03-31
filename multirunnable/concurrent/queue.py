from typing import Union

from .. import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION


if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
    from queue import (
        Queue as Thread_Queue,
        SimpleQueue as Thread_SimpleQueue,
        LifoQueue as Thread_LifoQueue,
        PriorityQueue as Thread_PriorityQueue)

    ThreadQueueDataType = Union[Thread_Queue, Thread_SimpleQueue, Thread_LifoQueue, Thread_PriorityQueue]

else:
    from queue import (
        Queue as Thread_Queue,
        LifoQueue as Thread_LifoQueue,
        PriorityQueue as Thread_PriorityQueue)

    ThreadQueueDataType = Union[Thread_Queue, Thread_LifoQueue, Thread_PriorityQueue]

