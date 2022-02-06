from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from multirunnable.mode import RunningMode, FeatureMode
from multirunnable.api.decorator import (
    RunWith, AsyncRunWith
)
from multirunnable.factory.lock import LockFactory, RLockFactory, SemaphoreFactory, BoundedSemaphoreFactory
from multirunnable.factory.communication import EventFactory, ConditionFactory
from multirunnable.factory.strategy import ExecutorStrategyAdapter
from multirunnable.coroutine.strategy import AsynchronousStrategy

from ..test_config import Worker_Size, Worker_Pool_Size, Task_Size, Semaphore_Value
from ._retry_sample import (
    _Retry_Time, _Default_Retry_Time, _Test_Return_Value, _Test_Exception,
    init_flag, get_process_flag, get_running_function_flag,
    target_function_with_default, target_function_raising_exception_with_default,
    target_function, target_function_raising_exception,
    async_target_function_with_default, async_target_function_raising_exception_with_default,
    async_target_function, async_target_function_raising_exception,
    TargetBoundedFunction, TargetBoundedAsyncFunction
)

from gevent.threading import get_ident as get_gevent_ident
from gevent import sleep as gevent_sleep
import threading
import asyncio
import pytest
import time
import os


_Worker_Size = Worker_Size
_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size

_Semaphore_Value = Semaphore_Value

_Sleep_Time: int = 1
_Random_Start_Time: int = 60
_Random_End_Time: int = 80

_Default_Value: int = 1


def instantiate_lock(_mode, **kwargs):
    _lock = LockFactory()
    return _initial(_lock, _mode, **kwargs)


def instantiate_rlock(_mode, **kwargs):
    _rlock = RLockFactory()
    return _initial(_rlock, _mode, **kwargs)


def instantiate_semaphore(_mode, **kwargs):
    _semaphore = SemaphoreFactory(value=_Semaphore_Value)
    return _initial(_semaphore, _mode, **kwargs)


def instantiate_bounded_semaphore(_mode, **kwargs):
    _bounded_semaphore = BoundedSemaphoreFactory(value=_Semaphore_Value)
    return _initial(_bounded_semaphore, _mode, **kwargs)


def instantiate_event(_mode, **kwargs):
    _event = EventFactory()
    return _initial(_event, _mode, **kwargs)


def instantiate_condition(_mode, **kwargs):
    _condition = ConditionFactory()
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


@pytest.fixture(scope="class")
def target_bounded_function() -> TargetBoundedFunction:
    return TargetBoundedFunction()


@pytest.fixture(scope="class")
def target_bounded_async_function() -> TargetBoundedAsyncFunction:
    return TargetBoundedAsyncFunction()


@pytest.fixture(scope="class")
def async_strategy() -> AsynchronousStrategy:
    return AsynchronousStrategy(executors=_Worker_Size)


class TestRetryMechanism:

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
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

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
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

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
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

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
        run_async(_function=_target_testing, _feature=LockFactory())
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
        run_async(_function=_target_testing, _feature=SemaphoreFactory(value=_Semaphore_Value))
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
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=BoundedSemaphoreFactory(value=_Semaphore_Value))
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

