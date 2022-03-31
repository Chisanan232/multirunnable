from multiprocessing import Queue, SimpleQueue, JoinableQueue
from typing import Union


ProcessQueueDataType = Union[Queue, SimpleQueue, JoinableQueue]

