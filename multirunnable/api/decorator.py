from functools import wraps
from inspect import isclass as inspect_isclass
from typing import List, Callable, Type, Any, Union, Optional
from types import MethodType, FunctionType
from abc import ABCMeta, abstractmethod

from ..framework.runnable.result import MRResult as _MRResult
from ..api.operator import (
    LockOperator as _LockOperator,
    RLockOperator as _RLockOperator,
    SemaphoreOperator as _SemaphoreOperator,
    BoundedSemaphoreOperator as _BoundedSemaphoreOperator,
    LockAsyncOperator as _LockAsyncOperator,
    SemaphoreAsyncOperator as _SemaphoreAsyncOperator,
    BoundedSemaphoreAsyncOperator as _BoundedSemaphoreAsyncOperator
)
from ._retry import (
    _BaseRetry,
    _RetryFunction, _RetryBoundedFunction,
    _BaseAsyncRetry,
    _AsyncRetryFunction, _AsyncRetryBoundedFunction
)


class InstantiateError(RuntimeError):

    def __init__(self, cls_name: str):
        self.__cls_name = cls_name

    def __str__(self):
        return f"It shouldn't instantiate {self.__cls_name} object."



class _BaseRetryDecorator(metaclass=ABCMeta):

    def __init__(self):
        raise InstantiateError(self.__class__.__name__)


    @staticmethod
    @abstractmethod
    def function(function=None, timeout: int = 1):
        pass


    @staticmethod
    @abstractmethod
    def bounded_function(function: Optional[FunctionType] = None, timeout: int = 1):
        pass


    @classmethod
    def _retry_process(cls, retry_mechanism: Type[Union[_BaseRetry, _BaseAsyncRetry]], function: Optional[FunctionType] = None, timeout: int = 1):
        if inspect_isclass(function) is True:
            raise ValueError("The target object be decorated should be a 'function' type object.")

        if function:
            return retry_mechanism(function=function, timeout=timeout)
        else:
            @wraps(function)
            def __retry(function: Callable):
                return retry_mechanism(function=function, timeout=timeout)

            return __retry



class retry(_BaseRetryDecorator):

    @staticmethod
    def function(function: Optional[FunctionType] = None, timeout: int = 1):
        return retry._retry_process(retry_mechanism=_RetryFunction, function=function, timeout=timeout)


    @staticmethod
    def bounded_function(function: Optional[FunctionType] = None, timeout: int = 1):
        return retry._retry_process(retry_mechanism=_RetryBoundedFunction, function=function, timeout=timeout)



class async_retry(_BaseRetryDecorator):

    @staticmethod
    def function(function: Optional[FunctionType] = None, timeout: int = 1):
        return async_retry._retry_process(retry_mechanism=_AsyncRetryFunction, function=function, timeout=timeout)


    @staticmethod
    def bounded_function(function: Optional[FunctionType] = None, timeout: int = 1):
        return async_retry._retry_process(retry_mechanism=_AsyncRetryBoundedFunction, function=function, timeout=timeout)



def retry_function(function: Optional[Union[FunctionType, MethodType]] = None, timeout: int = 1):
    return retry.function(function=function, timeout=timeout)


def retry_bounded_function(function: Optional[Union[FunctionType, MethodType]] = None, timeout: int = 1):
    return retry.bounded_function(function=function, timeout=timeout)


def async_retry_function(function: Callable = None, timeout: int = 1):
    return async_retry.function(function=function, timeout=timeout)


def async_retry_bounded_function(function: Callable = None, timeout: int = 1):
    return async_retry.bounded_function(function=function, timeout=timeout)



class RunWith:

    def __init__(self):
        raise InstantiateError(self.__class__.__name__)


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

    def __init__(self):
        raise InstantiateError(self.__class__.__name__)


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

