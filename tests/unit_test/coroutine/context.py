from typing import Type
import gevent.threading
import asyncio
import gevent
import pytest

from multirunnable.coroutine.context import green_thread_context, async_task_context

from ..._examples import RunByStrategy
from ..framework.context import _Function, ContextTestSpec



class _GreenThreadFunction(_Function):

    @property
    def worker_context(self) -> Type[green_thread_context]:
        return green_thread_context


    def get_current_worker(self):
        return gevent.getcurrent()


    def get_parent_worker(self):
        return gevent.threading.main_native_thread()


    def get_current_worker_is_parent(self):
        _checksum = gevent.getcurrent() is gevent.threading.main_native_thread()
        return _checksum


    def get_current_worker_ident(self):
        return str(gevent.threading.get_ident)


    def get_current_worker_name(self):
        return str(gevent.getcurrent().name)


    def get_current_worker_is_alive(self):
        return gevent.getcurrent().dead is not True


    def get_activate_count(self):
        return gevent.threading.__threading__.active_count()


    def get_activate_children(self):
        return gevent.threading.__threading__.enumerate()



class _AsyncTaskFunction(_Function):

    @property
    def worker_context(self) -> Type[async_task_context]:
        return async_task_context


    def get_current_worker(self):
        return gevent.getcurrent()


    def get_parent_worker(self):
        return asyncio.Task.current_task()


    def get_current_worker_is_parent(self):
        return True


    def get_current_worker_ident(self):
        return str(id(async_task_context.get_current_worker()))


    def get_current_worker_name(self):
        return str(async_task_context.get_current_worker().get_name())


    def get_current_worker_is_alive(self):
        return asyncio.Task.current_task().done() is False


    def get_activate_count(self):
        return len(asyncio.Task.all_tasks())


    def get_activate_children(self):
        return asyncio.Task.all_tasks()



class TestGreenThreadContext(ContextTestSpec):

    @pytest.fixture(scope='class')
    def testing_func(self) -> _GreenThreadFunction:
        return _GreenThreadFunction(py_pkg="gevent")


    @pytest.fixture(scope='class')
    def running_func(self):
        return RunByStrategy.CoroutineWithGreenThread



class TestAsynchronousTaskContext(ContextTestSpec):

    @pytest.fixture(scope='class')
    def testing_func(self) -> _Function:
        return _AsyncTaskFunction(py_pkg="asyncio")


    @pytest.fixture(scope='class')
    def running_func(self):
        return RunByStrategy.CoroutineWithAsynchronous

