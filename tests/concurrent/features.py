from multirunnable.framework.features import PosixThreadLock, PosixThreadCommunication
from multirunnable.concurrent.features import ThreadLock, ThreadCommunication, ThreadQueueType
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ..test_config import Semaphore_Value

from threading import Lock, RLock, Semaphore, BoundedSemaphore, Event, Condition
if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION == 6:
    from queue import Queue, LifoQueue, PriorityQueue
else:
    from queue import Queue, SimpleQueue, LifoQueue, PriorityQueue
import pytest


_Semaphore_Value = Semaphore_Value


@pytest.fixture(scope="class")
def mr_queue():
    return ThreadQueueType


@pytest.fixture(scope="class")
def mr_lock() -> ThreadLock:
    return ThreadLock()


@pytest.fixture(scope="class")
def mr_communication() -> ThreadCommunication:
    return ThreadCommunication()


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



class TestThreadLock:

    def test_get_lock(self, mr_lock: PosixThreadLock):
        _lock = mr_lock.get_lock()
        _thread_lock = Lock()
        assert isinstance(_lock, type(_thread_lock)) is True, f"This type of instance should be 'threading.Lock'."


    def test_get_rlock(self, mr_lock: PosixThreadLock):
        _rlock = mr_lock.get_rlock()
        _thread_rlock = RLock()
        assert isinstance(_rlock, type(_thread_rlock)) is True, f"This type of instance should be 'threading.RLock'."


    def test_get_semaphore(self, mr_lock: PosixThreadLock):
        _semaphore = mr_lock.get_semaphore(value=_Semaphore_Value)
        assert isinstance(_semaphore, Semaphore) is True, f"This type of instance should be 'threading.Semaphore'."


    def test_get_bounded_semaphore(self, mr_lock: PosixThreadLock):
        _bounded_semaphore = mr_lock.get_bounded_semaphore(value=_Semaphore_Value)
        assert isinstance(_bounded_semaphore, BoundedSemaphore) is True, f"This type of instance should be 'threading.BoundedSemaphore'."



class TestThreadCommunication:

    def test_get_event(self, mr_communication: PosixThreadCommunication):
        _event = mr_communication.get_event()
        assert isinstance(_event, Event) is True, f"This type of instance should be 'threading.Event'."


    def test_get_communication(self, mr_communication: PosixThreadCommunication):
        _communication = mr_communication.get_condition()
        assert isinstance(_communication, Condition) is True, f"This type of instance should be 'threading.Condition'."

