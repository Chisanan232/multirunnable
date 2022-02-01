from multirunnable.coroutine.queue import GeventQueueType, AsynchronousQueueType
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ..test_config import Semaphore_Value

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

from asyncio.queues import (
    Queue as async_Queue,
    LifoQueue as async_LifoQueue,
    PriorityQueue as async_PriorityQueue)
from typing import Type
import pytest


_Semaphore_Value = Semaphore_Value


@pytest.fixture(scope="class")
def mr_gevent_queue() -> Type[GeventQueueType]:
    return GeventQueueType


@pytest.fixture(scope="class")
def mr_async_queue() -> Type[AsynchronousQueueType]:
    return AsynchronousQueueType



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



class TestAsynchronousQueue:

    def test_queue(self, mr_async_queue: AsynchronousQueueType):
        assert isinstance(mr_async_queue.Queue.value, async_Queue) is True, f"This type of instance should be 'asyncio.queues.Queue'."


    def test_priority_queue(self, mr_async_queue: AsynchronousQueueType):
        assert isinstance(mr_async_queue.PriorityQueue.value, async_PriorityQueue) is True, f"This type of instance should be 'asyncio.queues.PriorityQueue'."


    def test_lifo_queue(self, mr_async_queue: AsynchronousQueueType):
        assert isinstance(mr_async_queue.LifoQueue.value, async_LifoQueue) is True, f"This type of instance should be 'asyncio.queues.LifoQueue'."


