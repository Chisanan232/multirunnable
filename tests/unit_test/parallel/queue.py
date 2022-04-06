# from multirunnable.parallel.queue import ProcessQueueType

from multiprocessing.queues import Queue, SimpleQueue, JoinableQueue

from ...test_config import Semaphore_Value


_Semaphore_Value = Semaphore_Value


# @pytest.fixture(scope="class")
# def mr_queue():
#     return ProcessQueueType



class TestProcessQueue:

    def test_queue(self):
        from multirunnable.parallel.queue import Queue as Process_Queue
        _queue = Process_Queue()
        assert isinstance(_queue, Queue) is True, "This type of instance should be 'multiprocessing.Queue'."


    def test_simple_queue(self):
        from multirunnable.parallel.queue import SimpleQueue as Process_SimpleQueue
        _queue = Process_SimpleQueue()
        assert isinstance(_queue, SimpleQueue) is True, "This type of instance should be 'multiprocessing.SimpleQueue'."


    def test_joinable_queue(self):
        from multirunnable.parallel.queue import JoinableQueue as Process_JoinableQueue
        _queue = Process_JoinableQueue()
        assert isinstance(_queue, JoinableQueue) is True, "This type of instance should be 'multiprocessing.JoinableQueue'."

