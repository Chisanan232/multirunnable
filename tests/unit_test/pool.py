import traceback
import pytest

from multirunnable.concurrent.strategy import ThreadPoolStrategy
from multirunnable.coroutine.strategy import GreenThreadPoolStrategy
from multirunnable.parallel.strategy import ProcessPoolStrategy
from multirunnable.pool import AdapterPool
from multirunnable import get_current_mode, set_mode, RunningMode, SimplePool

from ..test_config import Worker_Pool_Size, Task_Size, Test_Function_Args, Test_Function_Multiple_Args
from .._examples import (
    # # Import the flags
    get_running_cnt, get_current_workers, get_running_workers_ids, get_running_done_timestamps,
    # # Import some common functions
    reset_running_flags, initial_lock,
    # # Import some target functions to run for Pool object
    target_function, target_function_for_map, target_funcs_iter
)
from .framework.strategy import PoolRunningTestSpec


_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size


@pytest.fixture(scope="function")
def simple_pool(request) -> SimplePool:
    return SimplePool(mode=request.param, pool_size=_Worker_Pool_Size)


@pytest.fixture(scope="function")
def adapter_pool() -> AdapterPool:
    set_mode(RunningMode.Concurrent)
    return AdapterPool(strategy=ThreadPoolStrategy(pool_size=_Worker_Pool_Size))



class TestSimplePool:

    """
    Description:
        Testing executor which may be as Process, Thread, Green Thread or Asynchronous object.
        The responsibility of this object is calling the mapping method(s) by the RunningMode.
        For example, it will use 'multiprocessing.Process.start' when you call 'run' with RunningMode.Parallel.

        For the testing concern, we should pay the attention to the feature of responsibility which means
        it should target at the feature about 'Procedure' and 'Adapter of features', doesn't working process.
    """

    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_initial_running_strategy(self, simple_pool: SimplePool):
        simple_pool._initial_running_strategy()

        _rmode = get_current_mode(force=True)

        from multirunnable.pool import Pool_Runnable_Strategy
        if _rmode is RunningMode.Parallel:
            assert Pool_Runnable_Strategy is not None, "It should be assign running-strategy instance."
            assert isinstance(Pool_Runnable_Strategy, ProcessPoolStrategy), "It should be an sub-instance of 'ProcessPoolStrategy'."
        elif _rmode is RunningMode.Concurrent:
            assert Pool_Runnable_Strategy is not None, "It should be assign running-strategy instance."
            assert isinstance(Pool_Runnable_Strategy, ThreadPoolStrategy), "It should be an sub-instance of 'ThreadPoolStrategy'."
        elif _rmode is RunningMode.GreenThread:
            assert Pool_Runnable_Strategy is not None, "It should be assign running-strategy instance."
            assert isinstance(Pool_Runnable_Strategy, GreenThreadPoolStrategy), "It should be an sub-instance of 'GreenThreadPoolStrategy'."
        else:
            raise ValueError("The RunningMode has the unexpected mode.")


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_apply(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.apply(tasks_size=Task_Size, function=target_function)
        TestSimplePool._chk_blocking_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_apply_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.apply(tasks_size=Task_Size, function=target_function)
        TestSimplePool._chk_blocking_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_apply(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.async_apply(tasks_size=Task_Size, function=target_function)
        TestSimplePool._chk_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_apply_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.async_apply(tasks_size=Task_Size, function=target_function)
        TestSimplePool._chk_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_apply_with_iter(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_apply_with_iter_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_apply_with_iter(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_apply_with_iter_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.map(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.map(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_map(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.async_map(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_map_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.async_map(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map_by_args(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.map_by_args(function=target_function_for_map, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_map_by_args_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.map_by_args(function=target_function_for_map, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_map_by_args(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.async_map_by_args(function=target_function_for_map, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_async_map_by_args_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.async_map_by_args(function=target_function_for_map, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_imap(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.imap(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_imap_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.imap(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_imap_unordered(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        simple_pool.initial()
        simple_pool.imap_unordered(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_imap_unordered_by_pykeyword_with(self, simple_pool: SimplePool):
        TestSimplePool._initial()
        with simple_pool as _pool:
            _pool.imap_unordered(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = simple_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_terminal(self, simple_pool: SimplePool):
        try:
            simple_pool.initial()
            simple_pool.async_apply(tasks_size=Task_Size, function=lambda a: a+a, args=(1,))
            simple_pool.terminal()
        except Exception:
            assert False, f"It should work finely without any issue. Please check it.\n Error: {traceback.format_exc()}"
        else:
            assert True, "It work finely without any issue."


    @pytest.mark.parametrize(
        argnames="simple_pool",
        argvalues=[RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread],
        indirect=True
    )
    def test_close(self, simple_pool: SimplePool):
        try:
            simple_pool.initial()
            simple_pool.async_apply(tasks_size=Task_Size, function=lambda a: a+a, args=(1,))
            simple_pool.close()
        except Exception:
            assert False, f"It should work finely without any issue. Please check it.\n Error: {traceback.format_exc()}"
        else:
            assert True, "It work finely without any issue."


    @staticmethod
    def _initial():
        reset_running_flags()
        initial_lock()


    @staticmethod
    def _chk_blocking_record():
        # PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_blocking(
            pool_running_cnt=get_running_cnt(),
            worker_size=_Task_Size,
            running_worker_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps(),
            de_duplicate=False
        )


    @staticmethod
    def _chk_record():
        # PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record(
            pool_running_cnt=get_running_cnt(),
            worker_size=_Task_Size,
            running_worker_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps()
        )


    @staticmethod
    def _chk_map_record():
        # PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_map(
            pool_running_cnt=get_running_cnt(),
            function_args=Test_Function_Args,
            running_worker_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps()
        )


    @staticmethod
    def chk_results(results, expected_size):
        assert results, "It should have something, it couldn't be empty or None."
        assert len(results) == expected_size, f"The result length should be equal to the expected value '{expected_size}'."
        for _r in results:
            assert "result_" in _r.data, "The result value should be same as the return value of target function."
            assert _r.exception is None, f"The exception should be nothing. But it got {_r.exception}."
            assert _r.is_successful is True, "It should work finely."



class TestAdapterPool:

    def test_apply(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.apply(tasks_size=Task_Size, function=target_function)
        TestSimplePool._chk_blocking_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_apply_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.apply(tasks_size=Task_Size, function=target_function)
        TestSimplePool._chk_blocking_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_async_apply(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.async_apply(tasks_size=Task_Size, function=target_function)
        TestSimplePool._chk_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_async_apply_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.async_apply(tasks_size=Task_Size, function=target_function)
        TestSimplePool._chk_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_apply_with_iter(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_apply_with_iter_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_blocking_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_async_apply_with_iter(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_async_apply_with_iter_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.async_apply_with_iter(functions_iter=target_funcs_iter())
        TestSimplePool._chk_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=Task_Size)


    def test_map(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.map(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_map_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.map(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_async_map(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.async_map(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_async_map_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.async_map(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_map_by_args(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.map_by_args(function=target_function_for_map, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    def test_map_by_args_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.map_by_args(function=target_function_for_map, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    def test_async_map_by_args(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.async_map_by_args(function=target_function_for_map, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    def test_async_map_by_args_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.async_map_by_args(function=target_function_for_map, args_iter=Test_Function_Multiple_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Multiple_Args))


    def test_imap(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.imap(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_imap_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.imap(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_imap_unordered(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        adapter_pool.initial()
        adapter_pool.imap_unordered(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_imap_unordered_by_pykeyword_with(self, adapter_pool: AdapterPool):
        TestSimplePool._initial()
        with adapter_pool as _pool:
            _pool.imap_unordered(function=target_function_for_map, args_iter=Test_Function_Args)
        TestSimplePool._chk_map_record()

        _results = adapter_pool.get_result()
        TestSimplePool.chk_results(results=_results, expected_size=len(Test_Function_Args))


    def test_terminal(self, adapter_pool: AdapterPool):
        try:
            adapter_pool.initial()
            adapter_pool.async_apply(tasks_size=Task_Size, function=lambda a: a+a, args=(1,))
            adapter_pool.terminal()
        except Exception:
            assert False, f"It should work finely without any issue. Please check it.\n Error: {traceback.format_exc()}"
        else:
            assert True, "It work finely without any issue."


    def test_close(self, adapter_pool: AdapterPool):
        try:
            adapter_pool.initial()
            adapter_pool.async_apply(tasks_size=Task_Size, function=lambda a: a+a, args=(1,))
            adapter_pool.close()
        except Exception:
            assert False, f"It should work finely without any issue. Please check it.\n Error: {traceback.format_exc()}"
        else:
            assert True, "It work finely without any issue."

