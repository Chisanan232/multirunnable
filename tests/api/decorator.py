from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from multirunnable.mode import RunningMode, FeatureMode
from multirunnable.api.decorator import retry, async_retry, RunWith, AsyncRunWith
from multirunnable.adapter.lock import Lock, RLock, Semaphore, BoundedSemaphore
from multirunnable.adapter.communication import Event, Condition
from multirunnable.adapter.strategy import ExecutorStrategyAdapter
from multirunnable.coroutine.strategy import AsynchronousStrategy

from ..test_config import Worker_Size, Worker_Pool_Size, Task_Size, Semaphore_Value

from gevent.threading import get_ident as get_gevent_ident
from gevent import sleep as gevent_sleep
import threading
import asyncio
import pytest
import time
import re
import os


_Retry_Time = 4
_Default_Retry_Time = 1
Running_Target_Function_Counter: int = 0
Initial_Handling_Flag_Counter: int = 0
Done_Handling_Flag_Counter: int = 0
Final_Handling_Flag_Counter: int = 0
Error_Handling_Flag_Counter: int = 0

_Worker_Size = Worker_Size
_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size

_Semaphore_Value = Semaphore_Value

_Sleep_Time: int = 1
_Random_Start_Time: int = 60
_Random_End_Time: int = 80


def init_flag() -> None:
    global Running_Target_Function_Counter, Initial_Handling_Flag_Counter, Done_Handling_Flag_Counter, Final_Handling_Flag_Counter, Error_Handling_Flag_Counter
    Running_Target_Function_Counter = 0
    Initial_Handling_Flag_Counter = 0
    Done_Handling_Flag_Counter = 0
    Final_Handling_Flag_Counter = 0
    Error_Handling_Flag_Counter = 0


def instantiate_lock(_mode, **kwargs):
    _lock = Lock()
    return _initial(_lock, _mode, **kwargs)


def instantiate_rlock(_mode, **kwargs):
    _rlock = RLock()
    return _initial(_rlock, _mode, **kwargs)


def instantiate_semaphore(_mode, **kwargs):
    _semaphore = Semaphore(value=_Semaphore_Value)
    return _initial(_semaphore, _mode, **kwargs)


def instantiate_bounded_semaphore(_mode, **kwargs):
    _bounded_semaphore = BoundedSemaphore(value=_Semaphore_Value)
    return _initial(_bounded_semaphore, _mode, **kwargs)


def instantiate_event(_mode, **kwargs):
    _event = Event()
    return _initial(_event, _mode, **kwargs)


def instantiate_condition(_mode, **kwargs):
    _condition = Condition()
    return _initial(_condition, _mode, **kwargs)


def _initial(_feature_factory, _mode, **kwargs):
    _feature_factory.feature_mode = _mode
    _feature_instn = _feature_factory.get_instance(**kwargs)
    _feature_factory.globalize_instance(_feature_instn)
    return _feature_instn


def run_multi_process(_function):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Parallel, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _run_with_multiple_workers(_strategy, _function)


def run_multi_threads(_function):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Concurrent, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _run_with_multiple_workers(_strategy, _function)


def run_multi_green_thread(_function):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.GreenThread, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _run_with_multiple_workers(_strategy, _function)


def run_async(_function, _feature):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    async def __process():
        await _strategy.initialization(queue_tasks=None, features=_feature)
        _ps = [_strategy.generate_worker(_function) for _ in range(Worker_Size)]
        await _strategy.activate_workers(_ps)

    if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
        asyncio.run(__process(), debug=True)
    else:
        _event_loop = asyncio.get_event_loop()
        _event_loop.run_until_complete(__process())


def _run_with_multiple_workers(_strategy, _function):
    _ps = [_strategy.generate_worker(_function) for _ in range(Worker_Size)]
    _strategy.activate_workers(_ps)
    _strategy.close(_ps)



@retry
def target_function():
    global Running_Target_Function_Counter
    Running_Target_Function_Counter += 1


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



class TargetBoundedFunction:

    @retry
    def target_method_with_default(self):
        global Running_Target_Function_Counter
        Running_Target_Function_Counter += 1
        return "TestResult"


    @retry
    def target_method(self):
        global Running_Target_Function_Counter
        Running_Target_Function_Counter += 1


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



class TargetBoundedAsyncFunction:

    @async_retry
    async def target_method_with_default(self):
        global Running_Target_Function_Counter
        Running_Target_Function_Counter += 1


    @async_retry
    async def target_method(self):
        global Running_Target_Function_Counter
        Running_Target_Function_Counter += 1


    @target_method.initialization
    async def initial_function(self, *args, **kwargs):
        global Initial_Handling_Flag_Counter
        Initial_Handling_Flag_Counter += 1


    @target_method.done_handling
    async def done_function(self, result):
        global Done_Handling_Flag_Counter
        Done_Handling_Flag_Counter += 1
        return result


    @target_method.final_handling
    async def final_function(self):
        global Final_Handling_Flag_Counter
        Final_Handling_Flag_Counter += 1


    @target_method.error_handling
    async def error_function(self, e: Exception):
        global Error_Handling_Flag_Counter
        Error_Handling_Flag_Counter += 1
        return e



class JustTestException(Exception):

    def __str__(self):
        return "Just for testing to raise an exception."



class TargetErrorBoundedFunction:

    @retry
    def target_error_method_with_default(self):
        global Running_Target_Function_Counter
        Running_Target_Function_Counter += 1
        raise JustTestException


    @retry(timeout=_Retry_Time)
    def target_error_method(self):
        global Running_Target_Function_Counter
        Running_Target_Function_Counter += 1
        raise JustTestException


    @target_error_method.initialization
    def _initial(self, *args, **kwargs):
        global Initial_Handling_Flag_Counter
        Initial_Handling_Flag_Counter += 1


    @target_error_method.done_handling
    def _done(self, result):
        global Done_Handling_Flag_Counter
        Done_Handling_Flag_Counter += 1
        return result


    @target_error_method.final_handling
    def _final(self):
        global Final_Handling_Flag_Counter
        Final_Handling_Flag_Counter += 1


    @target_error_method.error_handling
    def _error(self, e: Exception):
        global Error_Handling_Flag_Counter
        Error_Handling_Flag_Counter += 1
        assert isinstance(e, JustTestException), f""
        print(f"[DEBUG] This is the customized error handling function.")
        return e



class TargetErrorBoundedAsyncFunction:

    @async_retry
    async def target_error_method_with_default(self):
        global Running_Target_Function_Counter
        Running_Target_Function_Counter += 1
        raise JustTestException


    @async_retry(timeout=_Retry_Time)
    async def target_error_method(self):
        global Running_Target_Function_Counter
        Running_Target_Function_Counter += 1
        raise JustTestException


    @target_error_method.initialization
    async def _initial(self, *args, **kwargs):
        global Initial_Handling_Flag_Counter
        Initial_Handling_Flag_Counter += 1


    @target_error_method.done_handling
    async def _done(self, result):
        global Done_Handling_Flag_Counter
        Done_Handling_Flag_Counter += 1
        return result


    @target_error_method.final_handling
    async def _final(self):
        global Final_Handling_Flag_Counter
        Final_Handling_Flag_Counter += 1


    @target_error_method.error_handling
    async def _error(self, e: Exception):
        global Error_Handling_Flag_Counter
        Error_Handling_Flag_Counter += 1
        assert isinstance(e, JustTestException), f""
        return e



@pytest.fixture(scope="class")
def target_bounded_function() -> TargetBoundedFunction:
    return TargetBoundedFunction()


@pytest.fixture(scope="class")
def target_error_bounded_function() -> TargetErrorBoundedFunction:
    return TargetErrorBoundedFunction()


@pytest.fixture(scope="class")
def target_bounded_async_function() -> TargetBoundedAsyncFunction:
    return TargetBoundedAsyncFunction()


@pytest.fixture(scope="class")
def target_error_bounded_async_function() -> TargetErrorBoundedAsyncFunction:
    return TargetErrorBoundedAsyncFunction()


@pytest.fixture(scope="class")
def async_strategy() -> AsynchronousStrategy:
    return AsynchronousStrategy(executors=_Worker_Size)


class TestRetryMechanism:

    @pytest.mark.skip(reason="Consider about the requirement necessary. It fail currently.")
    def test_retry_decorating_at_function(self):
        init_flag()

        target_function()
        assert Initial_Handling_Flag_Counter == 1, F"The initial handling flag should be 'True'."
        assert Done_Handling_Flag_Counter == 1, F"The done handling flag should be 'True'"
        assert Final_Handling_Flag_Counter == 1, F"The final handling flag should be 'True'"
        assert Error_Handling_Flag_Counter == 0, F"The error handling flag should be 'False'"


    def test_retry_decorating_at_bounded_function_with_default(self, target_bounded_function: TargetBoundedFunction):
        init_flag()

        _result = target_bounded_function.target_method_with_default()
        assert Initial_Handling_Flag_Counter == 1, F"The initial handling flag should be '1'."
        assert Done_Handling_Flag_Counter == 1, F"The done handling flag should be '1'"
        assert Final_Handling_Flag_Counter == 1, F"The final handling flag should be '1'"
        assert Error_Handling_Flag_Counter == 0, F"The error handling flag should be '0'"
        assert _result == "TestResult", f"The return value should be the same as 'TestResult'."


    def test_retry_decorating_at_bounded_function(self, target_bounded_function: TargetBoundedFunction):
        init_flag()

        target_bounded_function.target_method()
        assert Initial_Handling_Flag_Counter == 1, F"The initial handling flag should be '1'."
        assert Done_Handling_Flag_Counter == 1, F"The done handling flag should be '1'"
        assert Final_Handling_Flag_Counter == 1, F"The final handling flag should be '1'"
        assert Error_Handling_Flag_Counter == 0, F"The error handling flag should be '0'"


    @pytest.mark.skip(reason="An issue. It will fix it in version 0.17.0.")
    def test_retry_decorating_at_bounded_function_raising_an_exception_with_default(self):
        # target_error_bounded_function = TargetErrorBoundedFunction()
        _target_error_fun = TargetErrorBoundedFunction()

        init_flag()

        try:
            # _result = target_error_bounded_function.target_error_method_with_default()
            _result = _target_error_fun.target_error_method_with_default()
        except Exception as e:
            print(f"[DEBUG] this is except section code 1.")
            assert e is JustTestException, f""
            assert "Just for testing to raise an exception" in str(e), f""
            print(f"[DEBUG] this is except section code.")
        else:
            assert False, f"It should doesn't handle the exception and raise it out again."

        assert Initial_Handling_Flag_Counter == _Default_Retry_Time, F"The default timeout value is '{_Default_Retry_Time}' so that initial handling flag should be '{_Retry_Time}'."
        assert Done_Handling_Flag_Counter == 0, F"The default timeout value is '{_Default_Retry_Time}' so that done handling flag should be '0'"
        assert Final_Handling_Flag_Counter == _Default_Retry_Time, F"The default timeout value is '{_Default_Retry_Time}' so that final handling flag should be '{_Retry_Time}'"
        assert Error_Handling_Flag_Counter == _Default_Retry_Time, F"The default timeout value is '{_Default_Retry_Time}' so that error handling flag should be '{_Retry_Time}'"


    def test_retry_decorating_at_bounded_function_raising_an_exception(self, target_error_bounded_function: TargetErrorBoundedFunction):
        init_flag()

        _result = target_error_bounded_function.target_error_method()
        assert Initial_Handling_Flag_Counter == _Retry_Time, F"The initial handling flag should be '{_Retry_Time}'."
        assert Done_Handling_Flag_Counter == 0, F"The done handling flag should be '0'"
        assert Final_Handling_Flag_Counter == _Retry_Time, F"The final handling flag should be '{_Retry_Time}'"
        assert Error_Handling_Flag_Counter == _Retry_Time, F"The error handling flag should be '{_Retry_Time}'"


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_retry_decorating_at_classmethod_function(self, target_bounded_function: TargetBoundedFunction):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_retry_decorating_at_staticmethod_function(self, target_bounded_function: TargetBoundedFunction):
        pass



class TestAsyncRetryMechanism:

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_async_retry_decorating_at_function(self):
        pass


    def test_async_retry_decorating_at_bounded_function_with_default(self, async_strategy: AsynchronousStrategy, target_bounded_async_function: TargetBoundedAsyncFunction):
        init_flag()

        async_strategy.run(function=target_bounded_async_function.target_method_with_default)
        assert Initial_Handling_Flag_Counter == _Worker_Size, F"The count of initial handling flag should be '{_Worker_Size}'."
        assert Done_Handling_Flag_Counter == _Worker_Size, F"The count of done handling flag should be '{_Worker_Size}'"
        assert Final_Handling_Flag_Counter == _Worker_Size, F"The count of final handling flag should be '{_Worker_Size}'"
        assert Error_Handling_Flag_Counter == 0, F"The count of error handling flag should be '0'"


    def test_async_retry_decorating_at_bounded_function(self, async_strategy: AsynchronousStrategy, target_bounded_async_function: TargetBoundedAsyncFunction):
        init_flag()

        async_strategy.run(function=target_bounded_async_function.target_method)
        assert Initial_Handling_Flag_Counter == _Worker_Size, F"The count of initial handling flag should be '{_Worker_Size}'."
        assert Done_Handling_Flag_Counter == _Worker_Size, F"The count of done handling flag should be '{_Worker_Size}'"
        assert Final_Handling_Flag_Counter == _Worker_Size, F"The count of final handling flag should be '{_Worker_Size}'"
        assert Error_Handling_Flag_Counter == 0, F"The count of error handling flag should be '0'"


    def test_async_retry_decorating_at_bounded_function_raising_an_exception_with_default(self, async_strategy: AsynchronousStrategy, target_error_bounded_async_function: TargetErrorBoundedAsyncFunction):
        init_flag()

        async_strategy.run(function=target_error_bounded_async_function.target_error_method_with_default)

        assert Initial_Handling_Flag_Counter == _Default_Retry_Time * _Worker_Size, F"The default timeout value is '{_Default_Retry_Time}' so that count of initial handling flag should be '{_Default_Retry_Time * _Worker_Size}'."
        assert Done_Handling_Flag_Counter == 0, F"The default timeout value is '{_Default_Retry_Time}' so that count of done handling flag should be 'False'"
        assert Final_Handling_Flag_Counter == _Default_Retry_Time * _Worker_Size, F"The default timeout value is '{_Default_Retry_Time}' so that count of final handling flag should be '{_Default_Retry_Time * _Worker_Size}'"
        assert Error_Handling_Flag_Counter == _Default_Retry_Time * _Worker_Size, F"The default timeout value is '{_Default_Retry_Time}' so that count of error handling flag should be '{_Default_Retry_Time * _Worker_Size}'"


    def test_async_retry_decorating_at_bounded_function_raising_an_exception(self, async_strategy: AsynchronousStrategy, target_error_bounded_async_function: TargetErrorBoundedAsyncFunction):
        init_flag()

        async_strategy.run(function=target_error_bounded_async_function.target_error_method)
        assert Initial_Handling_Flag_Counter == _Retry_Time * _Worker_Size, F"The count of initial handling flag should be '{_Retry_Time * _Worker_Size}'."
        assert Done_Handling_Flag_Counter == 0, F"The count of done handling flag should be 'False'"
        assert Final_Handling_Flag_Counter == _Retry_Time * _Worker_Size, F"The count of final handling flag should be '{_Retry_Time * _Worker_Size}'"
        assert Error_Handling_Flag_Counter == _Retry_Time * _Worker_Size, F"The count of error handling flag should be '{_Retry_Time * _Worker_Size}'"


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_async_retry_decorating_at_classmethod_function(self):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_async_retry_decorating_at_staticmethod_function(self):
        pass



class TestFeaturesDecorator:

    @pytest.mark.skip(reason="Not finish yet.")
    def test_lock_decorator_in_parallel(self):

        _done_timestamp = {}
        instantiate_lock(FeatureMode.Parallel)

        @RunWith.Lock
        def _target_testing():
            # Save a timestamp into list
            _process_id = os.getpid()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_process_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_multi_process(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_lock_decorator_in_concurrent(self):

        _done_timestamp = {}
        instantiate_lock(FeatureMode.Concurrent)

        @RunWith.Lock
        def _target_testing():
            # Save a timestamp into list
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_lock_decorator_in_green_thread(self):

        _done_timestamp = {}
        instantiate_lock(FeatureMode.GreenThread)

        @RunWith.Lock
        def _target_testing():
            # Save a timestamp into list
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_multi_green_thread(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_rlock_decorator_in_concurrent(self):

        _done_timestamp = {}
        instantiate_rlock(FeatureMode.Concurrent)

        @RunWith.RLock
        def _target_testing():
            # Save a timestamp into list
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_rlock_decorator_in_green_thread(self):

        _done_timestamp = {}
        instantiate_rlock(FeatureMode.GreenThread)

        @RunWith.RLock
        def _target_testing():
            # Save a timestamp into list
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_multi_green_thread(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    @pytest.mark.skip(reason="Not finish yet.")
    def test_semaphore_decorator_in_parallel(self):

        _done_timestamp = {}
        instantiate_semaphore(FeatureMode.Parallel)

        @RunWith.Semaphore
        def _target_testing():
            # Save a timestamp into list
            _process_id = os.getpid()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_process_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_semaphore_decorator_in_concurrent(self):

        _done_timestamp = {}
        instantiate_semaphore(FeatureMode.Concurrent)

        @RunWith.Semaphore
        def _target_testing():
            # Save a timestamp into list
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_semaphore_decorator_in_green_thread(self):

        _done_timestamp = {}
        instantiate_semaphore(FeatureMode.GreenThread)

        @RunWith.Semaphore
        def _target_testing():
            # Save a timestamp into list
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_multi_green_thread(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    @pytest.mark.skip(reason="Not finish yet.")
    def test_bounded_semaphore_decorator_in_parallel(self):

        _done_timestamp = {}
        instantiate_bounded_semaphore(FeatureMode.Concurrent)

        @RunWith.Bounded_Semaphore
        def _target_testing():
            # Save a time stamp into list
            try:
                _process_id = os.getpid()
                time.sleep(_Sleep_Time)
                _time = float(time.time())
                _done_timestamp[_process_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. \n" \
                              f"Exception: {e}"
            else:
                assert True, f"Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        run_multi_process(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_bounded_semaphore_decorator_in_concurrent(self):

        _done_timestamp = {}
        instantiate_bounded_semaphore(FeatureMode.Concurrent)

        @RunWith.Bounded_Semaphore
        def _target_testing():
            # Save a time stamp into list
            try:
                _thread_id = threading.get_ident()
                time.sleep(_Sleep_Time)
                _time = float(time.time())
                _done_timestamp[_thread_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. \n" \
                              f"Exception: {e}"
            else:
                assert True, f"Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_bounded_semaphore_decorator_in_green_thread(self):

        _done_timestamp = {}
        instantiate_bounded_semaphore(FeatureMode.GreenThread)

        @RunWith.Bounded_Semaphore
        def _target_testing():
            # Save a time stamp into list
            try:
                _thread_id = get_gevent_ident()
                gevent_sleep(_Sleep_Time)
                _time = float(time.time())
                _done_timestamp[_thread_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. \n" \
                              f"Exception: {e}"
            else:
                assert True, f"Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        run_multi_green_thread(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp_by_lock(_done_timestamp: dict):
        assert len(_done_timestamp.keys()) == _Worker_Size, f"The amount of thread ID keys (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(set(_done_timestamp.keys())) == _Worker_Size, f"The amount of thread ID keys (de-duplicate) should be equal to worker size '{_Worker_Size}'."
        _previous_v = None
        for _v in sorted(_done_timestamp.values()):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time betweeen them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_done_timestamp}"
                _previous_v = _v


    @staticmethod
    def _chk_done_timestamp_by_semaphore(_done_timestamp: dict):
        assert len(_done_timestamp.keys()) == _Worker_Size, f"The amount of thread ID keys (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(set(_done_timestamp.keys())) == _Worker_Size, f"The amount of thread ID keys (de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(_done_timestamp.values()) == _Worker_Size, f"The amount of done-timestamp (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        _int_unix_time_timestamps = [int(_v) for _v in _done_timestamp.values()]
        if _Worker_Size % 2 == 0:
            assert len(set(_int_unix_time_timestamps)) == int(_Worker_Size / _Semaphore_Value), \
                f"The amount of done-timestamp (de-duplicate) should be equal to (worker size: {_Worker_Size} / semaphore value: {_Semaphore_Value}) '{int(_Worker_Size / _Semaphore_Value)}'."
        else:
            assert len(set(_int_unix_time_timestamps)) == int(_Worker_Size / _Semaphore_Value) + 1, \
                f"The amount of done-timestamp (de-duplicate) should be equal to (worker size: {_Worker_Size} / semaphore value: {_Semaphore_Value}) '{int(_Worker_Size / _Semaphore_Value)}'."
        _previous_v = None
        for _v in sorted(_int_unix_time_timestamps):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time betweeen them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_done_timestamp}"
                _previous_v = _v



class TestAsyncFeaturesDecorator:

    def test_lock_decorator(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}
        instantiate_lock(FeatureMode.Asynchronous, event_loop=_event_loop)

        @AsyncRunWith.Lock
        async def _target_testing():
            # Save a timestamp into list
            await asyncio.sleep(_Sleep_Time)
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _current_task = asyncio.current_task()
            else:
                _current_task = asyncio.Task.current_task()
            _current_task_id = id(_current_task)
            _time = float(time.time())
            _done_timestamp[_current_task_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=Lock())
        TestAsyncFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_semaphore_decorator(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}
        instantiate_semaphore(FeatureMode.Asynchronous, event_loop=_event_loop)

        @AsyncRunWith.Semaphore
        async def _target_testing():
            # Save a timestamp into list
            await asyncio.sleep(_Sleep_Time)
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _current_task = asyncio.current_task()
            else:
                _current_task = asyncio.Task.current_task()
            _current_task_id = id(_current_task)
            _time = float(time.time())
            _done_timestamp[_current_task_id] = _time

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=Semaphore(value=_Semaphore_Value))
        TestAsyncFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_bounded_semaphore_decorator(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}
        instantiate_bounded_semaphore(FeatureMode.Asynchronous, event_loop=_event_loop)

        @AsyncRunWith.Bounded_Semaphore
        async def _target_testing():
            # Save a time stamp into list
            try:
                await asyncio.sleep(_Sleep_Time)
                if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                    _current_task = asyncio.current_task()
                else:
                    _current_task = asyncio.Task.current_task()
                _current_task_id = id(_current_task)
                _time = float(time.time())
                _done_timestamp[_current_task_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. \n" \
                              f"Exception: {e}"
            else:
                assert True, f"Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=BoundedSemaphore(value=_Semaphore_Value))
        TestAsyncFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp_by_lock(_done_timestamp: dict):
        assert len(_done_timestamp.keys()) == _Worker_Size, f"The amount of thread ID keys (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(set(_done_timestamp.keys())) == _Worker_Size, f"The amount of thread ID keys (de-duplicate) should be equal to worker size '{_Worker_Size}'."
        _previous_v = None
        for _v in sorted(_done_timestamp.values()):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time betweeen them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_done_timestamp}"
                _previous_v = _v


    @staticmethod
    def _chk_done_timestamp_by_semaphore(_done_timestamp: dict):
        assert len(_done_timestamp.keys()) == _Worker_Size, f"The amount of thread ID keys (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(set(_done_timestamp.keys())) == _Worker_Size, f"The amount of thread ID keys (de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(_done_timestamp.values()) == _Worker_Size, f"The amount of done-timestamp (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        _int_unix_time_timestamps = [int(_v) for _v in _done_timestamp.values()]
        if _Worker_Size % 2 == 0:
            assert len(set(_int_unix_time_timestamps)) == int(_Worker_Size / _Semaphore_Value), \
                f"The amount of done-timestamp (de-duplicate) should be equal to (worker size: {_Worker_Size} / semaphore value: {_Semaphore_Value}) '{int(_Worker_Size / _Semaphore_Value)}'."
        else:
            assert len(set(_int_unix_time_timestamps)) == int(_Worker_Size / _Semaphore_Value) + 1, \
                f"The amount of done-timestamp (de-duplicate) should be equal to (worker size: {_Worker_Size} / semaphore value: {_Semaphore_Value}) '{int(_Worker_Size / _Semaphore_Value)}'."
        _previous_v = None
        for _v in sorted(_int_unix_time_timestamps):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time betweeen them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_done_timestamp}"
                _previous_v = _v

