from abc import ABCMeta, abstractmethod
from typing import Tuple, Dict, Callable
from functools import wraps, update_wrapper, partial
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



class _Retry:

    __Retry_Instances: Dict = {}

    __Running_Timeout: int = None

    __default_func = ReTryDefaultFunction()

    __Target_Function: Callable = None
    __Initial_Function: Callable = __default_func.initial
    __Initial_Args: Tuple = ()
    __Initial_Kwargs: Dict = {}
    __Exception_Handling_Function: Callable = __default_func.error_handling
    __Done_Handling_Function: Callable = __default_func.done_handling
    __Final_Handling_Function: Callable = __default_func.final_handling


    # def __new__(cls, *args, **kwargs):
    #     """ Create and return a new object.  See help(type) for accurate signature. """
    #     __Retry_Instances
    #     return super.__new__(*args, **kwargs)


    def __init__(self, function: Callable, timeout: int = 1):
        update_wrapper(self, function)
        self.__Target_Function = function
        self.__Running_Timeout = timeout


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    def __call__(self, instance, *args, **kwargs):
        print(f"[DEBUG] self.__Target_Function: {self.__Target_Function}")
        print(f"[DEBUG] instance: {instance}")
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
            print(f"[DEBUG] function: {function} - initial")
            __self.__Initial_Args = args
            __self.__Initial_Kwargs = kwargs

        return __wrapper


    @classmethod
    def error_handling(cls, function: Callable):
        cls.__Exception_Handling_Function = function
        __self = cls

        @wraps(function)
        def __wrapper(e: Exception):
            print(f"[DEBUG] function: {function} - error_handling")
            pass
        return __wrapper


    @classmethod
    def done_handling(cls, function):
        cls.__Done_Handling_Function = function
        __self = cls

        @wraps(function)
        def __wrapper(func_result):
            print(f"[DEBUG] function: {function} - done_handling")
            pass
        return __wrapper


    @classmethod
    def final_handling(cls, function):
        cls.__Final_Handling_Function = function

        @wraps(function)
        def __wrapper(func_result):
            print(f"[DEBUG] function: {function} - final_handling")
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


