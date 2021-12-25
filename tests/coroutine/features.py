from multirunnable.framework.features import PosixThreadLock, PosixThreadCommunication
from multirunnable.coroutine.features import (
    GreenThreadLock, GreenThreadCommunication, GeventQueueType,
    AsynchronousLock, AsynchronousCommunication, AsynchronousQueueType
)
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ..test_config import Semaphore_Value

from gevent.threading import Lock as gevent_Lock
from gevent.lock import (
    RLock as gevent_RLock,
    Semaphore as gevent_Semaphore,
    BoundedSemaphore as gevent_BoundedSemaphore)

if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION == 6:
    from gevent.queue import (
        Queue as gevent_Queue,
        LifoQueue as gevent_LifoQueue,
        PriorityQueue as gevent_PriorityQueue,
        JoinableQueue as gevent_JoinableQueue,
        UnboundQueue as gevent_UnboundQueue)
else:
    from gevent.queue import (
        Queue as gevent_Queue,
        SimpleQueue as gevent_SimpleQueue,
        LifoQueue as gevent_LifoQueue,
        PriorityQueue as gevent_PriorityQueue,
        JoinableQueue as gevent_JoinableQueue,
        UnboundQueue as gevent_UnboundQueue)

from asyncio import (
    Lock as async_Lock,
    Semaphore as async_Semaphore,
    BoundedSemaphore as async_BoundedSemaphore,
    Event as async_Event,
    Condition as async_Condition)
from asyncio.queues import (
    Queue as async_Queue,
    LifoQueue as async_LifoQueue,
    PriorityQueue as async_PriorityQueue)
from asyncio import new_event_loop
from typing import Type
import pytest


_Semaphore_Value = Semaphore_Value


@pytest.fixture(scope="class")
def mr_gevent_queue() -> Type[GeventQueueType]:
    return GeventQueueType


@pytest.fixture(scope="class")
def mr_gevent_lock() -> GreenThreadLock:
    return GreenThreadLock()


@pytest.fixture(scope="class")
def mr_gevent_communication() -> GreenThreadCommunication:
    return GreenThreadCommunication()


@pytest.fixture(scope="class")
def mr_async_queue() -> Type[AsynchronousQueueType]:
    return AsynchronousQueueType


@pytest.fixture(scope="class")
def mr_async_lock() -> AsynchronousLock:
    return AsynchronousLock()


@pytest.fixture(scope="class")
def mr_async_communication() -> AsynchronousCommunication:
    return AsynchronousCommunication()


class TestGreenThreadQueue:

    def test_queue(self, mr_gevent_queue: GeventQueueType):
        assert isinstance(mr_gevent_queue.Queue.value, gevent_Queue) is True, f"This type of instance should be 'gevent.queue.Queue'."


    if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
        def test_simple_queue(self, mr_gevent_queue: GeventQueueType):
            assert isinstance(mr_gevent_queue.SimpleQueue.value, gevent_SimpleQueue) is True, f"This type of instance should be 'gevent.queue.SimpleQueue'."


    def test_priority_queue(self, mr_gevent_queue: GeventQueueType):
        assert isinstance(mr_gevent_queue.PriorityQueue.value, gevent_PriorityQueue) is True, f"This type of instance should be 'gevent.queue.PriorityQueue'."


    def test_lifo_queue(self, mr_gevent_queue: GeventQueueType):
        assert isinstance(mr_gevent_queue.LifoQueue.value, gevent_LifoQueue) is True, f"This type of instance should be 'gevent.queue.LifoQueue'."


    def test_joinable_queue(self, mr_gevent_queue: GeventQueueType):
        assert isinstance(mr_gevent_queue.JoinableQueue.value, gevent_JoinableQueue) is True, f"This type of instance should be 'gevent.queue.JoinableQueue'."


    def test_unbounded_queue(self, mr_gevent_queue: GeventQueueType):
        pass
        # assert isinstance(mr_queue.value, gevent_UnboundQueue) is True, f"This type of instance should be 'gevent.queue.UnboundQueue'."



class TestGreenThreadLock:

    def test_get_lock(self, mr_gevent_lock: PosixThreadLock):
        _lock = mr_gevent_lock.get_lock()
        assert isinstance(_lock, gevent_Lock) is True, f"This type of instance should be 'gevent.threading.Lock'."


    def test_get_rlock(self, mr_gevent_lock: PosixThreadLock):
        _rlock = mr_gevent_lock.get_rlock()
        assert isinstance(_rlock, gevent_RLock) is True, f"This type of instance should be 'gevent.lock.RLock'."


    def test_get_semaphore(self, mr_gevent_lock: PosixThreadLock):
        _semaphore = mr_gevent_lock.get_semaphore(value=_Semaphore_Value)
        assert isinstance(_semaphore, gevent_Semaphore) is True, f"This type of instance should be 'gevent.lock.Semaphore'."


    def test_get_bounded_semaphore(self, mr_gevent_lock: PosixThreadLock):
        _bounded_semaphore = mr_gevent_lock.get_bounded_semaphore(value=_Semaphore_Value)
        assert isinstance(_bounded_semaphore, gevent_BoundedSemaphore) is True, f"This type of instance should be 'gevent.lock.BoundedSemaphore'."



class TestGreenThreadCommunication:

    def test_get_event(self, mr_gevent_communication: PosixThreadCommunication):
        pass
        # _event = mr_communication.get_event()
        # assert isinstance(_event, Event) is True, f"This type of instance should be 'gevent.lock.Event'."


    def test_get_communication(self, mr_gevent_communication: PosixThreadCommunication):
        pass
        # _communication = mr_communication.get_condition()
        # assert isinstance(_communication, Condition) is True, f"This type of instance should be 'gevent.lock.Condition'."



class TestAsynchronousQueue:

    def test_queue(self, mr_async_queue: AsynchronousQueueType):
        assert isinstance(mr_async_queue.Queue.value, async_Queue) is True, f"This type of instance should be 'asyncio.queues.Queue'."


    def test_priority_queue(self, mr_async_queue: AsynchronousQueueType):
        assert isinstance(mr_async_queue.PriorityQueue.value, async_PriorityQueue) is True, f"This type of instance should be 'asyncio.queues.PriorityQueue'."


    def test_lifo_queue(self, mr_async_queue: AsynchronousQueueType):
        assert isinstance(mr_async_queue.LifoQueue.value, async_LifoQueue) is True, f"This type of instance should be 'asyncio.queues.LifoQueue'."



class TestAsynchronousLock:

    def test_get_lock(self, mr_async_lock: PosixThreadLock):
        try:
            _lock = mr_async_lock.get_lock()
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), f"The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _lock = mr_async_lock.get_lock(loop=_event_loop)
        assert isinstance(_lock, async_Lock) is True, f"This type of instance should be 'asyncio.lock.RLock'."


    def test_get_rlock(self, mr_async_lock: PosixThreadLock):
        try:
            _rlock = mr_async_lock.get_rlock()
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), f"The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _rlock = mr_async_lock.get_rlock(loop=_event_loop)
        assert isinstance(_rlock, async_Lock) is True, f"This type of instance should be 'asyncio.lock.RLock'."


    def test_get_semaphore(self, mr_async_lock: PosixThreadLock):
        try:
            _semaphore = mr_async_lock.get_semaphore(value=_Semaphore_Value)
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), f"The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _semaphore = mr_async_lock.get_semaphore(loop=_event_loop, value=_Semaphore_Value)
        assert isinstance(_semaphore, async_Semaphore) is True, f"This type of instance should be 'asyncio.lock.Semaphore'."


    def test_get_bounded_semaphore(self, mr_async_lock: PosixThreadLock):
        try:
            _bounded_semaphore = mr_async_lock.get_bounded_semaphore(value=_Semaphore_Value)
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), f"The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _bounded_semaphore = mr_async_lock.get_bounded_semaphore(loop=_event_loop, value=_Semaphore_Value)
        assert isinstance(_bounded_semaphore, async_BoundedSemaphore) is True, f"This type of instance should be 'asyncio.lock.BoundedSemaphore'."



class TestAsynchronousCommunication:

    def test_get_event(self, mr_async_communication: PosixThreadCommunication):
        try:
            _event = mr_async_communication.get_event()
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), f"The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _event = mr_async_communication.get_event(loop=_event_loop)
        assert isinstance(_event, async_Event) is True, f"This type of instance should be 'asyncio.Event'."


    def test_get_communication(self, mr_async_communication: PosixThreadCommunication):
        try:
            _communication = mr_async_communication.get_condition()
        except ValueError as e:
            assert "Async Event Loop object cannot be empty" in str(e), f"The exception error should be 'Async Event Loop object cannot be empty'."

        _event_loop = new_event_loop()
        _communication = mr_async_communication.get_condition(loop=_event_loop)
        assert isinstance(_communication, async_Condition) is True, f"This type of instance should be 'asyncio.Condition'."


