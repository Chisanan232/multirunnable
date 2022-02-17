from multirunnable.coroutine.context import green_thread_context, async_task_context

from ..framework.context import _Function, ContextTestSpec
from .._examples import run_multi_green_thread, run_async

from typing import Type
import asyncio
import gevent.threading
import gevent
import pytest



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
        return threading.active_count()


    def get_activate_children(self):
        return threading.enumerate()



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
    def testing_func(self) -> _Function:
        return _GreenThreadFunction(py_pkg="gevent")


    @pytest.fixture(scope='class')
    def running_func(self):
        return run_multi_green_thread


    @pytest.mark.skip(reason="Python package *gevent* doesn't support this feature. MultiRunnable doesn't implement it currently.")
    def test_activate_workers_count(self, running_func, testing_func):
        pass


    @pytest.mark.skip(reason="Python package *gevent* doesn't support this feature. MultiRunnable doesn't implement it currently.")
    def test_children_workers(self, running_func, testing_func):
        pass



class TestAsynchronousTaskContext(ContextTestSpec):

    @pytest.fixture(scope='class')
    def testing_func(self) -> _Function:
        return _AsyncTaskFunction(py_pkg="asyncio")


    @pytest.fixture(scope='class')
    def running_func(self):
        return run_async

