from typing import Type, Union
import pytest

from multirunnable.concurrent.context import context as thread_context
from multirunnable.coroutine.context import green_thread_context, async_task_context
from multirunnable.parallel.context import context as process_context
from multirunnable.adapter.context import context as adapter_context
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION, set_mode, RunningMode

from ..._examples import RunByStrategy



class _Function:

    def __init__(self, mode: RunningMode):
        self._mode = mode


    def get_current_worker_func(self):
        assert adapter_context.get_current_worker() is self._get_context().get_current_worker()


    def get_parent_worker_func(self):
        assert adapter_context.get_parent_worker() is self._get_context().get_parent_worker()


    def get_current_worker_is_parent_func(self):
        assert adapter_context.current_worker_is_parent() is self._get_context().current_worker_is_parent()


    def get_current_worker_ident_func(self):
        assert adapter_context.get_current_worker_ident() == self._get_context().get_current_worker_ident()


    def get_current_worker_name_func(self):
        assert adapter_context.get_current_worker_name() == self._get_context().get_current_worker_name()


    def get_current_worker_is_alive_func(self):
        assert adapter_context.current_worker_is_alive() is self._get_context().current_worker_is_alive()


    def activate_count_func(self):
        assert adapter_context.active_workers_count() is self._get_context().active_workers_count()


    def children_workers_func(self):
        assert adapter_context.children_workers() is self._get_context().children_workers()


    def _get_context(self) -> Union[Type[process_context], Type[thread_context], Type[green_thread_context], Type[async_task_context]]:
        if self._mode is RunningMode.Parallel:
            return process_context
        elif self._mode is RunningMode.Concurrent:
            return thread_context
        elif self._mode is RunningMode.GreenThread:
            return green_thread_context
        elif self._mode is RunningMode.Asynchronous:
            return async_task_context
        else:
            raise ValueError



class TestAdapterContext:

    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_get_current_worker(self, mode):
        _test_spec = _Function(mode=mode)

        set_mode(mode=mode)
        TestAdapterContext._run_test(mode=mode, testing=_test_spec.get_current_worker_func)


    @pytest.mark.xfail(reason="It doesn't support to get parent process via *multiprocessing* under Python 3.7 version.")
    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_get_parent_worker(self, mode):
        if mode is RunningMode.Parallel and (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) <= (3, 7):
            raise NotImplementedError
        else:
            _test_spec = _Function(mode=mode)

            set_mode(mode=mode)
            TestAdapterContext._run_test(mode=mode, testing=_test_spec.get_parent_worker_func)


    @pytest.mark.xfail(reason="It doesn't support to get parent process via *multiprocessing* under Python 3.7 version.")
    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_current_worker_is_parent(self, mode):
        if mode is RunningMode.Parallel and (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) <= (3, 7):
            raise NotImplementedError
        else:
            _test_spec = _Function(mode=mode)

            set_mode(mode=mode)
            TestAdapterContext._run_test(mode=mode, testing=_test_spec.get_current_worker_is_parent_func)


    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_get_current_worker_ident(self, mode):
        _test_spec = _Function(mode=mode)

        set_mode(mode=mode)
        TestAdapterContext._run_test(mode=mode, testing=_test_spec.get_current_worker_ident_func)


    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_get_current_worker_name(self, mode):
        _test_spec = _Function(mode=mode)

        set_mode(mode=mode)
        TestAdapterContext._run_test(mode=mode, testing=_test_spec.get_current_worker_name_func)


    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_get_current_worke_is_alive(self, mode):
        _test_spec = _Function(mode=mode)

        set_mode(mode=mode)
        TestAdapterContext._run_test(mode=mode, testing=_test_spec.get_current_worker_is_alive_func)


    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_get_activate_count(self, mode):
        _test_spec = _Function(mode=mode)

        set_mode(mode=mode)
        TestAdapterContext._run_test(mode=mode, testing=_test_spec.activate_count_func)


    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_get_children_workers(self, mode):
        _test_spec = _Function(mode=mode)

        set_mode(mode=mode)
        TestAdapterContext._run_test(mode=mode, testing=_test_spec.children_workers_func)


    @staticmethod
    def _run_test(mode, testing):
        if mode is RunningMode.Parallel:
            RunByStrategy.Parallel(_function=testing)
        elif mode is RunningMode.Concurrent:
            RunByStrategy.Concurrent(_function=testing)
        elif mode is RunningMode.GreenThread:
            RunByStrategy.CoroutineWithGreenThread(_function=testing)
        elif mode is RunningMode.Asynchronous:
            RunByStrategy.CoroutineWithAsynchronous(_function=testing)
        else:
            raise ValueError

