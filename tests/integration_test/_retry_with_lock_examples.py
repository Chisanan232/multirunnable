from multirunnable.api import retry, RunWith

from .._examples import (
    _sleep_time, __record_info_to_flags as _record_info_to_flags
)


def target_function_with_lock() -> None:
    retry_success_with_lock()


def target_function_with_rlock() -> None:
    retry_success_with_rlock()


def target_function_with_smp() -> None:
    retry_success_with_smp()


def target_function_with_bsmp() -> None:
    retry_success_with_bsmp()


@retry.function
@RunWith.Lock
def retry_success_with_lock() -> None:
    _record_info_to_flags()
    _sleep_time()


@retry.function
@RunWith.RLock
def retry_success_with_rlock() -> None:
    _record_info_to_flags()
    _sleep_time()


@retry.function
@RunWith.Semaphore
def retry_success_with_smp() -> None:
    _record_info_to_flags()
    _sleep_time()


@retry.function
@RunWith.Bounded_Semaphore
def retry_success_with_bsmp() -> None:
    _record_info_to_flags()
    _sleep_time()



class RetrySuccessMethods:

    @retry.bounded_function
    @RunWith.Lock
    def retry_success_with_lock(self) -> None:
        _record_info_to_flags()
        _sleep_time()


    @retry.bounded_function
    @RunWith.RLock
    def retry_success_with_rlock(self) -> None:
        _record_info_to_flags()
        _sleep_time()


    @retry.bounded_function
    @RunWith.Semaphore
    def retry_success_with_smp(self) -> None:
        _record_info_to_flags()
        _sleep_time()


    @retry.bounded_function
    @RunWith.Bounded_Semaphore
    def retry_success_with_bsmp(self) -> None:
        _record_info_to_flags()
        _sleep_time()

