from functools import wraps, update_wrapper, partial
from typing import Tuple, List, Dict, Callable, Optional
from abc import ABCMeta, abstractmethod
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
    def final_handling(self, *args, **kwargs):
        pass



class ReTryDefaultFunction(BaseDefaultFunction):

    def initial(self, *args, **kwargs):
        pass


    def error_handling(self, e: Exception):
        raise e


    def done_handling(self, result):
        return result


    def final_handling(self, *args, **kwargs):
        pass



class _BaseRetry:

    _Retry_Object = {}
    _Running_Timeout: int = None

    _Default_Func = ReTryDefaultFunction()

    _Target_Function: Callable = None
    _Initial_Function: Callable = _Default_Func.initial
    _Initial_Args: Tuple = ()
    _Initial_Kwargs: Dict = {}
    _Done_Handling_Function: Callable = _Default_Func.done_handling
    _Exception_Handling_Function: Callable = _Default_Func.error_handling
    _Final_Handling_Function: Callable = _Default_Func.final_handling


    def __init__(self, function: Callable, timeout: int = 1):
        pass


    @classmethod
    def initialization(cls, function: Callable):
        _cls = cls._get_retry_instance(function=function)
        _cls._Initial_Function = function

        @wraps(function)
        def __wrapper(*args, **kwargs):
            _cls._Initial_Args = args
            _cls._Initial_Kwargs = kwargs

        return __wrapper


    @classmethod
    def error_handling(cls, function: Callable):
        _cls = cls._get_retry_instance(function=function)
        _cls._Exception_Handling_Function = function

        @wraps(function)
        def __wrapper(e: Exception):
            pass
        return __wrapper


    @classmethod
    def done_handling(cls, function):
        _cls = cls._get_retry_instance(function=function)
        _cls._Done_Handling_Function = function

        @wraps(function)
        def __wrapper(_result):
            pass
        return __wrapper


    @classmethod
    def final_handling(cls, function):
        _cls = cls._get_retry_instance(function=function)
        _cls._Final_Handling_Function = function

        @wraps(function)
        def __wrapper():
            pass
        return __wrapper


    @classmethod
    def _call_retry_instance(cls, frame: List[inspect.FrameInfo], index: int):
        _retry_func_name = cls.__search_target_function_by_frame(frame=frame, index=index)
        assert _retry_func_name, "It should already have the function which target to retry in keys."
        _cls = cls._Retry_Object[_retry_func_name]
        return _cls


    @classmethod
    def __search_target_function_by_frame(cls, frame: List[inspect.FrameInfo], index: int) -> str:
        if index >= len(frame):
            raise ValueError("It cannot search the target function name in frame.")

        if index == 1:
            _next_index = -1
        elif index == -1:
            _next_index = 2
        else:
            _next_index = index + 1

        _code_lines = frame[index].code_context
        _retry_func_name_iter = filter(
            lambda key: cls.__exist_retry_function(retry_func=key, code_lines=_code_lines, line_index=0) is not None,
            cls._Retry_Object.keys()
        )
        _retry_func_name_list: List[str] = list(_retry_func_name_iter)

        if len(_retry_func_name_list) >= 1:
            return _retry_func_name_list[0]
        else:
            return cls.__search_target_function_by_frame(frame=frame, index=_next_index)


    @classmethod
    def __exist_retry_function(cls, retry_func: str, code_lines: List[str], line_index: int) -> Optional[str]:
        if line_index < len(code_lines):
            _retry_func_name = retry_func.split(".")[-1]
            _search_result = re.search(re.escape(_retry_func_name) + r"\w{0,128}", str(code_lines[line_index]))
            if _search_result is not None and f"{_retry_func_name}" == _search_result.group(0):
                return retry_func
            return cls.__exist_retry_function(retry_func=retry_func, code_lines=code_lines, line_index=(line_index + 1))
        return None


    @classmethod
    def _get_retry_instance(cls, function: Callable):
        _qualname_function_name = function.__qualname__
        _is_bounded = False

        # # Method 1: For general scenario like ACls.func
        # _class_function_format = re.search(r"\w{1,32}\.\w{1,32}", str(_qualname_function_name))
        # if _class_function_format is not None:
        #     _class_name = _class_function_format.group(0).split(".")[0]
        #     _is_bounded = True

        # # Method 2: For some special scenario like ACls.func.<local>._func
        if "." in str(_qualname_function_name):
            _qualname_function_name_list = str(_qualname_function_name).split(".")
            _class_name = ".".join(_qualname_function_name_list[:-1])
            _is_bounded = True

        _source_code_line = inspect.getsource(function)
        _source_code_lines = inspect.getsourcelines(function)
        _retry_target_function_name = cls.__parse_retry_target(code_lines=_source_code_line, is_bounded=_is_bounded)

        if _is_bounded is True:
            _retry_instance_key = f"{_class_name}.{_retry_target_function_name}"
        else:
            _retry_instance_key = _retry_target_function_name

        _cls = cls._Retry_Object[_retry_instance_key]
        return _cls


    @classmethod
    def __parse_retry_target(cls, code_lines: str, is_bounded: bool) -> str:
        _search_result = cls.__search_decorator(code_line=code_lines, is_bounded=is_bounded)
        if _search_result is not None:
            return _search_result
        raise ValueError("It cannot find the target function name.")


    # @overload
    # @classmethod
    # def __parse_retry_target(cls, code_lines: List[str], line_index: int) -> str:
    #     if line_index < len(code_lines):
    #         _search_result = cls.__search_decorator(code_line=code_lines[line_index])
    #         if _search_result is not None:
    #             return _search_result
    #         return cls.__parse_retry_target(code_lines=code_lines, line_index=(line_index + 1))
    #
    #     raise ValueError("It cannot find the target function name.")


    @classmethod
    def __search_decorator(cls, code_line: str, is_bounded: bool) -> Optional[str]:
        _search_retry_target = re.search(r"@[\w_]{1,64}\.", str(code_line))
        if _search_retry_target is not None:
            _retry_target = _search_retry_target.group(0).replace("@", "")
            _retry_target = _retry_target.replace(".", "")
            if is_bounded is True:
                _exist_retry_target = map(lambda key: _retry_target in key, cls._Retry_Object.keys())
            else:
                _exist_retry_target = map(lambda key: _retry_target == key, cls._Retry_Object.keys())
            if True in set(_exist_retry_target):
                return _retry_target
        return None


_TimeoutValueError = ValueError("The value of option *timeout* should be bigger than 0. The smallest valid option value is 1.")
_RetryTimeoutError = TimeoutError("Retry to run the target function running timeout.")


class _RetryFunction(_BaseRetry):

    _Retry_Object = {}


    def __new__(cls, *args, **kwargs):
        __function_name = kwargs['function'].__qualname__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_RetryFunction, cls).__new__(cls)
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        super().__init__(function, timeout)
        _cls = self._Retry_Object[function.__qualname__]
        _cls._Target_Function = function
        if timeout <= 0:
            raise _TimeoutValueError
        _cls._Running_Timeout = timeout


    @classmethod
    def __call__(cls, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        _current_frame = inspect.currentframe()
        _frame = inspect.getouterframes(_current_frame, 1)
        _current_cls = cls._call_retry_instance(frame=_frame, index=1)

        while __running_counter < _current_cls._Running_Timeout:
            try:
                _current_cls._Initial_Function(*_current_cls._Initial_Args, **_current_cls._Initial_Kwargs)
                __result = _current_cls._Target_Function(*args, **kwargs)
            except Exception as e:
                __running_success_flag = False
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
            __result = _RetryTimeoutError

        return __result



class _RetryBoundedFunction(_BaseRetry):

    _Retry_Object = {}

    _Target_Function: Callable = None
    _Initial_Function: Callable = None
    _Initial_Args: Tuple = ()
    _Initial_Kwargs: Dict = {}
    _Done_Handling_Function: Callable = None
    _Exception_Handling_Function: Callable = None
    _Final_Handling_Function: Callable = None

    __Current_Function = None


    def __new__(cls, *args, **kwargs):
        __function_name = kwargs['function'].__qualname__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_RetryBoundedFunction, cls).__new__(cls)
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        super().__init__(function, timeout)
        update_wrapper(self, function)

        _cls = self._Retry_Object[function.__qualname__]
        _cls._Target_Function = function
        if timeout <= 0:
            raise _TimeoutValueError
        _cls._Running_Timeout = timeout

        self.__Current_Function = function


    def __repr__(self):
        if self.__Current_Function is None:
            return super(_RetryBoundedFunction, self).__repr__()
        return f"{self.__Current_Function.__qualname__}"


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    def __call__(self, instance, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        _current_cls = self._Retry_Object[repr(self)]

        while __running_counter < _current_cls._Running_Timeout:
            try:
                self.run_initial_function(current_cls=_current_cls, instance=instance)
                __result = self.run_target_function(current_cls=_current_cls, instance=instance, *args, **kwargs)
            except Exception as e:
                __running_success_flag = False
                __error_handling_result = self.run_error_handling_function(current_cls=_current_cls, instance=instance, e=e)
                if __error_handling_result:
                    __result = __error_handling_result
                else:
                    __result = e
            else:
                __running_success_flag = True
                self.run_done_handling_function(current_cls=_current_cls, instance=instance, result=__result)
            finally:
                self.run_final_handling_function(current_cls=_current_cls, instance=instance)
                if __running_success_flag is True:
                    return __result
                __running_counter += 1
        else:
            __result = _RetryTimeoutError

        return __result


    def run_target_function(self, current_cls, instance, *args, **kwargs):
        _target_func = getattr(current_cls, "_Target_Function")
        assert _target_func is not None, "It's impossible that the target function is None object."
        return _target_func(instance, *args, **kwargs)


    def run_initial_function(self, current_cls, instance):
        _init_func = getattr(current_cls, "_Initial_Function")
        if _init_func is None:
            self._Default_Func.initial()
        else:
            _init_func_args = getattr(current_cls, "_Initial_Args")
            _init_func_kwargs = getattr(current_cls, "_Initial_Kwargs")
            _init_func(instance, *_init_func_args, **_init_func_kwargs)


    def run_error_handling_function(self, current_cls, instance, e: Exception):
        _exception_handling_func = getattr(current_cls, "_Exception_Handling_Function")
        if _exception_handling_func is None:
            return self._Default_Func.error_handling(e=e)
        else:
            return _exception_handling_func(instance, e)


    def run_done_handling_function(self, current_cls, instance, result):
        _done_handling_func = getattr(current_cls, "_Done_Handling_Function")
        if _done_handling_func is None:
            self._Default_Func.done_handling(result=result)
        else:
            _done_handling_func(instance, result)


    def run_final_handling_function(self, current_cls, instance):
        _final_handling_func = getattr(current_cls, "_Final_Handling_Function")
        if _final_handling_func is None:
            self._Default_Func.final_handling()
        else:
            _final_handling_func(instance)



class AsyncReTryDefaultFunction(BaseDefaultFunction):

    async def initial(self, *args, **kwargs):
        pass


    async def error_handling(self, e: Exception):
        raise e


    async def done_handling(self, result):
        return result


    async def final_handling(self, *args, **kwargs):
        pass



class _BaseAsyncRetry(_BaseRetry):

    _Default_Func = AsyncReTryDefaultFunction()

    _Target_Function: Callable = None
    _Initial_Function: Callable = _Default_Func.initial
    _Initial_Args: Tuple = ()
    _Initial_Kwargs: Dict = {}
    _Done_Handling_Function: Callable = _Default_Func.done_handling
    _Exception_Handling_Function: Callable = _Default_Func.error_handling
    _Final_Handling_Function: Callable = _Default_Func.final_handling

    FunctionNotCoroutineError = TypeError("The marker decorator function isn't coroutine.")


    @classmethod
    def initialization(cls, function: Callable):
        cls._chk_coroutine_function(function=function)

        _cls = cls._get_retry_instance(function=function)
        _cls._Initial_Function = function

        @wraps(function)
        def __wrapper(*args, **kwargs):
            _cls.__Initial_Args = args
            _cls.__Initial_Kwargs = kwargs

        return __wrapper


    @classmethod
    def error_handling(cls, function: Callable):
        cls._chk_coroutine_function(function=function)

        _cls = cls._get_retry_instance(function=function)
        _cls._Exception_Handling_Function = function

        @wraps(function)
        def __wrapper(e: Exception):
            pass
        return __wrapper


    @classmethod
    def done_handling(cls, function):
        cls._chk_coroutine_function(function=function)

        _cls = cls._get_retry_instance(function=function)
        _cls._Done_Handling_Function = function

        @wraps(function)
        def __wrapper(func_result):
            pass
        return __wrapper


    @classmethod
    def final_handling(cls, function):
        cls._chk_coroutine_function(function=function)

        _cls = cls._get_retry_instance(function=function)
        _cls._Final_Handling_Function = function

        @wraps(function)
        def __wrapper(func_result):
            pass
        return __wrapper


    @classmethod
    def _chk_coroutine_function(cls, function: Callable):
        __chksum = inspect.iscoroutinefunction(function)
        if __chksum is True:
            return True
        else:
            raise cls.FunctionNotCoroutineError



class _AsyncRetryFunction(_BaseAsyncRetry):

    _Retry_Object = {}


    def __new__(cls, *args, **kwargs):
        __function_name = kwargs['function'].__qualname__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_AsyncRetryFunction, cls).__new__(cls)
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        super().__init__(function, timeout)

        self._chk_coroutine_function(function=function)

        update_wrapper(self, function)
        _cls = self._Retry_Object[function.__qualname__]
        _cls._Target_Function = function
        if timeout <= 0:
            raise _TimeoutValueError
        _cls._Running_Timeout = timeout


    @classmethod
    async def __call__(cls, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        _current_frame = inspect.currentframe()
        _frame = inspect.getouterframes(_current_frame, 1)
        _current_cls = cls._call_retry_instance(frame=_frame, index=0)

        while __running_counter < _current_cls._Running_Timeout:
            try:
                await _current_cls._Initial_Function(*_current_cls._Initial_Args, **_current_cls._Initial_Kwargs)
                __result = await _current_cls._Target_Function(*args, **kwargs)
            except Exception as e:
                __running_success_flag = False
                __error_handling_result = await _current_cls._Exception_Handling_Function(e)
                if __error_handling_result:
                    __result = __error_handling_result
                else:
                    __result = e
            else:
                __running_success_flag = True
                __result = await _current_cls._Done_Handling_Function(__result)
            finally:
                await _current_cls._Final_Handling_Function()
                if __running_success_flag is True:
                    return __result
                __running_counter += 1
        else:
            __result = _RetryTimeoutError

        return __result



class _AsyncRetryBoundedFunction(_BaseAsyncRetry):

    _Retry_Object = {}

    _Target_Function: Callable = None
    _Initial_Function: Callable = None
    _Initial_Args: Tuple = ()
    _Initial_Kwargs: Dict = {}
    _Done_Handling_Function: Callable = None
    _Exception_Handling_Function: Callable = None
    _Final_Handling_Function: Callable = None

    __Current_Function = None


    def __new__(cls, *args, **kwargs):
        __function_name = kwargs['function'].__qualname__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_AsyncRetryBoundedFunction, cls).__new__(cls)
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        super().__init__(function, timeout)

        self._chk_coroutine_function(function=function)

        update_wrapper(self, function)
        _cls = self._Retry_Object[function.__qualname__]
        _cls._Target_Function = function
        if timeout <= 0:
            raise _TimeoutValueError
        _cls._Running_Timeout = timeout

        self.__Current_Function = function


    def __repr__(self):
        if self.__Current_Function is None:
            return super(_AsyncRetryBoundedFunction, self).__repr__()
        return f"{self.__Current_Function.__qualname__}"


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    async def __call__(self, instance, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        _current_cls = self._Retry_Object[repr(self)]

        while __running_counter < _current_cls._Running_Timeout:
            try:
                await self.run_initial_function(current_cls=_current_cls, instance=instance)
                __result = await self.run_target_function(current_cls=_current_cls, instance=instance, *args, **kwargs)
            except Exception as e:
                __running_success_flag = False
                __error_handling_result = await self.run_error_handling_function(current_cls=_current_cls, instance=instance, e=e)
                if __error_handling_result:
                    __result = __error_handling_result
                else:
                    __result = e
            else:
                __running_success_flag = True
                __result = await self.run_done_handling_function(current_cls=_current_cls, instance=instance, result=__result)
            finally:
                await self.run_final_handling_function(current_cls=_current_cls, instance=instance)
                if __running_success_flag is True:
                    return __result
                __running_counter += 1
        else:
            __result = _RetryTimeoutError

        return __result


    async def run_target_function(self, current_cls, instance, *args, **kwargs):
        _target_func = getattr(current_cls, "_Target_Function")
        assert _target_func is not None, "It's impossible that the target function is None object."
        return await _target_func(instance, *args, **kwargs)


    async def run_initial_function(self, current_cls, instance):
        _init_func = getattr(current_cls, "_Initial_Function")
        if _init_func is None:
            await self._Default_Func.initial()
        else:
            _init_func_args = getattr(current_cls, "_Initial_Args")
            _init_func_kwargs = getattr(current_cls, "_Initial_Kwargs")
            await _init_func(instance, *_init_func_args, **_init_func_kwargs)


    async def run_error_handling_function(self, current_cls, instance, e: Exception):
        _exception_handling_func = getattr(current_cls, "_Exception_Handling_Function")
        if _exception_handling_func is None:
            return await self._Default_Func.error_handling(e=e)
        else:
            return await _exception_handling_func(instance, e)


    async def run_done_handling_function(self, current_cls, instance, result):
        _done_handling_func = getattr(current_cls, "_Done_Handling_Function")
        if _done_handling_func is None:
            await self._Default_Func.done_handling(result=result)
        else:
            await _done_handling_func(instance, result)


    async def run_final_handling_function(self, current_cls, instance):
        _final_handling_func = getattr(current_cls, "_Final_Handling_Function")
        if _final_handling_func is None:
            await self._Default_Func.final_handling()
        else:
            await _final_handling_func(instance)


