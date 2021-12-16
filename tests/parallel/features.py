from multirunnable.framework.features import PosixThreadLock, PosixThreadCommunication
from multirunnable.parallel.features import ProcessLock, ProcessCommunication, ProcessQueueType

from ..test_config import Semaphore_Value

from multiprocessing.synchronize import Lock, RLock, Semaphore, BoundedSemaphore, Event, Condition
from multiprocessing.queues import Queue, SimpleQueue, JoinableQueue
import pytest


_Semaphore_Value = Semaphore_Value


@pytest.fixture(scope="class")
def mr_queue():
    return ProcessQueueType


@pytest.fixture(scope="class")
def mr_lock() -> ProcessLock:
    return ProcessLock()


@pytest.fixture(scope="class")
def mr_communication() -> ProcessCommunication:
    return ProcessCommunication()


class TestProcessQueue:

    def test_queue(self, mr_queue: ProcessQueueType):
        assert isinstance(mr_queue.Queue.value, Queue) is True, f"This type of instance should be 'multiprocessing.Queue'."


    def test_simple_queue(self, mr_queue: ProcessQueueType):
        assert isinstance(mr_queue.SimpleQueue.value, SimpleQueue) is True, f"This type of instance should be 'multiprocessing.SimpleQueue'."


    def test_joinable_queue(self, mr_queue: ProcessQueueType):
        assert isinstance(mr_queue.JoinableQueue.value, JoinableQueue) is True, f"This type of instance should be 'multiprocessing.JoinableQueue'."



class TestProcessLock:

    def test_get_lock(self, mr_lock: PosixThreadLock):
        _lock = mr_lock.get_lock()
        assert isinstance(_lock, Lock) is True, f"This type of instance should be 'multiprocessing.synchronize.Lock'."


    def test_get_rlock(self, mr_lock: PosixThreadLock):
        _rlock = mr_lock.get_rlock()
        assert isinstance(_rlock, RLock) is True, f"This type of instance should be 'multiprocessing.synchronize.RLock'."


    def test_get_semaphore(self, mr_lock: PosixThreadLock):
        _semaphore = mr_lock.get_semaphore(value=_Semaphore_Value)
        assert isinstance(_semaphore, Semaphore) is True, f"This type of instance should be 'multiprocessing.synchronize.Semaphore'."


    def test_get_bounded_semaphore(self, mr_lock: PosixThreadLock):
        _bounded_semaphore = mr_lock.get_bounded_semaphore(value=_Semaphore_Value)
        assert isinstance(_bounded_semaphore, BoundedSemaphore) is True, f"This type of instance should be 'multiprocessing.synchronize.BoundedSemaphore'."



class TestProcessCommunication:

    def test_get_event(self, mr_communication: PosixThreadCommunication):
        _event = mr_communication.get_event()
        assert isinstance(_event, Event) is True, f"This type of instance should be 'multiprocessing.synchronize.Event'."


    def test_get_communication(self, mr_communication: PosixThreadCommunication):
        _communication = mr_communication.get_condition()
        assert isinstance(_communication, Condition) is True, f"This type of instance should be 'multiprocessing.synchronize.Condition'."

