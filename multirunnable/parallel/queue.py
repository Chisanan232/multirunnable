from multirunnable.framework.queue import BaseQueueType as _BaseQueueType

from multiprocessing import (
    Queue as Process_Queue,
    SimpleQueue as Process_SimpleQueue,
    JoinableQueue as Process_JoinableQueue)
from typing import Union


ProcessQueueDataType = Union[Process_Queue, Process_SimpleQueue, Process_JoinableQueue]


class ProcessQueueType(_BaseQueueType):

    Queue = Process_Queue()
    SimpleQueue = Process_SimpleQueue()
    JoinableQueue = Process_JoinableQueue()

