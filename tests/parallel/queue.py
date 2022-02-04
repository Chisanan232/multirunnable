from multirunnable.parallel.queue import ProcessQueueType

from ..test_config import Semaphore_Value

from multiprocessing.queues import Queue, SimpleQueue, JoinableQueue
import pytest


_Semaphore_Value = Semaphore_Value


@pytest.fixture(scope="class")
def mr_queue():
    return ProcessQueueType



class TestProcessQueue:

    def test_queue(self, mr_queue: ProcessQueueType):
        assert isinstance(mr_queue.Queue.value, Queue) is True, "This type of instance should be 'multiprocessing.Queue'."


    def test_simple_queue(self, mr_queue: ProcessQueueType):
        assert isinstance(mr_queue.SimpleQueue.value, SimpleQueue) is True, "This type of instance should be 'multiprocessing.SimpleQueue'."


    def test_joinable_queue(self, mr_queue: ProcessQueueType):
        assert isinstance(mr_queue.JoinableQueue.value, JoinableQueue) is True, "This type of instance should be 'multiprocessing.JoinableQueue'."

