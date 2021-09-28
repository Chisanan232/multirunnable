from multirunnable.framework.result import OceanResult as _OceanResult
from multirunnable.api.operator import (
    LockAdapterOperator as _LockOperator,
    SemaphoreOperator as _SemaphoreOperator,
    BoundedSemaphoreOperator as _BoundedSemaphoreOperator,
    LockAsyncOperator as _LockAsyncOperator,
    SemaphoreAsyncOperator as _SemaphoreAsyncOperator,
    BoundedSemaphoreAsyncOperator as _BoundedSemaphoreAsyncOperator)

from functools import wraps, update_wrapper, partial
from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Callable, Type, Any, Union
import inspect



class BaseDefaultFunction(metaclass=ABCMeta):

    @abstractmethod
    def initial(self, *args, **kwargs):
        pass


    @abstractmethod
    def error_handling(self, e: Exception):
        raise e


    @abstractmethod
    def done_handling(self, result):
        return result


    @abstractmethod
    def final_handling(self):
        pass



class ReTryDefaultFunction(BaseDefaultFunction):

    def initial(self, *args, **kwargs):
        pass


    def error_handling(self, e: Exception):
        raise e


    def done_handling(self, result):
        return result


    def final_handling(self):
        pass


def retry(function: Callable = None, timeout: int = 1):

    if function:
        return _Retry(function=function, timeout=timeout)
    else:
        @wraps(function)
        def __retry(function: Callable):
            return _Retry(function=function, timeout=timeout)
        return __retry


class _Retry:

    __Running_Timeout: int = None

    __default_func = ReTryDefaultFunction()

    __Target_Function: Callable = None
    __Initial_Function: Callable = __default_func.initial
    __Initial_Args: Tuple = ()
    __Initial_Kwargs: Dict = {}
    __Exception_Handling_Function: Callable = __default_func.error_handling
    __Done_Handling_Function: Callable = __default_func.done_handling
    __Final_Handling_Function: Callable = __default_func.final_handling


    def __init__(self, function: Callable, timeout: int = 1):
        update_wrapper(self, function)
        self.__Target_Function = function
        self.__Running_Timeout = timeout


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    def __call__(self, instance, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        while __running_counter < self.__Running_Timeout:
            try:
                self.__Initial_Function(*self.__Initial_Args, **self.__Initial_Kwargs)
                __result = self.__Target_Function(instance, *args, **kwargs)
            except Exception as e:
                __running_success_flag = False
                __error_handling_result = self.__Exception_Handling_Function(e)
                if __error_handling_result:
                    __result = __error_handling_result
                else:
                    __result = e
            else:
                __running_success_flag = True
                __result = self.__Done_Handling_Function(__result)
            finally:
                self.__Final_Handling_Function()
                if __running_success_flag is True:
                    return __result
                __running_counter += 1
        else:
            __result = TimeoutError("The target function running timeout.")

        return __result


    @classmethod
    def initialization(cls, function: Callable):

        cls.__Initial_Function = function
        __self = cls

        @wraps(function)
        def __wrapper(*args, **kwargs):
            __self.__Initial_Args = args
            __self.__Initial_Kwargs = kwargs

        return __wrapper


    @classmethod
    def error_handling(cls, function: Callable):
        cls.__Exception_Handling_Function = function
        __self = cls

        @wraps(function)
        def __wrapper(e: Exception):
            pass
        return __wrapper


    @classmethod
    def done_handling(cls, function):
        cls.__Done_Handling_Function = function
        __self = cls

        @wraps(function)
        def __wrapper(func_result):
            pass
        return __wrapper


    @classmethod
    def final_handling(cls, function):
        cls.__Final_Handling_Function = function

        @wraps(function)
        def __wrapper(func_result):
            pass
        return __wrapper



class AsyncReTryDefaultFunction(BaseDefaultFunction):

    async def initial(self, *args, **kwargs):
        pass


    async def error_handling(self, e: Exception):
        raise e


    async def done_handling(self, result):
        return result


    async def final_handling(self):
        pass



def async_retry(function: Callable = None, timeout: int = 1):

    if function:
        return _AsyncRetry(function=function, timeout=timeout)
    else:
        @wraps(function)
        def __async_retry(function: Callable):
            return _AsyncRetry(function=function, timeout=timeout)
        return __async_retry



class _AsyncRetry:

    __Running_Timeout: int = None

    __default_func = AsyncReTryDefaultFunction()

    __Target_Function: Callable = None
    __Initial_Function: Callable = __default_func.initial
    __Initial_Args: Tuple = ()
    __Initial_Kwargs: Dict = {}
    __Exception_Handling_Function: Callable = __default_func.error_handling
    __Done_Handling_Function: Callable = __default_func.done_handling
    __Final_Handling_Function: Callable = __default_func.final_handling

    FunctionNotCoroutineError = TypeError("The marker decorator function isn't coroutine.")


    def __init__(self, function: Callable, timeout: int = 1):
        self.__chk_coroutine_function(function=function)
        update_wrapper(self, function)
        self.__Target_Function = function
        self.__Running_Timeout = timeout


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    async def __call__(self, instance, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        while __running_counter < self.__Running_Timeout:
            try:
                await self.__Initial_Function(*self.__Initial_Args, **self.__Initial_Kwargs)
                __result = await self.__Target_Function(instance, *args, **kwargs)
            except Exception as e:
                __running_success_flag = False
                __error_handling_result = await self.__Exception_Handling_Function(e)
                if __error_handling_result:
                    __result = __error_handling_result
                else:
                    __result = e
            else:
                __running_success_flag = True
                __result = await self.__Done_Handling_Function(__result)
            finally:
                await self.__Final_Handling_Function()
                if __running_success_flag is True:
                    return __result
                __running_counter += 1
        else:
            __result = TimeoutError("The target function running timeout.")

        return __result


    @classmethod
    def initialization(cls, function: Callable):
        cls.__chk_coroutine_function(function=function)
        cls.__Initial_Function = function
        __self = cls

        @wraps(function)
        def __wrapper(*args, **kwargs):
            __self.__Initial_Args = args
            __self.__Initial_Kwargs = kwargs

        return __wrapper


    @classmethod
    def error_handling(cls, function: Callable):
        cls.__chk_coroutine_function(function=function)
        cls.__Exception_Handling_Function = function
        __self = cls

        @wraps(function)
        def __wrapper(e: Exception):
            pass
        return __wrapper


    @classmethod
    def done_handling(cls, function):
        cls.__chk_coroutine_function(function=function)
        cls.__Done_Handling_Function = function
        __self = cls

        @wraps(function)
        def __wrapper(func_result):
            pass
        return __wrapper


    @classmethod
    def final_handling(cls, function):
        cls.__chk_coroutine_function(function=function)
        cls.__Final_Handling_Function = function

        @wraps(function)
        def __wrapper(func_result):
            pass
        return __wrapper


    @classmethod
    def __chk_coroutine_function(cls, function: Callable):
        __chksum = inspect.iscoroutinefunction(function)
        if __chksum is True:
            return True
        else:
            raise cls.FunctionNotCoroutineError



class RunWith:

    @staticmethod
    def Lock(function: Callable[[Any, Any], List[Type[_OceanResult]]]):
        """
        Description:
            A decorator which would add lock mechanism around the target
            function for fixed time.
        :return:
        """

        @wraps(function)
        def __lock_process(*args, **kwargs) -> List[Type[_OceanResult]]:
            __lock = _LockOperator()

            with __lock:
                result = function(*args, **kwargs)
            return result

        return __lock_process


    @staticmethod
    def Semaphore(function: Callable[[Any, Any], List[Type[_OceanResult]]]):
        """
        Description:
            A decorator which would add semaphore mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def __semaphore_process(*args, **kwargs) -> List[Type[_OceanResult]]:
            __semaphore = _SemaphoreOperator()

            with __semaphore:
                result = function(*args, **kwargs)
            return result

        return __semaphore_process


    @staticmethod
    def Bounded_Semaphore(function: Callable[[Any, Any], List[Type[_OceanResult]]]):
        """
        Description:
            A decorator which would add bounded semaphore mechanism
            around the target function for fixed time.
        :return:
        """

        @wraps(function)
        def __bounded_semaphore_process(*args, **kwargs) -> List[Type[_OceanResult]]:
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
        async def __lock_process(*args, **kwargs) -> List[Type[_OceanResult]]:
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
        async def __semaphore_process(*args, **kwargs) -> List[Type[_OceanResult]]:
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
        async def __bounded_semaphore_process(*args, **kwargs) -> List[Type[_OceanResult]]:
            __bounded_semaphore = _BoundedSemaphoreAsyncOperator()

            async with __bounded_semaphore:
                result = await function(*args, **kwargs)
            return result

        return __bounded_semaphore_process

