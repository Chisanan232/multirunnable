from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ...test_config import Semaphore_Value

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
import asyncio
import pytest


_Semaphore_Value = Semaphore_Value


# @pytest.fixture(scope="class")
# def mr_gevent_queue() -> Type[GeventQueueType]:
#     return GeventQueueType
#
#
# @pytest.fixture(scope="class")
# def mr_async_queue() -> Type[AsynchronousQueueType]:
#     return AsynchronousQueueType



class TestGreenThreadQueue:

    def test_queue(self):
        from multirunnable.coroutine.queue import Greenlet_Queue
        _queue = Greenlet_Queue()
        assert isinstance(_queue, gevent_Queue) is True, "This type of instance should be 'gevent.queue.Queue'."


    if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
        def test_simple_queue(self):
            from multirunnable.coroutine.queue import Greenlet_SimpleQueue
            _queue = Greenlet_SimpleQueue()
            assert isinstance(_queue, gevent_SimpleQueue) is True, "This type of instance should be 'gevent.queue.SimpleQueue'."


    def test_priority_queue(self):
        from multirunnable.coroutine.queue import Greenlet_PriorityQueue
        _queue = Greenlet_PriorityQueue()
        assert isinstance(_queue, gevent_PriorityQueue) is True, "This type of instance should be 'gevent.queue.PriorityQueue'."


    def test_lifo_queue(self):
        from multirunnable.coroutine.queue import Greenlet_LifoQueue
        _queue = Greenlet_LifoQueue()
        assert isinstance(_queue, gevent_LifoQueue) is True, "This type of instance should be 'gevent.queue.LifoQueue'."


    def test_joinable_queue(self):
        from multirunnable.coroutine.queue import Greenlet_JoinableQueue
        _queue = Greenlet_JoinableQueue()
        assert isinstance(_queue, gevent_JoinableQueue) is True, "This type of instance should be 'gevent.queue.JoinableQueue'."


    @pytest.mark.skip(reason="Not implement this testing logic.")
    def test_unbounded_queue(self):
        from multirunnable.coroutine.queue import Greenlet_UnboundQueue
        _queue = Greenlet_UnboundQueue()
        assert isinstance(_queue, gevent_UnboundQueue) is True, "This type of instance should be 'gevent.queue.UnboundQueue'."



class TestAsynchronousQueue:

    def test_queue(self):
        from multirunnable.coroutine.queue import Async_Queue

        _new_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_new_event_loop)

        _queue = Async_Queue()
        assert isinstance(_queue, async_Queue) is True, "This type of instance should be 'asyncio.queues.Queue'."


    def test_priority_queue(self):
        from multirunnable.coroutine.queue import Async_PriorityQueue

        _new_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_new_event_loop)

        _queue = Async_PriorityQueue()
        assert isinstance(_queue, async_PriorityQueue) is True, "This type of instance should be 'asyncio.queues.PriorityQueue'."


    def test_lifo_queue(self):
        from multirunnable.coroutine.queue import Async_LifoQueue

        _new_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_new_event_loop)

        _queue = Async_LifoQueue()
        assert isinstance(_queue, async_LifoQueue) is True, "This type of instance should be 'asyncio.queues.LifoQueue'."


