from typing import Type
import threading
import pytest

from multirunnable.concurrent.context import context

from ..._examples import RunByStrategy
from ..framework.context import _Function, ContextTestSpec



class _ConcurrentFunction(_Function):

    @property
    def worker_context(self) -> Type[context]:
        return context


    def get_current_worker(self):
        return threading.current_thread()


    def get_parent_worker(self):
        return threading.main_thread()


    def get_current_worker_is_parent(self):
        _checksum = threading.current_thread() is threading.main_thread()
        return _checksum


    def get_current_worker_ident(self):
        return threading.current_thread().ident


    def get_current_worker_name(self):
        return threading.current_thread().name


    def get_current_worker_is_alive(self):
        return threading.current_thread().is_alive()


    def get_activate_count(self):
        return threading.active_count()


    def get_activate_children(self):
        return threading.enumerate()



class TestParallelContext(ContextTestSpec):

    @pytest.fixture(scope='class')
    def testing_func(self) -> _Function:
        return _ConcurrentFunction(py_pkg="threading")


    @pytest.fixture(scope='class')
    def running_func(self):
        return RunByStrategy.Concurrent

