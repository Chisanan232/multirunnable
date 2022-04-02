from typing import List, Callable
import pytest

from multirunnable import RunningMode

from ..test_config import Under_Test_RunningModes, Worker_Size, Semaphore_Value, Running_Diff_Time, Test_Function_Sleep_Time
from .._examples import (
    RunByStrategy, reset_running_flags, get_running_workers_ids, get_running_done_timestamps
)
from .._examples_with_synchronization import (
    instantiate_lock, instantiate_rlock,
    instantiate_semaphore, instantiate_bounded_semaphore
)
from ._retry_with_lock_examples import (
    target_function_with_lock, target_function_with_rlock, target_function_with_smp, target_function_with_bsmp,
    RetrySuccessMethods
)


@pytest.fixture(scope="class")
def retry_funcs_cls() -> RetrySuccessMethods:
    return RetrySuccessMethods()


class TestRetryWithLock:

    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_retry_with_lock_function(self, mode: RunningMode):
        reset_running_flags()

        instantiate_lock(_mode=mode)
        TestRetryWithLock._run_test(mode=mode, function=target_function_with_lock)
        TestRetryWithLock._chk_results(synchronize=True)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_retry_with_rlock_function(self, mode: RunningMode):
        reset_running_flags()

        instantiate_rlock(_mode=mode)
        TestRetryWithLock._run_test(mode=mode, function=target_function_with_rlock)
        TestRetryWithLock._chk_results(synchronize=True)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_retry_with_semaphore_function(self, mode: RunningMode):
        reset_running_flags()

        instantiate_semaphore(_mode=mode)
        TestRetryWithLock._run_test(mode=mode, function=target_function_with_smp)
        TestRetryWithLock._chk_results(synchronize=False)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_retry_with_bounded_semaphore_function(self, mode: RunningMode):
        reset_running_flags()

        instantiate_bounded_semaphore(_mode=mode)
        TestRetryWithLock._run_test(mode=mode, function=target_function_with_bsmp)
        TestRetryWithLock._chk_results(synchronize=False)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_retry_with_lock_bounded_function(self, mode: RunningMode, retry_funcs_cls: RetrySuccessMethods):
        reset_running_flags()

        instantiate_lock(_mode=mode)
        TestRetryWithLock._run_test(mode=mode, function=retry_funcs_cls.retry_success_with_lock)
        TestRetryWithLock._chk_results(synchronize=True)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_retry_with_rlock_bounded_function(self, mode: RunningMode, retry_funcs_cls: RetrySuccessMethods):
        reset_running_flags()

        instantiate_rlock(_mode=mode)
        TestRetryWithLock._run_test(mode=mode, function=retry_funcs_cls.retry_success_with_rlock)
        TestRetryWithLock._chk_results(synchronize=True)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_retry_with_semaphore_bounded_function(self, mode: RunningMode, retry_funcs_cls: RetrySuccessMethods):
        reset_running_flags()

        instantiate_semaphore(_mode=mode)
        TestRetryWithLock._run_test(mode=mode, function=retry_funcs_cls.retry_success_with_smp)
        TestRetryWithLock._chk_results(synchronize=False)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_retry_with_bounded_semaphore_bounded_function(self, mode: RunningMode, retry_funcs_cls: RetrySuccessMethods):
        reset_running_flags()

        instantiate_bounded_semaphore(_mode=mode)
        TestRetryWithLock._run_test(mode=mode, function=retry_funcs_cls.retry_success_with_bsmp)
        TestRetryWithLock._chk_results(synchronize=False)


    @staticmethod
    def _run_test(mode: RunningMode, function: Callable) -> None:
        if mode is RunningMode.Parallel:
            RunByStrategy.Parallel(_function=function)
        elif mode is RunningMode.Concurrent:
            RunByStrategy.Concurrent(_function=function)
        elif mode is RunningMode.GreenThread:
            RunByStrategy.CoroutineWithGreenThread(_function=function)
        else:
            raise ValueError("The RunningMode is invalid. Please check your entry argument.")


    @staticmethod
    def _chk_results(synchronize: bool):
        _running_workers_ids = get_running_workers_ids()
        _running_done_timestamps = get_running_done_timestamps()

        assert len(_running_workers_ids) == Worker_Size, "The length of worker IDs list (no de-duplicate) should be same as the worker size."
        assert len(set(_running_workers_ids)) == Worker_Size, "The length of worker IDs list (de-duplicate) should be same as the worker size."

        if synchronize is True:
            TestRetryWithLock._chk_blocking_done_timestamp(timestamp_list=_running_done_timestamps)
        else:
            TestRetryWithLock._chk_done_timestamp(timestamp_list=_running_done_timestamps)


    @staticmethod
    def _chk_blocking_done_timestamp(timestamp_list: List[int]):
        _max_timestamp = max(timestamp_list)
        _min_timestamp = min(timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= (Test_Function_Sleep_Time * Worker_Size) + Running_Diff_Time, "Processes should be run in the same time period."


    @staticmethod
    def _chk_done_timestamp(timestamp_list: List[int]):
        _max_timestamp = max(timestamp_list)
        _min_timestamp = min(timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Test_Function_Sleep_Time * round(Worker_Size / Semaphore_Value), "Processes should be run in the same time period."
