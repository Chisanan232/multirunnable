from gevent.threading import Lock as gevent_Lock
from gevent.lock import (
    RLock as gevent_RLock,
    Semaphore as gevent_Semaphore,
    BoundedSemaphore as gevent_BoundedSemaphore)

from asyncio import (
    Lock as async_Lock,
    Semaphore as async_Semaphore,
    BoundedSemaphore as async_BoundedSemaphore,
    Event as async_Event,
    Condition as async_Condition)
from asyncio import new_event_loop
import pytest

from multirunnable.framework.runnable.synchronization import PosixThreadLock, PosixThreadCommunication
from multirunnable.coroutine.synchronization import (
    GreenThreadLock, GreenThreadCommunication,
    AsynchronousLock, AsynchronousCommunication
)

from ...test_config import Semaphore_Value


_Semaphore_Value = Semaphore_Value


@pytest.fixture(scope="class")
def mr_gevent_lock() -> GreenThreadLock:
    return GreenThreadLock()


@pytest.fixture(scope="class")
def mr_gevent_communication() -> GreenThreadCommunication:
    return GreenThreadCommunication()


@pytest.fixture(scope="class")
def mr_async_lock() -> AsynchronousLock:
    return AsynchronousLock()


@pytest.fixture(scope="class")
def mr_async_communication() -> AsynchronousCommunication:
    return AsynchronousCommunication()



class TestGreenThreadLock:

    def test_get_lock(self, mr_gevent_lock: PosixThreadLock):
        _lock = mr_gevent_lock.get_lock()
        assert isinstance(_lock, gevent_Lock) is True, "This type of instance should be 'gevent.threading.Lock'."


    def test_get_rlock(self, mr_gevent_lock: PosixThreadLock):
        _rlock = mr_gevent_lock.get_rlock()
        assert isinstance(_rlock, gevent_RLock) is True, "This type of instance should be 'gevent.lock.RLock'."


    def test_get_semaphore(self, mr_gevent_lock: PosixThreadLock):
        _semaphore = mr_gevent_lock.get_semaphore(value=_Semaphore_Value)
        assert isinstance(_semaphore, gevent_Semaphore) is True, "This type of instance should be 'gevent.lock.Semaphore'."


    def test_get_bounded_semaphore(self, mr_gevent_lock: PosixThreadLock):
        _bounded_semaphore = mr_gevent_lock.get_bounded_semaphore(value=_Semaphore_Value)
        assert isinstance(_bounded_semaphore, gevent_BoundedSemaphore) is True, "This type of instance should be 'gevent.lock.BoundedSemaphore'."



class TestGreenThreadCommunication:

    def test_get_event(self, mr_gevent_communication: PosixThreadCommunication):
        pass
        # _event = mr_communication.get_event()
        # assert isinstance(_event, Event) is True, "This type of instance should be 'gevent.lock.Event'."


    def test_get_communication(self, mr_gevent_communication: PosixThreadCommunication):
        pass
        # _communication = mr_communication.get_condition()
        # assert isinstance(_communication, Condition) is True, "This type of instance should be 'gevent.lock.Condition'."



class TestAsynchronousLock:

    def test_get_lock(self, mr_async_lock: PosixThreadLock):
        try:
            _lock = mr_async_lock.get_lock()
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), "The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _lock = mr_async_lock.get_lock(loop=_event_loop)
        assert isinstance(_lock, async_Lock) is True, "This type of instance should be 'asyncio.lock.RLock'."


    def test_get_rlock(self, mr_async_lock: PosixThreadLock):
        try:
            _rlock = mr_async_lock.get_rlock()
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), "The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _rlock = mr_async_lock.get_rlock(loop=_event_loop)
        assert isinstance(_rlock, async_Lock) is True, "This type of instance should be 'asyncio.lock.RLock'."


    def test_get_semaphore(self, mr_async_lock: PosixThreadLock):
        try:
            _semaphore = mr_async_lock.get_semaphore(value=_Semaphore_Value)
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), "The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _semaphore = mr_async_lock.get_semaphore(loop=_event_loop, value=_Semaphore_Value)
        assert isinstance(_semaphore, async_Semaphore) is True, "This type of instance should be 'asyncio.lock.Semaphore'."


    def test_get_bounded_semaphore(self, mr_async_lock: PosixThreadLock):
        try:
            _bounded_semaphore = mr_async_lock.get_bounded_semaphore(value=_Semaphore_Value)
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), "The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _bounded_semaphore = mr_async_lock.get_bounded_semaphore(loop=_event_loop, value=_Semaphore_Value)
        assert isinstance(_bounded_semaphore, async_BoundedSemaphore) is True, "This type of instance should be 'asyncio.lock.BoundedSemaphore'."



class TestAsynchronousCommunication:

    def test_get_event(self, mr_async_communication: PosixThreadCommunication):
        try:
            _event = mr_async_communication.get_event()
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), "The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _event = mr_async_communication.get_event(loop=_event_loop)
        assert isinstance(_event, async_Event) is True, "This type of instance should be 'asyncio.Event'."


    def test_get_communication(self, mr_async_communication: PosixThreadCommunication):
        try:
            _communication = mr_async_communication.get_condition()
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), "The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _communication = mr_async_communication.get_condition(loop=_event_loop)
        assert isinstance(_communication, async_Condition) is True, "This type of instance should be 'asyncio.Condition'."


