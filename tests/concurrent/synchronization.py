from multirunnable.framework.synchronization import PosixThreadLock, PosixThreadCommunication
from multirunnable.concurrent.synchronization import ThreadLock, ThreadCommunication

from ..test_config import Semaphore_Value

from threading import Lock, RLock, Semaphore, BoundedSemaphore, Event, Condition
import pytest


_Semaphore_Value = Semaphore_Value


@pytest.fixture(scope="class")
def mr_lock() -> ThreadLock:
    return ThreadLock()


@pytest.fixture(scope="class")
def mr_communication() -> ThreadCommunication:
    return ThreadCommunication()



class TestThreadLock:

    def test_get_lock(self, mr_lock: PosixThreadLock):
        _lock = mr_lock.get_lock()
        _thread_lock = Lock()
        assert isinstance(_lock, type(_thread_lock)) is True, "This type of instance should be 'threading.Lock'."


    def test_get_rlock(self, mr_lock: PosixThreadLock):
        _rlock = mr_lock.get_rlock()
        _thread_rlock = RLock()
        assert isinstance(_rlock, type(_thread_rlock)) is True, "This type of instance should be 'threading.RLock'."


    def test_get_semaphore(self, mr_lock: PosixThreadLock):
        _semaphore = mr_lock.get_semaphore(value=_Semaphore_Value)
        assert isinstance(_semaphore, Semaphore) is True, "This type of instance should be 'threading.Semaphore'."


    def test_get_bounded_semaphore(self, mr_lock: PosixThreadLock):
        _bounded_semaphore = mr_lock.get_bounded_semaphore(value=_Semaphore_Value)
        assert isinstance(_bounded_semaphore, BoundedSemaphore) is True, "This type of instance should be 'threading.BoundedSemaphore'."



class TestThreadCommunication:

    def test_get_event(self, mr_communication: PosixThreadCommunication):
        _event = mr_communication.get_event()
        assert isinstance(_event, Event) is True, "This type of instance should be 'threading.Event'."


    def test_get_communication(self, mr_communication: PosixThreadCommunication):
        _communication = mr_communication.get_condition()
        assert isinstance(_communication, Condition) is True, "This type of instance should be 'threading.Condition'."

