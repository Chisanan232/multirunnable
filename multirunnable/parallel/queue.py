from typing import Union
from multiprocessing import Queue, SimpleQueue, JoinableQueue


ProcessQueueDataType = Union[Queue, SimpleQueue, JoinableQueue]

