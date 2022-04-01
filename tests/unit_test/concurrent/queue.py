# from multirunnable.concurrent.queue import ThreadQueueType
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ...test_config import Semaphore_Value

if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION == 6:
    from queue import Queue, LifoQueue, PriorityQueue
else:
    from queue import Queue, SimpleQueue, LifoQueue, PriorityQueue


_Semaphore_Value = Semaphore_Value


# @pytest.fixture(scope="class")
# def mr_queue():
#     return ThreadQueueType


class TestThreadQueue:

    def test_queue(self):
        from multirunnable.concurrent.queue import Thread_Queue
        _queue = Thread_Queue()
        assert isinstance(_queue, Queue) is True, "This type of instance should be 'queue.Queue'."


    if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
        def test_simple_queue(self):
            from multirunnable.concurrent.queue import Thread_SimpleQueue
            _queue = Thread_SimpleQueue()
            assert isinstance(_queue, SimpleQueue) is True, "This type of instance should be 'queue.SimpleQueue'."


    def test_priority_queue(self):
        from multirunnable.concurrent.queue import Thread_PriorityQueue
        _queue = Thread_PriorityQueue()
        assert isinstance(_queue, PriorityQueue) is True, "This type of instance should be 'queue.PriorityQueue'."


    def test_lifo_queue(self):
        from multirunnable.concurrent.queue import Thread_LifoQueue
        _queue = Thread_LifoQueue()
        assert isinstance(_queue, LifoQueue) is True, "This type of instance should be 'queue.LifoQueue'."


