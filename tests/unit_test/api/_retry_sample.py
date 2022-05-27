from multirunnable.api.decorator import (
    retry, async_retry
)

from collections import namedtuple


_Retry_Time = 4
_Default_Retry_Time = 1
Running_Target_Function_Counter: int = 0
Initial_Handling_Flag_Counter: int = 0
Done_Handling_Flag_Counter: int = 0
Final_Handling_Flag_Counter: int = 0
Error_Handling_Flag_Counter: int = 0

Default_Function_Flag = False
Retry_Function_Flag = False

Default_Method_Flag = False
Retry_Method_Flag = False

Default_Classmethod_Flag = False
Retry_Classmethod_Flag = False

Default_Staticmethod_Flag = False
Retry_Staticmethod_Flag = False

_Async_Running = False


_Test_Return_Value = "TestResult"
_Test_Exception = Exception("Test for raising exception.")


def init_flag() -> None:
    """
    Initial and reset value of all flags.
    :return:
    """
    global Running_Target_Function_Counter, Initial_Handling_Flag_Counter, Done_Handling_Flag_Counter, Final_Handling_Flag_Counter, Error_Handling_Flag_Counter
    global Default_Function_Flag, Retry_Function_Flag, Default_Method_Flag, Retry_Method_Flag, Default_Classmethod_Flag, Retry_Classmethod_Flag, Default_Staticmethod_Flag, Retry_Staticmethod_Flag, _Async_Running

    Running_Target_Function_Counter = 0
    Initial_Handling_Flag_Counter = 0
    Done_Handling_Flag_Counter = 0
    Final_Handling_Flag_Counter = 0
    Error_Handling_Flag_Counter = 0

    Default_Function_Flag = False
    Retry_Function_Flag = False

    Default_Method_Flag = False
    Retry_Method_Flag = False

    Default_Classmethod_Flag = False
    Retry_Classmethod_Flag = False

    Default_Staticmethod_Flag = False
    Retry_Staticmethod_Flag = False

    _Async_Running = False


Process_Flag = namedtuple(
        "Process_Flag",
        ["Running_Target_Function_Counter",
         "Initial_Handling_Flag_Counter",
         "Done_Handling_Flag_Counter",
         "Final_Handling_Flag_Counter",
         "Error_Handling_Flag_Counter"]
    )

Run_Function_Flag = namedtuple(
    "Run_Function_Flag",
    ["Default_Function_Flag",
     "Retry_Function_Flag",
     "Default_Method_Flag",
     "Retry_Method_Flag",
     "Default_Classmethod_Flag",
     "Retry_Classmethod_Flag",
     "Default_Staticmethod_Flag",
     "Retry_Staticmethod_Flag",
     "Async_Running"]
)


def get_process_flag() -> Process_Flag:
    global Running_Target_Function_Counter, Initial_Handling_Flag_Counter, Done_Handling_Flag_Counter, Final_Handling_Flag_Counter, Error_Handling_Flag_Counter

    _process_flag = Process_Flag(
        Running_Target_Function_Counter=Running_Target_Function_Counter,
        Initial_Handling_Flag_Counter=Initial_Handling_Flag_Counter,
        Done_Handling_Flag_Counter=Done_Handling_Flag_Counter,
        Error_Handling_Flag_Counter=Error_Handling_Flag_Counter,
        Final_Handling_Flag_Counter=Final_Handling_Flag_Counter
    )
    return _process_flag


def get_running_function_flag() -> Run_Function_Flag:
    global Running_Target_Function_Counter, Initial_Handling_Flag_Counter, Done_Handling_Flag_Counter, Final_Handling_Flag_Counter, Error_Handling_Flag_Counter

    _run_func_falg = Run_Function_Flag(
        Default_Function_Flag=Default_Function_Flag,
        Retry_Function_Flag=Retry_Function_Flag,
        Default_Method_Flag=Default_Method_Flag,
        Retry_Method_Flag=Retry_Method_Flag,
        Default_Classmethod_Flag=Default_Classmethod_Flag,
        Retry_Classmethod_Flag=Retry_Classmethod_Flag,
        Default_Staticmethod_Flag=Default_Staticmethod_Flag,
        Retry_Staticmethod_Flag=Retry_Staticmethod_Flag,
        Async_Running=_Async_Running
    )
    return _run_func_falg


def instantiate_retry_decorator() -> None:
    retry()


def instantiate_async_retry_decorator() -> None:
    async_retry()


@retry.function
def target_function_with_default():
    """
    Function using retry mechanism with default processes.
    :return:
    """
    global Running_Target_Function_Counter, Default_Function_Flag
    Running_Target_Function_Counter += 1
    Default_Function_Flag = True
    return _Test_Return_Value


@retry.function
def target_function_raising_exception_with_default():
    """
    Same as target_function_with_default but this would raise an exception.
    :return:
    """
    global Running_Target_Function_Counter, Default_Function_Flag
    Running_Target_Function_Counter += 1
    Default_Function_Flag = True
    raise _Test_Exception



@retry.function(timeout=_Retry_Time)
def target_function():
    """
    Function using retry mechanism and implement all processes.
    :return:
    """
    global Running_Target_Function_Counter, Retry_Function_Flag
    Running_Target_Function_Counter += 1
    Retry_Function_Flag = True
    return _Test_Return_Value


@target_function.initialization
def _initial_func(*args, **kwargs):
    global Initial_Handling_Flag_Counter
    Initial_Handling_Flag_Counter += 1


@target_function.done_handling
def _done_func(result):
    global Done_Handling_Flag_Counter
    Done_Handling_Flag_Counter += 1
    return result


@target_function.final_handling
def _final_func():
    global Final_Handling_Flag_Counter
    Final_Handling_Flag_Counter += 1


@target_function.error_handling
def _error_func(e: Exception):
    global Error_Handling_Flag_Counter
    Error_Handling_Flag_Counter += 1
    return e



@retry.function(timeout=_Retry_Time)
def target_function_raising_exception():
    """
    Same as target_function but this would raise an exception.
    :return:
    """
    global Running_Target_Function_Counter, Retry_Function_Flag
    Running_Target_Function_Counter += 1
    Retry_Function_Flag = True
    raise _Test_Exception


@target_function_raising_exception.initialization
def _initial_func(*args, **kwargs):
    global Initial_Handling_Flag_Counter
    Initial_Handling_Flag_Counter += 1


@target_function_raising_exception.done_handling
def _done_func(result):
    global Done_Handling_Flag_Counter
    Done_Handling_Flag_Counter += 1
    return result


@target_function_raising_exception.final_handling
def _final_func():
    global Final_Handling_Flag_Counter
    Final_Handling_Flag_Counter += 1


@target_function_raising_exception.error_handling
def _error_func(e: Exception):
    global Error_Handling_Flag_Counter
    Error_Handling_Flag_Counter += 1
    return e



@async_retry.function
async def async_target_function_with_default():
    global Running_Target_Function_Counter, Default_Function_Flag, _Async_Running
    Running_Target_Function_Counter += 1
    Default_Function_Flag = True
    _Async_Running = True
    return _Test_Return_Value


@async_retry.function
async def async_target_function_raising_exception_with_default():
    global Running_Target_Function_Counter, Default_Function_Flag, _Async_Running
    Running_Target_Function_Counter += 1
    Default_Function_Flag = True
    _Async_Running = True
    raise _Test_Exception



@async_retry.function(timeout=_Retry_Time)
async def async_target_function():
    global Running_Target_Function_Counter, Retry_Function_Flag, _Async_Running
    Running_Target_Function_Counter += 1
    Retry_Function_Flag = True
    _Async_Running = True
    return _Test_Return_Value


@async_target_function.initialization
async def _initial_func(*args, **kwargs):
    global Initial_Handling_Flag_Counter
    Initial_Handling_Flag_Counter += 1


@async_target_function.done_handling
async def _done_func(result):
    global Done_Handling_Flag_Counter
    Done_Handling_Flag_Counter += 1
    return result


@async_target_function.final_handling
async def _final_func():
    global Final_Handling_Flag_Counter
    Final_Handling_Flag_Counter += 1


@async_target_function.error_handling
async def _error_func(e: Exception):
    global Error_Handling_Flag_Counter
    Error_Handling_Flag_Counter += 1
    return e



@async_retry.function(timeout=_Retry_Time)
async def async_target_function_raising_exception():
    global Running_Target_Function_Counter, Retry_Function_Flag, _Async_Running
    Running_Target_Function_Counter += 1
    Retry_Function_Flag = True
    _Async_Running = True
    raise _Test_Exception


@async_target_function_raising_exception.initialization
async def _async_initial_func(*args, **kwargs):
    global Initial_Handling_Flag_Counter
    Initial_Handling_Flag_Counter += 1


@async_target_function_raising_exception.done_handling
async def _async_done_func(result):
    global Done_Handling_Flag_Counter
    Done_Handling_Flag_Counter += 1
    return result


@async_target_function_raising_exception.final_handling
async def _async_final_func():
    global Final_Handling_Flag_Counter
    Final_Handling_Flag_Counter += 1


@async_target_function_raising_exception.error_handling
async def _async_error_func(e: Exception):
    global Error_Handling_Flag_Counter
    Error_Handling_Flag_Counter += 1
    return e



class TargetBoundedFunction:

    @retry.bounded_function
    def target_method_with_default(self):
        global Running_Target_Function_Counter, Default_Method_Flag
        Running_Target_Function_Counter += 1
        Default_Method_Flag = True
        return _Test_Return_Value


    @retry.bounded_function
    def target_method_raising_exception_with_default(self):
        global Running_Target_Function_Counter, Default_Method_Flag
        Running_Target_Function_Counter += 1
        Default_Method_Flag = True
        raise _Test_Exception


    @retry.bounded_function(timeout=_Retry_Time)
    def target_method(self):
        global Running_Target_Function_Counter, Retry_Method_Flag
        Running_Target_Function_Counter += 1
        Retry_Method_Flag = True
        return _Test_Return_Value


    @target_method.initialization
    def initial_function(self, *args, **kwargs):
        global Initial_Handling_Flag_Counter
        Initial_Handling_Flag_Counter += 1


    @target_method.done_handling
    def done_function(self, result):
        global Done_Handling_Flag_Counter
        Done_Handling_Flag_Counter += 1
        return result


    @target_method.final_handling
    def final_function(self):
        global Final_Handling_Flag_Counter
        Final_Handling_Flag_Counter += 1


    @target_method.error_handling
    def error_function(self, e: Exception):
        global Error_Handling_Flag_Counter
        Error_Handling_Flag_Counter += 1
        return e


    @retry.bounded_function(timeout=_Retry_Time)
    def target_method_raising_exception(self):
        global Running_Target_Function_Counter, Retry_Method_Flag
        Running_Target_Function_Counter += 1
        Retry_Method_Flag = True
        raise _Test_Exception


    @target_method_raising_exception.initialization
    def raising_exception_initial_function(self, *args, **kwargs):
        global Initial_Handling_Flag_Counter
        Initial_Handling_Flag_Counter += 1


    @target_method_raising_exception.done_handling
    def raising_exception_done_function(self, result):
        global Done_Handling_Flag_Counter
        Done_Handling_Flag_Counter += 1
        return result


    @target_method_raising_exception.error_handling
    def raising_exception_error_function(self, e: Exception):
        global Error_Handling_Flag_Counter
        Error_Handling_Flag_Counter += 1
        return e


    @target_method_raising_exception.final_handling
    def raising_exception_final_function(self):
        global Final_Handling_Flag_Counter
        Final_Handling_Flag_Counter += 1



class TargetBoundedAsyncFunction:

    @async_retry.bounded_function
    async def target_method_with_default(self):
        global Running_Target_Function_Counter, _Async_Running
        Running_Target_Function_Counter += 1
        _Async_Running = True
        return _Test_Return_Value


    @async_retry.bounded_function
    async def target_method_raising_exception_with_default(self):
        global Running_Target_Function_Counter, _Async_Running
        Running_Target_Function_Counter += 1
        _Async_Running = True
        raise _Test_Exception


    @async_retry.bounded_function(timeout=_Retry_Time)
    async def target_method(self):
        global Running_Target_Function_Counter, _Async_Running
        Running_Target_Function_Counter += 1
        _Async_Running = True
        return _Test_Return_Value


    @target_method.initialization
    async def async_initial_function(self, *args, **kwargs):
        global Initial_Handling_Flag_Counter
        Initial_Handling_Flag_Counter += 1


    @target_method.done_handling
    async def async_done_function(self, result):
        global Done_Handling_Flag_Counter
        Done_Handling_Flag_Counter += 1
        return result


    @target_method.final_handling
    async def async_final_function(self):
        global Final_Handling_Flag_Counter
        Final_Handling_Flag_Counter += 1


    @target_method.error_handling
    async def async_error_function(self, e: Exception):
        global Error_Handling_Flag_Counter
        Error_Handling_Flag_Counter += 1
        return e


    @async_retry.bounded_function(timeout=_Retry_Time)
    async def target_method_raising_exception(self):
        global Running_Target_Function_Counter, _Async_Running
        Running_Target_Function_Counter += 1
        _Async_Running = True
        raise _Test_Exception


    @target_method_raising_exception.initialization
    async def async_raising_exception_initial_function(self, *args, **kwargs):
        global Initial_Handling_Flag_Counter
        Initial_Handling_Flag_Counter += 1


    @target_method_raising_exception.done_handling
    async def async_raising_exception_done_function(self, result):
        global Done_Handling_Flag_Counter
        Done_Handling_Flag_Counter += 1
        return result


    @target_method_raising_exception.final_handling
    async def async_raising_exception_final_function(self):
        global Final_Handling_Flag_Counter
        Final_Handling_Flag_Counter += 1


    @target_method_raising_exception.error_handling
    async def async_raising_exception_error_function(self, e: Exception):
        global Error_Handling_Flag_Counter
        Error_Handling_Flag_Counter += 1
        return e


