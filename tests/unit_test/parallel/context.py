from typing import Type
import multiprocessing
import pytest

from multirunnable.parallel.context import context
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ..framework.context import _Function, ContextTestSpec
from ..._examples import RunByStrategy



class _ParallelFunction(_Function):

    @property
    def worker_context(self) -> Type[context]:
        return context


    def get_current_worker(self):
        _current_process = multiprocessing.current_process()
        return _current_process


    def get_parent_worker(self):
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 7):
            _parent_process = multiprocessing.parent_process()
            return _parent_process


    def get_current_worker_is_parent(self):
        _checksum = multiprocessing.current_process().name == "MainProcess"
        return _checksum


    def get_current_worker_ident(self):
        _current_process_ident = multiprocessing.current_process().ident
        return _current_process_ident


    def get_current_worker_name(self):
        _current_process_name = multiprocessing.current_process().name
        return _current_process_name


    def get_current_worker_is_alive(self):
        _current_process_is_alive = multiprocessing.current_process().is_alive()
        return _current_process_is_alive


    def get_activate_count(self):
        _active_children_process = multiprocessing.active_children()
        return len(_active_children_process)


    def get_activate_children(self):
        _active_children_process = multiprocessing.active_children()
        return _active_children_process



class TestParallelContext(ContextTestSpec):

    @pytest.fixture(scope='class')
    def testing_func(self) -> _Function:
        return _ParallelFunction(py_pkg="multiprocessing")


    @pytest.fixture(scope='class')
    def running_func(self):
        return RunByStrategy.Parallel


    @pytest.mark.skipif((PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 7), reason="It doesn't support to get parent process via APIs of multiprocessing less than Python 3.8.")
    def test_get_parent_worker(self, running_func, testing_func):
        super(TestParallelContext, self).test_get_parent_worker(running_func=running_func, testing_func=testing_func)

