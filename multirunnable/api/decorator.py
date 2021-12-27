from ._retry import _Retry, _AsyncRetry

from functools import wraps
from typing import List, Callable, Type, Any

from multirunnable.framework.result import MRResult as _MRResult
from multirunnable.api.operator import (
    LockAdapterOperator as _LockOperator,
    RLockOperator as _RLockOperator,
    SemaphoreOperator as _SemaphoreOperator,
    BoundedSemaphoreOperator as _BoundedSemaphoreOperator,
    LockAsyncOperator as _LockAsyncOperator,
    SemaphoreAsyncOperator as _SemaphoreAsyncOperator,
    BoundedSemaphoreAsyncOperator as _BoundedSemaphoreAsyncOperator
)



def retry(function: Callable = None, timeout: int = 1):

    if function:
        return _Retry(function=function, timeout=timeout)
    else:
        @wraps(function)
        def __retry(function: Callable):
            return _Retry(function=function, timeout=timeout)
        return __retry



def async_retry(function: Callable = None, timeout: int = 1):

    if function:
        return _AsyncRetry(function=function, timeout=timeout)
    else:
        @wraps(function)
        def __async_retry(function: Callable):
            return _AsyncRetry(function=function, timeout=timeout)
        return __async_retry



class RunWith:

    @staticmethod
    def Lock(function: Callable[[Any, Any], List[Type[_MRResult]]]):
        """
        Description:
            A decorator which would add lock mechanism around the target
            function for fixed time.
        :return:
        """

        @wraps(function)
        def __lock_process(*args, **kwargs) -> List[Type[_MRResult]]:
            __lock = _LockOperator()

            with __lock:
                result = function(*args, **kwargs)
            return result

        return __lock_process


    @staticmethod
    def RLock(function: Callable[[Any, Any], List[Type[_MRResult]]]):
        """
        Description:
            A decorator which would add rlock mechanism around the target
            function for fixed time.
        :return:
        """

        @wraps(function)
        def __rlock_process(*args, **kwargs) -> List[Type[_MRResult]]:
            __rlock = _RLockOperator()

            with __rlock:
                result = function(*args, **kwargs)
            return result

        return __rlock_process


    @staticmethod
    def Semaphore(function: Callable[[Any, Any], List[Type[_MRResult]]]):
        """
        Description:
            A decorator which would add semaphore mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def __semaphore_process(*args, **kwargs) -> List[Type[_MRResult]]:
            __semaphore = _SemaphoreOperator()

            with __semaphore:
                result = function(*args, **kwargs)
            return result

        return __semaphore_process


    @staticmethod
    def Bounded_Semaphore(function: Callable[[Any, Any], List[Type[_MRResult]]]):
        """
        Description:
            A decorator which would add bounded semaphore mechanism
            around the target function for fixed time.
        :return:
        """

        @wraps(function)
        def __bounded_semaphore_process(*args, **kwargs) -> List[Type[_MRResult]]:
            __bounded_semaphore = _BoundedSemaphoreOperator()

            with __bounded_semaphore:
                result = function(*args, **kwargs)
            return result

        return __bounded_semaphore_process



class AsyncRunWith:

    @staticmethod
    def Lock(function: Callable):
        """
        Description:
            Asynchronous version of run_with_lock.
        :return:
        """

        @wraps(function)
        async def __lock_process(*args, **kwargs) -> List[Type[_MRResult]]:
            __lock = _LockAsyncOperator()

            async with __lock:
                result = await function(*args, **kwargs)
            return result

        return __lock_process


    @staticmethod
    def Semaphore(function: Callable):
        """
        Description:
            Asynchronous version of run_with_semaphore.
        :return:
        """

        @wraps(function)
        async def __semaphore_process(*args, **kwargs) -> List[Type[_MRResult]]:
            __semaphore = _SemaphoreAsyncOperator()

            async with __semaphore:
                result = await function(*args, **kwargs)
            return result

        return __semaphore_process


    @staticmethod
    def Bounded_Semaphore(function: Callable):
        """
        Description:
             Asynchronous version of run_with_bounded_semaphore.
       :return:
        """

        @wraps(function)
        async def __bounded_semaphore_process(*args, **kwargs) -> List[Type[_MRResult]]:
            __bounded_semaphore = _BoundedSemaphoreAsyncOperator()

            async with __bounded_semaphore:
                result = await function(*args, **kwargs)
            return result

        return __bounded_semaphore_process

