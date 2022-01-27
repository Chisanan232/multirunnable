from abc import ABCMeta, abstractmethod
from types import FrameType, FunctionType, MethodType
from typing import Tuple, List, Dict, Callable
from functools import wraps, update_wrapper, partial
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


    @classmethod
    def _call_retry_object(cls, frame: List[inspect.FrameInfo], index: int):
        _retry_func_name_iter = cls._search_target_function_in_code_lines(frame=frame, index=index)
        _retry_func_name = _retry_func_name_iter[0]
        assert _retry_func_name != "", f"It should already have the function which target to retry in keys."
        _cls = cls._Retry_Object[_retry_func_name]
        return _cls


    @classmethod
    def _search_target_function_in_code_lines(cls, frame: List[inspect.FrameInfo], index: int) -> List[str]:
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
            lambda key: cls._exist_retry_function(retry_func=key, code_lines=_code_lines, line_index=0) is not None,
            cls._Retry_Object.keys()
        )
        _retry_func_name_list = list(_retry_func_name_iter)

        if len(_retry_func_name_list) != 0:
            return _retry_func_name_list
        return cls._search_target_function_in_code_lines(frame=frame, index=_next_index)


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
        raise ValueError("It cannot find the target function name.")



class _RetryFunction(_BaseRetry):

    _Retry_Object = {}


    def __new__(cls, *args, **kwargs):
        __function_name = kwargs['function'].__name__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_RetryFunction, cls).__new__(cls)
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        super().__init__(function, timeout)
        _cls = self._Retry_Object[function.__name__]
        _cls._Target_Function = function
        _cls._Running_Timeout = timeout


    @classmethod
    def __call__(cls, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        _current_frame = inspect.currentframe()
        _frame = inspect.getouterframes(_current_frame, 1)
        _current_cls = cls._call_retry_object(frame=_frame, index=1)

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
            __result = TimeoutError("The target function running timeout.")

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


    def __new__(cls, *args, **kwargs):
        __function_name = kwargs['function'].__name__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_RetryBoundedFunction, cls).__new__(cls)
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        super().__init__(function, timeout)
        update_wrapper(self, function)
        _cls = self._Retry_Object[function.__name__]
        _cls._Target_Function = function
        _cls._Running_Timeout = timeout


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    def __call__(self, instance, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        _current_frame = inspect.currentframe()
        _frame = inspect.getouterframes(_current_frame, 1)
        _current_cls = self._call_retry_object(frame=_frame, index=1)

        while __running_counter < self._Running_Timeout:
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
            __result = TimeoutError("The target function running timeout.")

        return __result


    def run_target_function(self, current_cls, instance, *args, **kwargs):
        _target_func = getattr(current_cls, "_Target_Function")
        assert _target_func is not None, f"It's impossible that the target function is None object."
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

        _current_frame = inspect.currentframe()
        _cls = cls._get_retry_object(current_frame=_current_frame)

        _cls._Initial_Function = function

        @wraps(function)
        def __wrapper(*args, **kwargs):
            _cls.__Initial_Args = args
            _cls.__Initial_Kwargs = kwargs

        return __wrapper


    @classmethod
    def error_handling(cls, function: Callable):
        cls._chk_coroutine_function(function=function)

        _current_frame = inspect.currentframe()
        _cls = cls._get_retry_object(current_frame=_current_frame)

        _cls._Exception_Handling_Function = function

        @wraps(function)
        def __wrapper(e: Exception):
            pass
        return __wrapper


    @classmethod
    def done_handling(cls, function):
        cls._chk_coroutine_function(function=function)

        _current_frame = inspect.currentframe()
        _cls = cls._get_retry_object(current_frame=_current_frame)

        _cls._Done_Handling_Function = function

        @wraps(function)
        def __wrapper(func_result):
            pass
        return __wrapper


    @classmethod
    def final_handling(cls, function):
        cls._chk_coroutine_function(function=function)

        _current_frame = inspect.currentframe()
        _cls = cls._get_retry_object(current_frame=_current_frame)

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
        __function_name = kwargs['function'].__name__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_AsyncRetryFunction, cls).__new__(cls)
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        super().__init__(function, timeout)
        self._chk_coroutine_function(function=function)
        update_wrapper(self, function)
        _cls = self._Retry_Object[function.__name__]
        _cls._Target_Function = function
        _cls._Running_Timeout = timeout


    @classmethod
    async def __call__(cls, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        _current_frame = inspect.currentframe()
        _frame = inspect.getouterframes(_current_frame, 1)
        _current_cls = cls._call_retry_object(frame=_frame, index=0)

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
            __result = TimeoutError("The target function running timeout.")

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


    def __new__(cls, *args, **kwargs):
        __function_name = kwargs['function'].__name__
        if __function_name not in cls._Retry_Object.keys():
            cls._Retry_Object[__function_name] = super(_AsyncRetryBoundedFunction, cls).__new__(cls)
        return cls._Retry_Object[__function_name]


    def __init__(self, function: Callable, timeout: int = 1):
        super().__init__(function, timeout)
        self._chk_coroutine_function(function=function)
        update_wrapper(self, function)
        _cls = self._Retry_Object[function.__name__]
        _cls._Target_Function = function
        _cls._Running_Timeout = timeout


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    async def __call__(self, instance, *args, **kwargs):
        __running_counter = 0
        __running_success_flag = None
        __result = None

        _current_frame = inspect.currentframe()
        _frame = inspect.getouterframes(_current_frame, 1)
        _current_cls = self._call_retry_object(frame=_frame, index=0)

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
            __result = TimeoutError("The target function running timeout.")

        return __result


    async def run_target_function(self, current_cls, instance, *args, **kwargs):
        _target_func = getattr(current_cls, "_Target_Function")
        assert _target_func is not None, f"It's impossible that the target function is None object."
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


