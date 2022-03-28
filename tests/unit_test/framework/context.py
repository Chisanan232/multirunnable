from multirunnable.framework.runnable.context import BaseContext

from abc import ABCMeta, abstractmethod
from typing import Type
import pytest



class _Function(metaclass=ABCMeta):

    def __init__(self, py_pkg: str):
        self._py_pkg = py_pkg


    @property
    @abstractmethod
    def worker_context(self) -> Type[BaseContext]:
        pass


    def func_to_get_current_worker(self):
        _worker_str = _Function._get_worker_name(pkg=self._py_pkg)
        _current_process = self.get_current_worker()
        _mr_current_process = self.worker_context.get_current_worker()
        assert _current_process is _mr_current_process, f"The current {_worker_str} we got should be same as the {_worker_str} it returns via Python package '{self._py_pkg}'."


    @abstractmethod
    def get_current_worker(self):
        pass


    def func_to_get_parent_worker(self):
        _worker_str = _Function._get_worker_name(pkg=self._py_pkg)
        _parent_process = self.get_parent_worker()
        _mr_parent_process = self.worker_context.get_parent_worker()
        assert _parent_process is _mr_parent_process, f"The parent {_worker_str} we got should be same as the {_worker_str} it returns via Python package '{self._py_pkg}'."


    @abstractmethod
    def get_parent_worker(self):
        pass


    def func_to_get_current_worker_is_parent(self):
        _worker_str = _Function._get_worker_name(pkg=self._py_pkg)
        _checksum = self.get_current_worker_is_parent()
        _mr_is_parent = self.worker_context.current_worker_is_parent()
        assert _checksum is _mr_is_parent, f"The checksum of is parent or not of {_worker_str} we got should be same as the checksum of is parent or not of {_worker_str} it returns via Python package '{self._py_pkg}'."


    @abstractmethod
    def get_current_worker_is_parent(self):
        pass


    def func_to_get_current_worker_ident(self):
        _worker_str = _Function._get_worker_name(pkg=self._py_pkg)
        _current_process_ident = self.get_current_worker_ident()
        _mr_current_process_ident = self.worker_context.get_current_worker_ident()
        assert _current_process_ident is _mr_current_process_ident, f"The identity of current {_worker_str} we got should be same as the identity of {_worker_str} it returns via Python package '{self._py_pkg}'."


    @abstractmethod
    def get_current_worker_ident(self):
        pass


    def func_to_get_current_worker_name(self):
        _worker_str = _Function._get_worker_name(pkg=self._py_pkg)
        _current_process_name = self.get_current_worker_name()
        _mr_current_process_name = self.worker_context.get_current_worker_name()
        print(f"[DEBUG in func_to_get_current_worker_name] _current_process_name: {_current_process_name}")
        print(f"[DEBUG in func_to_get_current_worker_name] _mr_current_process_name: {_mr_current_process_name}")
        assert _current_process_name is _mr_current_process_name, f"The name of current {_worker_str} we got should be same as the name of {_worker_str} it returns via Python package '{self._py_pkg}'."
        assert False


    @abstractmethod
    def get_current_worker_name(self):
        pass


    def func_to_get_current_worker_is_alive(self):
        _worker_str = _Function._get_worker_name(pkg=self._py_pkg)
        _current_process_is_alive = self.get_current_worker_is_alive()
        _mr_current_worker_is_alive = self.worker_context.current_worker_is_alive()
        assert _current_process_is_alive is _mr_current_worker_is_alive, f"The is_alive of current {_worker_str} we got should be same as the is_alive of {_worker_str} it returns via Python package '{self._py_pkg}'."


    @abstractmethod
    def get_current_worker_is_alive(self):
        pass


    def _func_to_get_activate_count(self):
        _worker_str = _Function._get_worker_name(pkg=self._py_pkg)
        _active_activate_count = self.get_activate_count()
        _mr_active_workers_count = self.worker_context.active_workers_count()
        assert _active_activate_count == _mr_active_workers_count, f"The amount of activate {_worker_str} we got should be same as amount of activate {_worker_str} it returns via Python package '{self._py_pkg}'."


    @abstractmethod
    def get_activate_count(self):
        pass


    def _func_to_get_children_workers(self):
        _worker_str = _Function._get_worker_name(pkg=self._py_pkg)
        _active_children_process = self.get_activate_children()
        _mr_children_workers = self.worker_context.children_workers()
        assert len(_active_children_process) == len(_mr_children_workers), f"The amount of activate {_worker_str} we got should be same as amount of activate {_worker_str} it returns via Python package '{self._py_pkg}'."
        assert _active_children_process == _mr_children_workers, f"The list of all activate {_worker_str} we got should be same as the list of all activate {_worker_str} it returns via Python package '{self._py_pkg}'."


    @abstractmethod
    def get_activate_children(self):
        pass


    @staticmethod
    def _get_worker_name(pkg: str):
        if pkg == "multiprocessing":
            return "Process"
        elif pkg == "threading":
            return "Thread"
        elif pkg == "gevent" or pkg == "greenlet":
            return "Green Thread"
        elif pkg == "asyncio":
            return "Asynchronous Task"
        else:
            raise ValueError("Invalid Python package name. It should be 'multiprocessing', 'threading', 'gevent', 'greenlet' or 'asynio'.")



class ContextTestSpec(metaclass=ABCMeta):

    @pytest.fixture(scope='class')
    @abstractmethod
    def testing_func(self) -> _Function:
        pass


    @pytest.fixture(scope='class')
    @abstractmethod
    def running_func(self):
        pass


    def test_get_current_worker(self, running_func, testing_func):
        running_func(_function=testing_func.func_to_get_current_worker)


    def test_get_parent_worker(self, running_func, testing_func):
        running_func(_function=testing_func.func_to_get_parent_worker)


    def test_current_worker_is_parent(self, running_func, testing_func):
        running_func(_function=testing_func.func_to_get_current_worker_is_parent)


    def test_current_worker_ident(self, running_func, testing_func):
        running_func(_function=testing_func.func_to_get_current_worker_ident)


    def test_current_worker_name(self, running_func, testing_func):
        running_func(_function=testing_func.func_to_get_current_worker_name)


    def test_current_worker_is_alive(self, running_func, testing_func):
        running_func(_function=testing_func.func_to_get_current_worker_is_alive)


    def test_activate_workers_count(self, running_func, testing_func):
        running_func(_function=testing_func._func_to_get_activate_count)


    def test_children_workers(self, running_func, testing_func):
        running_func(_function=testing_func._func_to_get_children_workers)

