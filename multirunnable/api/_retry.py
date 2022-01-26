from abc import ABCMeta, abstractmethod
from types import FrameType, FunctionType, MethodType
from typing import Tuple, List, Dict, Callable
from functools import wraps, update_wrapper, partial
from itertools import product
import inspect
import re



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



class _BaseRetry:

    _Retry_Object = {}


    @classmethod
    def _call_retry_object(cls, frame: List[inspect.FrameInfo]):
        _code_lines = frame[1].code_context

        _retry_func_name_iter = filter(
            lambda key: cls._exist_retry_function(retry_func=key, code_lines=_code_lines, line_index=0) is not None,
            cls._Retry_Object.keys()
        )
        _retry_func_name = list(_retry_func_name_iter)[0]
        assert _retry_func_name != "", f"It should already have the function which target to retry in keys."
        _cls = cls._Retry_Object[_retry_func_name]
        return _cls


    @classmethod
    def _exist_retry_function(cls, retry_func: str, code_lines: List[str], line_index: int):
        if line_index < len(code_lines):
            if retry_func in code_lines[line_index]:
                return retry_func
            return cls._exist_retry_function(retry_func=retry_func, code_lines=code_lines, line_index=(line_index + 1))
        return None


    @classmethod
    def _get_retry_object(cls, current_frame: FrameType):
        _code_lines = cls._get_code_lines(current_frame=current_frame)
        _retry_target_function_name = cls._parse_retry_target(code_lines=_code_lines, line_index=0)
        _cls = cls._Retry_Object[_retry_target_function_name]
        return _cls


    @classmethod
    def _get_code_lines(cls, current_frame: FrameType) -> List[str]:
        _frame = inspect.getouterframes(current_frame, 4)
        _code_lines = _frame[1].code_context
        return _code_lines


    @classmethod
    def _parse_retry_target(cls, code_lines: List[str], line_index: int) -> str:
        if line_index < len(code_lines):
            _search_retry_target = re.search(r"@[\w_]{1,64}\.", str(code_lines[line_index]))
            if _search_retry_target is not None:
                _retry_target = _search_retry_target.group(0).replace("@", "")
                _retry_target = _retry_target.replace(".", "")
                if _retry_target in cls._Retry_Object.keys():
                    return _retry_target
            return cls._parse_retry_target(code_lines=code_lines, line_index=(line_index + 1))
        raise ValueError("")


    @classmethod
    def initialization(cls, function: Callable):
        _current_frame = inspect.currentframe()
        _cls = cls._get_retry_object(current_frame=_current_frame)

        _cls._Initial_Function = function

        @wraps(function)
        def __wrapper(*args, **kwargs):
            _cls._Initial_Args = args
            _cls._Initial_Kwargs = kwargs

        return __wrapper


    @classmethod
    def error_handling(cls, function: Callable):
        _current_frame = inspect.currentframe()
        _cls = cls._get_retry_object(current_frame=_current_frame)

        _cls._Exception_Handling_Function = function

        @wraps(function)
        def __wrapper(e: Exception):
            pass
        return __wrapper


    @classmethod
    def done_handling(cls, function):
        _current_frame = inspect.currentframe()
        _cls = cls._get_retry_object(current_frame=_current_frame)

        _cls._Done_Handling_Function = function

        @wraps(function)
        def __wrapper(_result):
            pass
        return __wrapper


    @classmethod
    def final_handling(cls, function):
        _current_frame = inspect.currentframe()
        _cls = cls._get_retry_object(current_frame=_current_frame)
        _cls._Final_Handling_Function = function

        @wraps(function)
        def __wrapper():
            pass
        return __wrapper



class _RetryFunction(_BaseRetry):

    _Retry_Object = {}
    _Running_Timeout: int = None

    __default_func = ReTryDefaultFunction()

    _Target_Function: Callable = None
    _Initial_Function: Callable = __default_func.initial
    _Initial_Args: Tuple = ()
    _Initial_Kwargs: Dict = {}
    _Exception_Handling_Function: Callable = __default_func.error_handling
    _Done_Handling_Function: Callable = __default_func.done_handling
    _Final_Handling_Function: Callable = __default_func.final_handling


    def __new__(cls, *args, **kwargs):
        __function_name = kwargs['function'].__name__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_RetryFunction, cls).__new__(cls)
        print(f"[DEBUG in __new__] cls._Retry_Object: {cls._Retry_Object}")
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        _cls = self._Retry_Object[function.__name__]
        _cls._Target_Function = function
        _cls._Running_Timeout = timeout
        print(f"[DEBUG] function is FunctionType: {isinstance(function, FunctionType)}")
        print(f"[DEBUG] function is MethodType: {isinstance(function, MethodType)}")


    # def __get__(self, instance, owner):
    #     return partial(self.__call__, instance)


    @classmethod
    def __call__(cls, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        _current_frame = inspect.currentframe()
        _frame = inspect.getouterframes(_current_frame, 1)
        _current_cls = cls._call_retry_object(frame=_frame)
        print(f"[DEBUG in __call__] _current_cls: {_current_cls}")

        while __running_counter < _current_cls._Running_Timeout:
            try:
                _current_cls._Initial_Function(*_current_cls._Initial_Args, **_current_cls._Initial_Kwargs)
                __result = _current_cls._Target_Function(*args, **kwargs)
            except Exception as e:
                __running_success_flag = False
                print(f"[DEBUG in __call__] _current_cls._Exception_Handling_Function: {_current_cls._Exception_Handling_Function}")
                __error_handling_result = _current_cls._Exception_Handling_Function(e)
                if __error_handling_result:
                    __result = __error_handling_result
                else:
                    __result = e
            else:
                __running_success_flag = True
                __result = _current_cls._Done_Handling_Function(__result)
            finally:
                _current_cls._Final_Handling_Function()
                if __running_success_flag is True:
                    return __result
                __running_counter += 1
        else:
            __result = TimeoutError("The target function running timeout.")

        return __result


    @classmethod
    def _retry_instance_cache(cls) -> Dict[str, Callable]:
        return cls._Retry_Object



class _RetryClassFunction(_BaseRetry):

    _Running_Timeout: int = None

    __default_func = ReTryDefaultFunction()

    _Target_Function: Callable = None
    _Initial_Function: Callable = __default_func.initial
    _Initial_Args: Tuple = ()
    _Initial_Kwargs: Dict = {}
    _Exception_Handling_Function: Callable = __default_func.error_handling
    _Done_Handling_Function: Callable = __default_func.done_handling
    _Final_Handling_Function: Callable = __default_func.final_handling


    def __new__(cls, *args, **kwargs):
        __function_name = kwargs['function'].__name__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_RetryClassFunction, cls).__new__(cls)
        print(f"[DEBUG in __new__] cls._Retry_Object: {cls._Retry_Object}")
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        update_wrapper(self, function)
        _cls = self._Retry_Object[function.__name__]
        _cls._Target_Function = function
        _cls._Running_Timeout = timeout
        print(f"[DEBUG] function is FunctionType: {isinstance(function, FunctionType)}")
        print(f"[DEBUG] function is MethodType: {isinstance(function, MethodType)}")


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    def __call__(self, instance, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        while __running_counter < self._Running_Timeout:
            try:
                self._Initial_Function(*self._Initial_Args, **self._Initial_Kwargs)
                __result = self._Target_Function(instance, *args, **kwargs)
            except Exception as e:
                __running_success_flag = False
                __error_handling_result = self._Exception_Handling_Function(e)
                if __error_handling_result:
                    __result = __error_handling_result
                else:
                    __result = e
            else:
                __running_success_flag = True
                __result = self._Done_Handling_Function(__result)
            finally:
                self._Final_Handling_Function()
                if __running_success_flag is True:
                    return __result
                __running_counter += 1
        else:
            __result = TimeoutError("The target function running timeout.")

        return __result


    @classmethod
    def _retry_instance_cache(cls) -> Dict[str, Callable]:
        return cls._Retry_Object



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


