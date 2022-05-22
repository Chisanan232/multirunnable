from gevent.threading import get_ident as get_gevent_ident
from gevent import sleep as gevent_sleep
from typing import Callable
import threading
import asyncio
import pytest
import time
import os
import re

from multirunnable.coroutine.strategy import AsynchronousStrategy
from multirunnable.parallel.share import Global_Manager
from multirunnable.api.decorator import RunWith, AsyncRunWith
from multirunnable.factory.lock import LockFactory, SemaphoreFactory, BoundedSemaphoreFactory
from multirunnable.mode import RunningMode
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ...test_config import Worker_Size, Worker_Pool_Size, Task_Size, Semaphore_Value
from ..._examples import RunByStrategy
from ..._examples_with_synchronization import (
    instantiate_lock, instantiate_rlock,
    instantiate_semaphore, instantiate_bounded_semaphore
)
from ..framework.lock import LockTestSpec, SemaphoreTestSpec
from ._retry_sample import (
    _Retry_Time, _Default_Retry_Time, _Test_Return_Value, _Test_Exception,
    instantiate_retry_decorator, instantiate_async_retry_decorator, init_flag, get_process_flag,
    target_function_with_default, target_function_raising_exception_with_default,
    target_function, target_function_raising_exception,
    async_target_function_with_default, async_target_function_raising_exception_with_default,
    async_target_function, async_target_function_raising_exception,
    TargetBoundedFunction, TargetBoundedAsyncFunction
)


_Worker_Size = Worker_Size
_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size

_Semaphore_Value = Semaphore_Value

_Sleep_Time: int = 1
_Random_Start_Time: int = 60
_Random_End_Time: int = 80

_Default_Value: int = 1


@pytest.fixture(scope="class")
def target_bounded_function() -> TargetBoundedFunction:
    return TargetBoundedFunction()


@pytest.fixture(scope="class")
def target_bounded_async_function() -> TargetBoundedAsyncFunction:
    return TargetBoundedAsyncFunction()


@pytest.fixture(scope="class")
def async_strategy() -> AsynchronousStrategy:
    return AsynchronousStrategy(executors=_Worker_Size)


def _test_instantiate_decorator(instantiate_decorator: Callable) -> None:
    try:
        instantiate_decorator()
    except RuntimeError as e:
        _error_msg = re.search(r"It shouldn't instantiate \w{2,64} object.", str(e))
        assert _error_msg is not None, "It should raise a RuntimeError about it cannot instantiate static factory."
    else:
        assert False, "It should raise a RuntimeError about it cannot instantiate static factory."


class TestRetryMechanism:

    def test_cannot_instantiate_decorator(self):
        _test_instantiate_decorator(instantiate_retry_decorator)


    def test_retry_decorating_at_function_with_default(self):
        init_flag()

        _result = target_function_with_default()
        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Default_Value, f"The running counter flag should be '{_Default_Value}'"
        assert _process_flag.Initial_Handling_Flag_Counter == 0, "The initial handling flag should be '0'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, "The done handling flag should be '0'"
        assert _process_flag.Final_Handling_Flag_Counter == 0, "The final handling flag should be '0'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The error handling flag should be '0'"
        assert _result == _Test_Return_Value, f"The return value should be the same as '{_Test_Return_Value}'."


    def test_retry_decorating_at_function_raising_exception_with_default(self):
        init_flag()

        try:
            target_function_raising_exception_with_default()
        except Exception as e:
            assert e is _Test_Exception, ""
            assert "Test for raising exception" in str(e), ""
        else:
            assert False, "It should doesn't handle the exception and raise it out again."

        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Default_Value, f"The running counter flag should be '{_Default_Value}'"
        assert _process_flag.Initial_Handling_Flag_Counter == 0, "The initial handling flag should be '0'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, "The done handling flag should be '0'"
        assert _process_flag.Final_Handling_Flag_Counter == 0, "The final handling flag should be '0'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The error handling flag should be '0'"


    def test_retry_decorating_at_function(self):
        init_flag()

        _result = target_function()
        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Default_Value, f"The running counter flag should be '{_Default_Value}'"
        assert _process_flag.Initial_Handling_Flag_Counter == _Default_Value, f"The initial handling flag should be '{_Default_Value}'."
        assert _process_flag.Done_Handling_Flag_Counter == _Default_Value, f"The done handling flag should be '{_Default_Value}'"
        assert _process_flag.Final_Handling_Flag_Counter == _Default_Value, f"The final handling flag should be '{_Default_Value}'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The error handling flag should be 'False'"
        assert _result == _Test_Return_Value, f"The return value should be the same as '{_Test_Return_Value}'."


    def test_retry_decorating_at_function_raising_exception(self):
        init_flag()

        target_function_raising_exception()
        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Retry_Time, f"The running counter flag should be '{_Retry_Time}'"
        assert _process_flag.Initial_Handling_Flag_Counter == _Retry_Time, f"The initial handling flag should be '{_Retry_Time}'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, "The done handling flag should be '0'"
        assert _process_flag.Final_Handling_Flag_Counter == _Retry_Time, f"The final handling flag should be '{_Retry_Time}'"
        assert _process_flag.Error_Handling_Flag_Counter == _Retry_Time, f"The error handling flag should be '{_Retry_Time}'"


    def test_retry_decorating_at_bounded_function_with_default(self, target_bounded_function: TargetBoundedFunction):
        init_flag()

        _result = target_bounded_function.target_method_with_default()
        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Default_Value, "The running counter flag should be '0'."
        assert _process_flag.Initial_Handling_Flag_Counter == 0, "The initial handling flag should be '0'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, "The done handling flag should be '0'"
        assert _process_flag.Final_Handling_Flag_Counter == 0, "The final handling flag should be '0'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The error handling flag should be '0'"
        assert _result == _Test_Return_Value, f"The return value should be the same as '{_Test_Return_Value}'."


    def test_retry_decorating_at_bounded_function_raising_exception_with_default(self, target_bounded_function: TargetBoundedFunction):
        init_flag()

        try:
            _result = target_bounded_function.target_method_raising_exception_with_default()
        except Exception as e:
            assert e is _Test_Exception, ""
            assert "Test for raising exception" in str(e), ""
        else:
            assert False, "It should doesn't handle the exception and raise it out again."

        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Default_Retry_Time, f"The running counter flag should be '{_Default_Retry_Time}'."
        assert _process_flag.Initial_Handling_Flag_Counter == 0, f"The default timeout value is '{_Default_Retry_Time}' so that initial handling flag should be '0'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, f"The default timeout value is '{_Default_Retry_Time}' so that done handling flag should be '0'"
        assert _process_flag.Final_Handling_Flag_Counter == 0, f"The default timeout value is '{_Default_Retry_Time}' so that final handling flag should be '0'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, f"The default timeout value is '{_Default_Retry_Time}' so that error handling flag should be '0'"


    def test_retry_decorating_at_bounded_function(self, target_bounded_function: TargetBoundedFunction):
        init_flag()

        _result = target_bounded_function.target_method()
        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Default_Value, f"The running counter flag should be '{_Default_Value}'."
        assert _process_flag.Initial_Handling_Flag_Counter == _Default_Value, f"The initial handling flag should be '{_Default_Value}'."
        assert _process_flag.Done_Handling_Flag_Counter == _Default_Value, f"The done handling flag should be '{_Default_Value}'"
        assert _process_flag.Final_Handling_Flag_Counter == _Default_Value, f"The final handling flag should be '{_Default_Value}'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The error handling flag should be '0'"
        assert _result == _Test_Return_Value, f"The return value should be the same as '{_Test_Return_Value}'."


    def test_retry_decorating_at_bounded_function_raising_exception(self, target_bounded_function: TargetBoundedFunction):
        init_flag()

        _result = target_bounded_function.target_method_raising_exception()
        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Retry_Time, f"The running counter flag should be '{_Retry_Time}'."
        assert _process_flag.Initial_Handling_Flag_Counter == _Retry_Time, f"The initial handling flag should be '{_Retry_Time}'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, "The done handling flag should be '0'"
        assert _process_flag.Final_Handling_Flag_Counter == _Retry_Time, f"The final handling flag should be '{_Retry_Time}'"
        assert _process_flag.Error_Handling_Flag_Counter == _Retry_Time, f"The error handling flag should be '{_Retry_Time}'"



class TestAsyncRetryMechanism:

    def test_cannot_instantiate_decorator(self):
        _test_instantiate_decorator(instantiate_async_retry_decorator)


    def test_async_retry_decorating_at_function_with_default(self, async_strategy: AsynchronousStrategy):
        init_flag()

        async_strategy.run(function=async_target_function_with_default)
        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Default_Value * _Worker_Size, f"The running counter flag should be '{_Default_Value}'"
        assert _process_flag.Initial_Handling_Flag_Counter == 0, "The initial handling flag should be '0'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, "The done handling flag should be '0'"
        assert _process_flag.Final_Handling_Flag_Counter == 0, "The final handling flag should be '0'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The error handling flag should be '0'"

        _result = async_strategy.get_result()
        _result_content = [_r.data for _r in _result]
        _result_content_one_list = list(set(_result_content))

        assert len(_result_content_one_list) == 1 and _result_content_one_list[0] == _Test_Return_Value, f"The return value should be the same as '{_Test_Return_Value}'."


    def test_async_retry_decorating_at_function_with_default_raising_exception(self, async_strategy: AsynchronousStrategy):
        init_flag()

        async_strategy.run(function=async_target_function_raising_exception_with_default)
        _result = async_strategy.get_result()

        _result_content = [_r.data for _r in _result]
        _result_exception_content = [_r.exception for _r in _result]

        _result_content_set = set(_result_content)
        _result_exception_content_set = set(_result_exception_content)

        assert len(_result_content_set) == 1 and list(_result_content_set)[0] is None, f""
        assert len(_result_exception_content_set) == 1 and list(_result_exception_content_set)[0] is _Test_Exception, f""

        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Default_Value * _Worker_Size, F"The running counter flag should be '{_Default_Value}'"
        assert _process_flag.Initial_Handling_Flag_Counter == 0, "The initial handling flag should be '0'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, "The done handling flag should be '0'"
        assert _process_flag.Final_Handling_Flag_Counter == 0, "The final handling flag should be '0'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The error handling flag should be '0'"


    def test_async_retry_decorating_at_function(self, async_strategy: AsynchronousStrategy):
        init_flag()

        async_strategy.run(function=async_target_function)

        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Default_Value * _Worker_Size, f"The running counter flag should be '{_Default_Value}'"
        assert _process_flag.Initial_Handling_Flag_Counter == _Default_Value * _Worker_Size, f"The initial handling flag should be '{_Default_Value}'."
        assert _process_flag.Done_Handling_Flag_Counter == _Default_Value * _Worker_Size, f"The done handling flag should be '{_Default_Value}'"
        assert _process_flag.Final_Handling_Flag_Counter == _Default_Value * _Worker_Size, f"The final handling flag should be '{_Default_Value}'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The error handling flag should be 'False'"

        _result = async_strategy.get_result()
        _result_content = [_r.data for _r in _result]
        _result_content_one_list = list(set(_result_content))

        assert len(_result_content_one_list) == 1 and _result_content_one_list[0] == _Test_Return_Value, f"The return value should be the same as '{_Test_Return_Value}'."


    def test_async_retry_decorating_at_function_raising_exception(self, async_strategy: AsynchronousStrategy):
        init_flag()

        async_strategy.run(function=async_target_function_raising_exception)

        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Retry_Time * _Worker_Size, f"The running counter flag should be '{_Retry_Time}'"
        assert _process_flag.Initial_Handling_Flag_Counter == _Retry_Time * _Worker_Size, f"The initial handling flag should be '{_Retry_Time}'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, "The done handling flag should be '0'"
        assert _process_flag.Final_Handling_Flag_Counter == _Retry_Time * _Worker_Size, f"The final handling flag should be '{_Retry_Time}'"
        assert _process_flag.Error_Handling_Flag_Counter == _Retry_Time * _Worker_Size, f"The error handling flag should be '{_Retry_Time}'"


    def test_async_retry_decorating_at_bounded_function_with_default(self, async_strategy: AsynchronousStrategy, target_bounded_async_function: TargetBoundedAsyncFunction):
        init_flag()

        async_strategy.run(function=target_bounded_async_function.target_method_with_default)

        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Worker_Size, f"The running counter flag should be '{_Worker_Size}'."
        assert _process_flag.Initial_Handling_Flag_Counter == 0, f"The count of initial handling flag should be '{_Worker_Size}'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, f"The count of done handling flag should be '{_Worker_Size}'"
        assert _process_flag.Final_Handling_Flag_Counter == 0, f"The count of final handling flag should be '{_Worker_Size}'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The count of error handling flag should be '0'"


    def test_async_retry_decorating_at_bounded_function_raising_exception_with_default(self, async_strategy: AsynchronousStrategy, target_bounded_async_function: TargetBoundedAsyncFunction):
        init_flag()

        async_strategy.run(function=target_bounded_async_function.target_method_raising_exception_with_default)

        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Worker_Size, f"The running counter flag should be '{_Worker_Size}'."
        assert _process_flag.Initial_Handling_Flag_Counter == 0, f"The default timeout value is '{_Default_Retry_Time}' so that count of initial handling flag should be '{_Default_Retry_Time * _Worker_Size}'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, f"The default timeout value is '{_Default_Retry_Time}' so that count of done handling flag should be 'False'"
        assert _process_flag.Final_Handling_Flag_Counter == 0, f"The default timeout value is '{_Default_Retry_Time}' so that count of final handling flag should be '{_Default_Retry_Time * _Worker_Size}'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, f"The default timeout value is '{_Default_Retry_Time}' so that count of error handling flag should be '{_Default_Retry_Time * _Worker_Size}'"


    def test_async_retry_decorating_at_bounded_function(self, async_strategy: AsynchronousStrategy, target_bounded_async_function: TargetBoundedAsyncFunction):
        init_flag()

        async_strategy.run(function=target_bounded_async_function.target_method)

        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Worker_Size, f"The running counter flag should be '{_Worker_Size}'."
        assert _process_flag.Initial_Handling_Flag_Counter == _Worker_Size, f"The count of initial handling flag should be '{_Worker_Size}'."
        assert _process_flag.Done_Handling_Flag_Counter == _Worker_Size, f"The count of done handling flag should be '{_Worker_Size}'"
        assert _process_flag.Final_Handling_Flag_Counter == _Worker_Size, f"The count of final handling flag should be '{_Worker_Size}'"
        assert _process_flag.Error_Handling_Flag_Counter == 0, "The count of error handling flag should be '0'"


    def test_async_retry_decorating_at_bounded_function_raising_exception(self, async_strategy: AsynchronousStrategy, target_bounded_async_function: TargetBoundedAsyncFunction):
        init_flag()

        async_strategy.run(function=target_bounded_async_function.target_method_raising_exception)

        _process_flag = get_process_flag()

        assert _process_flag.Running_Target_Function_Counter == _Retry_Time * _Worker_Size, f"The running counter flag should be '{_Worker_Size}'."
        assert _process_flag.Initial_Handling_Flag_Counter == _Retry_Time * _Worker_Size, f"The count of initial handling flag should be '{_Retry_Time * _Worker_Size}'."
        assert _process_flag.Done_Handling_Flag_Counter == 0, "The count of done handling flag should be 'False'"
        assert _process_flag.Final_Handling_Flag_Counter == _Retry_Time * _Worker_Size, f"The count of final handling flag should be '{_Retry_Time * _Worker_Size}'"
        assert _process_flag.Error_Handling_Flag_Counter == _Retry_Time * _Worker_Size, f"The count of error handling flag should be '{_Retry_Time * _Worker_Size}'"



class TestFeaturesDecorator:

    def test_cannot_instantiate_decorator(self):
        _test_instantiate_decorator(RunWith)


    def test_lock_decorator_in_parallel(self):

        _done_timestamp = Global_Manager.dict()
        instantiate_lock(RunningMode.Parallel)

        @RunWith.Lock
        def _target_testing():
            # Save a timestamp into list
            _process_id = os.getpid()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_process_id] = _time

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.Parallel(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_lock_decorator_in_concurrent(self):

        _done_timestamp = {}
        instantiate_lock(RunningMode.Concurrent)

        @RunWith.Lock
        def _target_testing():
            # Save a timestamp into list
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.Concurrent(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_lock_decorator_in_green_thread(self):

        _done_timestamp = {}
        instantiate_lock(RunningMode.GreenThread)

        @RunWith.Lock
        def _target_testing():
            # Save a timestamp into list
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.CoroutineWithGreenThread(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_rlock_decorator_in_concurrent(self):

        _done_timestamp = {}
        instantiate_rlock(RunningMode.Concurrent)

        @RunWith.RLock
        def _target_testing():
            # Save a timestamp into list
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.Concurrent(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_rlock_decorator_in_green_thread(self):

        _done_timestamp = {}
        instantiate_rlock(RunningMode.GreenThread)

        @RunWith.RLock
        def _target_testing():
            # Save a timestamp into list
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.CoroutineWithGreenThread(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_semaphore_decorator_in_parallel(self):

        _done_timestamp = Global_Manager.dict()
        instantiate_semaphore(RunningMode.Parallel)

        @RunWith.Semaphore
        def _target_testing():
            # Save a timestamp into list
            _process_id = os.getpid()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_process_id] = _time

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.Parallel(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_semaphore_decorator_in_concurrent(self):

        _done_timestamp = {}
        instantiate_semaphore(RunningMode.Concurrent)

        @RunWith.Semaphore
        def _target_testing():
            # Save a timestamp into list
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.Concurrent(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_semaphore_decorator_in_green_thread(self):

        _done_timestamp = {}
        instantiate_semaphore(RunningMode.GreenThread)

        @RunWith.Semaphore
        def _target_testing():
            # Save a timestamp into list
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.CoroutineWithGreenThread(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_bounded_semaphore_decorator_in_parallel(self):

        _done_timestamp = Global_Manager.dict()
        instantiate_bounded_semaphore(RunningMode.Parallel)

        @RunWith.Bounded_Semaphore
        def _target_testing():
            # Save a time stamp into list
            try:
                _process_id = os.getpid()
                time.sleep(_Sleep_Time)
                _time = float(time.time())
                _done_timestamp[_process_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.Parallel(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_bounded_semaphore_decorator_in_concurrent(self):

        _done_timestamp = {}
        instantiate_bounded_semaphore(RunningMode.Concurrent)

        @RunWith.Bounded_Semaphore
        def _target_testing():
            # Save a time stamp into list
            try:
                _thread_id = threading.get_ident()
                time.sleep(_Sleep_Time)
                _time = float(time.time())
                _done_timestamp[_thread_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.Concurrent(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_bounded_semaphore_decorator_in_green_thread(self):

        _done_timestamp = {}
        instantiate_bounded_semaphore(RunningMode.GreenThread)

        @RunWith.Bounded_Semaphore
        def _target_testing():
            # Save a time stamp into list
            try:
                _thread_id = get_gevent_ident()
                gevent_sleep(_Sleep_Time)
                _time = float(time.time())
                _done_timestamp[_thread_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.CoroutineWithGreenThread(_function=_target_testing)
        TestFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp_by_lock(_done_timestamp: dict):
        LockTestSpec._chk_done_timestamp(_done_timestamp=_done_timestamp)


    @staticmethod
    def _chk_done_timestamp_by_semaphore(_done_timestamp: dict):
        SemaphoreTestSpec._chk_done_timestamp(_done_timestamp=_done_timestamp)



class TestAsyncFeaturesDecorator:

    def test_cannot_instantiate_decorator(self):
        _test_instantiate_decorator(AsyncRunWith)


    def test_lock_decorator(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}
        instantiate_lock(RunningMode.Asynchronous, event_loop=_event_loop)

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
        RunByStrategy.CoroutineWithAsynchronous(_function=_target_testing, _feature=LockFactory())
        TestAsyncFeaturesDecorator._chk_done_timestamp_by_lock(_done_timestamp)


    def test_semaphore_decorator(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}
        instantiate_semaphore(RunningMode.Asynchronous, event_loop=_event_loop)

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
        RunByStrategy.CoroutineWithAsynchronous(_function=_target_testing, _feature=SemaphoreFactory(value=_Semaphore_Value))
        TestAsyncFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    def test_bounded_semaphore_decorator(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}
        instantiate_bounded_semaphore(RunningMode.Asynchronous, event_loop=_event_loop)

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
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        RunByStrategy.CoroutineWithAsynchronous(_function=_target_testing, _feature=BoundedSemaphoreFactory(value=_Semaphore_Value))
        TestAsyncFeaturesDecorator._chk_done_timestamp_by_semaphore(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp_by_lock(_done_timestamp: dict):
        LockTestSpec._chk_done_timestamp(_done_timestamp=_done_timestamp)


    @staticmethod
    def _chk_done_timestamp_by_semaphore(_done_timestamp: dict):
        SemaphoreTestSpec._chk_done_timestamp(_done_timestamp=_done_timestamp)

