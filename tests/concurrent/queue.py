from multirunnable.concurrent.queue import ThreadQueueType
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ..test_config import Semaphore_Value

if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION == 6:
    from queue import Queue, LifoQueue, PriorityQueue
else:
    from queue import Queue, SimpleQueue, LifoQueue, PriorityQueue
import pytest


_Semaphore_Value = Semaphore_Value


@pytest.fixture(scope="class")
def mr_queue():
    return ThreadQueueType


class TestThreadQueue:

    def test_queue(self, mr_queue: ThreadQueueType):
        assert isinstance(mr_queue.Queue.value, Queue) is True, f"This type of instance should be 'queue.Queue'."


    if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
        def test_simple_queue(self, mr_queue: ThreadQueueType):
            assert isinstance(mr_queue.SimpleQueue.value, SimpleQueue) is True, f"This type of instance should be 'queue.SimpleQueue'."


    def test_priority_queue(self, mr_queue: ThreadQueueType):
        assert isinstance(mr_queue.PriorityQueue.value, PriorityQueue) is True, f"This type of instance should be 'queue.PriorityQueue'."


    def test_lifo_queue(self, mr_queue: ThreadQueueType):
        assert isinstance(mr_queue.LifoQueue.value, LifoQueue) is True, f"This type of instance should be 'queue.LifoQueue'."


