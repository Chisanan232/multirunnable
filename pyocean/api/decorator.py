from pyocean.framework.task import BaseTask as _BaseTask
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.api.operator import (
    LockOperator as _LockOperator,
    SemaphoreOperator as _SemaphoreOperator,
    BoundedSemaphoreOperator as _BoundedSemaphoreOperator)

from functools import wraps, update_wrapper, partial
from typing import List, Tuple, Dict, Callable, Type, Any, Union
import inspect



class ReTryMechanism:

    Running_Timeout = 1

    @staticmethod
    def function(function: Callable[[Any, Any], Union[List[Type[_OceanResult]], Exception]]):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def retry_function(*args, **kwargs) -> Union[List[Type[_OceanResult]], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < ReTryMechanism.Running_Timeout:
                try:
                    ReTryMechanism._initialization(*args, **kwargs)
                    result = function(*args, **kwargs)
                except Exception as e:
                    result = ReTryMechanism._error_handling(e=e)
                else:
                    result = ReTryMechanism._done_handling(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return retry_function


    @staticmethod
    def async_function(function: Callable):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        async def retry_async_function(*args, **kwargs) -> Union[List[Type[_OceanResult]], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < ReTryMechanism.Running_Timeout:
                try:
                    await ReTryMechanism._async_initialization(*args, **kwargs)
                    result = await function(*args, **kwargs)
                except Exception as e:
                    result = await ReTryMechanism._async_error_handling(e=e)
                else:
                    result = await ReTryMechanism._async_done_handling(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return retry_async_function


    # @staticmethod
    @classmethod
    def task(cls, function: Callable[[_BaseTask], Union[List[Type[_OceanResult]], Exception]]):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def task_retry(self, task: _BaseTask) -> Union[List[Type[_OceanResult]], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < task.running_timeout + 1:
                try:
                    task.initialization(*task.init_args, **task.init_kwargs)
                    result = task.function(*task.func_args, **task.func_kwargs)
                except Exception as e:
                    result = task.error_handler(e=e)
                else:
                    result = task.done_handler(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return task_retry


    @staticmethod
    def async_task(function: Callable[[_BaseTask], Union[List[Type[_OceanResult]], Exception]]):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        async def task_retry(self, task: _BaseTask) -> Union[List[Type[_OceanResult]], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < task.running_timeout + 1:
                try:
                    await task.initialization(*task.init_args, **task.init_kwargs)
                    result = await task.function(*task.func_args, **task.func_kwargs)
                except Exception as e:
                    result = await task.error_handler(e=e)
                else:
                    result = await task.done_handler(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return task_retry


    @classmethod
    def _initialization(cls, *args, **kwargs) -> None:
        """
        Description:
            Initial something before run main logic.
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @classmethod
    def _done_handling(cls, result: List[Type[_OceanResult]]) -> List[Type[_OceanResult]]:
        """
        Description:
            Handling the result data after target function running done.
        :param result:
        :return:
        """
        return result


    @classmethod
    def _error_handling(cls, e: Exception) -> Union[List[Type[_OceanResult]], Exception]:
        """
        Description:
            Handling all the error when occur any unexpected error in target function running.
        :param e:
        :return:
        """
        raise e


    @classmethod
    async def _async_initialization(cls, *args, **kwargs) -> None:
        """
        Description:
            Initial something before run main logic.
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @classmethod
    async def _async_done_handling(cls, result: List[Type[_OceanResult]]) -> List[Type[_OceanResult]]:
        """
        Description:
            Handling the result data after target function running done.
        :param result:
        :return:
        """
        return result


    @classmethod
    async def _async_error_handling(cls, e: Exception) -> Union[List[Type[_OceanResult]], Exception]:
        """
        Description:
            Handling all the error when occur any unexpected error in target function running.
        :param e:
        :return:
        """
        raise e



class ReTryDefaultFunction:

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
        __result = None

        while __running_counter < self.__Running_Timeout:
            try:
                self.__Initial_Function(*self.__Initial_Args, **self.__Initial_Kwargs)
                __result = self.__Target_Function(instance, *args, **kwargs)
            except Exception as e:
                __error_handling_result = self.__Exception_Handling_Function(e)
                if __error_handling_result:
                    __result = __error_handling_result
                else:
                    __result = e
            else:
                __result = self.__Done_Handling_Function(__result)
            finally:
                self.__Final_Handling_Function()
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



class AsyncReTryDefaultFunction:

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


    def __call__(self, instance, *args, **kwargs):
        __running_counter = 0
        __result = None

        while __running_counter < self.__Running_Timeout:
            try:
                await self.__Initial_Function(*self.__Initial_Args, **self.__Initial_Kwargs)
                __result = await self.__Target_Function(instance, *args, **kwargs)
            except Exception as e:
                __error_handling_result = await self.__Exception_Handling_Function(e)
                if __error_handling_result:
                    __result = __error_handling_result
                else:
                    __result = e
            else:
                __result = await self.__Done_Handling_Function(__result)
            finally:
                await self.__Final_Handling_Function()
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



class LockDecorator:

    @staticmethod
    def run_with_lock(function: Callable[[Any, Any], List[Type[_OceanResult]]]):
        """
        Description:
            A decorator which would add lock mechanism around the target
            function for fixed time.
        :return:
        """

        @wraps(function)
        def lock(*args, **kwargs) -> List[Type[_OceanResult]]:
            # from pyocean.api.manager import Running_Lock
            __lock = _LockOperator()

            with __lock:
                result = function(*args, **kwargs)
            return result

        return lock


    @staticmethod
    def run_with_semaphore(function: Callable[[Any, Any], List[Type[_OceanResult]]]):
        """
        Description:
            A decorator which would add semaphore mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def semaphore(*args, **kwargs) -> List[Type[_OceanResult]]:
            # from pyocean.api.manager import Running_Semaphore
            __semaphore = _SemaphoreOperator()

            with __semaphore:
                result = function(*args, **kwargs)
            return result

        return semaphore


    @staticmethod
    def run_with_bounded_semaphore(function: Callable[[Any, Any], List[Type[_OceanResult]]]):
        """
        Description:
            A decorator which would add bounded semaphore mechanism
            around the target function for fixed time.
        :return:
        """

        @wraps(function)
        def bounded_semaphore(*args, **kwargs) -> List[Type[_OceanResult]]:
            # from pyocean.api.manager import Running_Bounded_Semaphore
            __bounded_semaphore = _BoundedSemaphoreOperator()

            with __bounded_semaphore:
                result = function(*args, **kwargs)
            return result

        return bounded_semaphore


    @staticmethod
    def async_run_with_lock(function: Callable):
        """
        Description:
            Asynchronous version of run_with_lock.
        :return:
        """

        @wraps(function)
        async def lock(*args, **kwargs) -> List[Type[_OceanResult]]:
            # from pyocean.api.manager import Running_Lock
            __lock = LockDecorator()

            async with __lock:
                result = await function(*args, **kwargs)
            return result

        return lock


    @staticmethod
    def async_run_with_semaphore(function: Callable):
        """
        Description:
            Asynchronous version of run_with_semaphore.
        :return:
        """

        @wraps(function)
        async def semaphore(*args, **kwargs) -> List[Type[_OceanResult]]:
            # from pyocean.api.manager import Running_Semaphore
            __semaphore = _SemaphoreOperator()

            async with __semaphore:
                result = await function(*args, **kwargs)
            return result

        return semaphore


    @staticmethod
    def async_run_with_bounded_semaphore(function: Callable):
        """
        Description:
             Asynchronous version of run_with_bounded_semaphore.
       :return:
        """

        @wraps(function)
        async def bounded_semaphore(*args, **kwargs) -> List[Type[_OceanResult]]:
            # from pyocean.api.manager import Running_Bounded_Semaphore
            __bounded_semaphore = _BoundedSemaphoreOperator()

            async with __bounded_semaphore:
                result = await function(*args, **kwargs)
            return result

        return bounded_semaphore



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
            __lock = LockDecorator()

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
            __semaphore = _SemaphoreOperator()

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
            __bounded_semaphore = _BoundedSemaphoreOperator()

            async with __bounded_semaphore:
                result = await function(*args, **kwargs)
            return result

        return __bounded_semaphore_process

