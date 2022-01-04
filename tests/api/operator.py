from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from multirunnable.mode import RunningMode, FeatureMode
from multirunnable.adapter.lock import Lock, RLock, Semaphore, BoundedSemaphore
from multirunnable.adapter.communication import Event, Condition
from multirunnable.adapter.strategy import ExecutorStrategyAdapter, PoolStrategyAdapter
from multirunnable.api.operator import (
    LockAdapterOperator, RLockOperator,
    SemaphoreOperator, BoundedSemaphoreOperator,
    EventOperator, ConditionOperator,
    LockAsyncOperator,
    SemaphoreAsyncOperator, BoundedSemaphoreAsyncOperator,
    EventAsyncOperator, ConditionAsyncOperator)

from ..test_config import Worker_Size, Worker_Pool_Size, Task_Size, Semaphore_Value

from typing import List
from gevent.threading import get_ident as get_gevent_ident
from gevent import sleep as gevent_sleep
import threading
import asyncio
import pytest
import random
import time
import os
import re


_Worker_Size = Worker_Size
_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size

_Semaphore_Value = Semaphore_Value

_Sleep_Time: int = 1
_Random_Start_Time: int = 60
_Random_End_Time: int = 80


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


@pytest.fixture(scope="class")
def lock_opts():
    return LockAdapterOperator()


@pytest.fixture(scope="class")
def rlock_opts():
    return RLockOperator()


@pytest.fixture(scope="class")
def semaphore_opts():
    return SemaphoreOperator()


@pytest.fixture(scope="class")
def bounded_semaphore_opts():
    return BoundedSemaphoreOperator()


@pytest.fixture(scope="class")
def event_opts():
    return EventOperator()


@pytest.fixture(scope="class")
def condition_opts():
    return ConditionOperator()


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

    import asyncio

    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    async def __process():
        await _strategy.initialization(queue_tasks=None, features=_feature)
        _ps = [_strategy.generate_worker(_function) for _ in range(Worker_Size)]
        await _strategy.activate_workers(_ps)

    if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
        asyncio.run(__process())
    else:
        _event_loop = asyncio.get_event_loop()
        _event_loop.run_until_complete(__process())


def _run_with_multiple_workers(_strategy, _function):
    _ps = [_strategy.generate_worker(_function) for _ in range(Worker_Size)]
    _strategy.activate_workers(_ps)
    _strategy.close(_ps)


def map_multi_process(_functions: List):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Parallel, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _map_with_multiple_workers(_strategy, _functions)


def map_multi_threads(_functions: List):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Concurrent, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _map_with_multiple_workers(_strategy, _functions)


def map_multi_green_thread(_functions: List):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.GreenThread, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _map_with_multiple_workers(_strategy, _functions)


def map_async(_functions: List, _feature):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()
    _strategy.map_with_function(functions=_functions, features=_feature)


def _map_with_multiple_workers(_strategy, _functions: List):
    _ps = [_strategy.generate_worker(_f) for _f in _functions]
    _strategy.activate_workers(_ps)
    _strategy.close(_ps)



class TestOperator:
    pass



class TestLockAdapterOperator(TestOperator):

    def test_get_feature_instance_with_parallel(self, lock_opts: LockAdapterOperator):
        _lock = instantiate_lock(FeatureMode.Parallel)
        _feature_instn = lock_opts._get_feature_instance()
        assert _feature_instn is _lock, f"The feature property should be the 'Lock' instance we set."


    def test_feature_instance_property_with_parallel(self, lock_opts: LockAdapterOperator):
        # try:
        #     _feature_instn = lock_opts._feature_instance
        # except ValueError as ve:
        #     _chksum = re.search(r"The \w{1,32} object not be initialed yet", str(ve))
        #     assert _chksum is not None, f""
        # else:
        #     assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        #
        # _lock_adapter = Lock()
        # _lock = _initial(_lock_adapter)
        _lock = instantiate_lock(FeatureMode.Parallel)

        try:
            _feature_instn = lock_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _lock, f"The feature property should be the 'Lock' instance we set."


    @pytest.mark.skip(reason="Not finish this testing implementation yet.")
    def test_feature_in_parallel(self, lock_opts: LockAdapterOperator):

        def _target_testing():
            # Save a timestamp into list
            lock_opts.acquire()
            pass
            lock_opts.release()
            assert False, f""

        # # # # Run multiple workers and save something info at the right time
        run_multi_process(_function=_target_testing)


    def test_feature_in_concurrent(self, lock_opts: LockAdapterOperator):

        _done_timestamp = {}
        instantiate_lock(FeatureMode.Concurrent)

        def _target_testing():
            # Save a timestamp into list
            lock_opts.acquire()
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time
            lock_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_concurrent(self, lock_opts: LockAdapterOperator):

        _done_timestamp = {}
        instantiate_lock(FeatureMode.Concurrent)

        def _target_testing():
            # Save a time stamp into list
            try:
                with lock_opts:
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
        TestLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_in_green_thread(self):

        _done_timestamp = {}
        instantiate_lock(FeatureMode.GreenThread)

        def _target_testing():
            _lock_opts = LockAdapterOperator()
            # Save a timestamp into list
            _lock_opts.acquire()
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time
            _lock_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_multi_green_thread(_function=_target_testing)
        TestLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_green_thread(self):

        _done_timestamp = {}
        instantiate_lock(FeatureMode.GreenThread)

        def _target_testing():
            # Save a time stamp into list
            _lock_opts = LockAdapterOperator()
            try:
                with _lock_opts:
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
        TestLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_in_asynchronous_tasks(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}

        instantiate_lock(FeatureMode.Asynchronous, event_loop=_event_loop)

        async def _target_testing():
            _lock_async_opts = LockAsyncOperator()
            # Save a timestamp into list
            await _lock_async_opts.acquire()
            await asyncio.sleep(_Sleep_Time)
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
            else:
                _async_task = asyncio.Task.current_task()
            _async_task_id = id(_async_task)
            _time = float(time.time())
            _done_timestamp[_async_task_id] = _time
            _lock_async_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=Lock())
        TestLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_asynchronous_task(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}

        async def _target_testing():
            # Save a time stamp into list
            _lock_async_opts = LockAsyncOperator()
            try:
                async with _lock_async_opts:
                    await asyncio.sleep(_Sleep_Time)
                    if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                        _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
                    else:
                        _async_task = asyncio.Task.current_task()
                    _async_task_id = id(_async_task)
                    _time = float(time.time())
                    _done_timestamp[_async_task_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. \n" \
                              f"Exception: {e}"
            else:
                assert True, f"Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=Lock())
        TestLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp(_done_timestamp: dict):
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



class TestRLockAdapterOperator(TestOperator):

    def test_get_feature_instance_with_parallel(self, rlock_opts: RLockOperator):
        _rlock = instantiate_rlock(FeatureMode.Parallel)
        _feature_instn = rlock_opts._get_feature_instance()
        assert _feature_instn is _rlock, f"The feature property should be the 'RLock' instance we set."


    def test_feature_instance_property_with_parallel(self, rlock_opts: RLockOperator):
        _rlock = instantiate_rlock(FeatureMode.Parallel)
        try:
            _feature_instn = rlock_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _rlock, f"The feature property should be the 'RLock' instance we set."


    def test_feature_in_concurrent(self, rlock_opts: RLockOperator):

        _done_timestamp = {}
        instantiate_rlock(FeatureMode.Concurrent)

        def _target_testing():
            # Save a timestamp into list
            rlock_opts.acquire()
            rlock_opts.acquire()
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time
            rlock_opts.release()
            rlock_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestRLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_concurrent(self, rlock_opts: RLockOperator):

        _done_timestamp = {}
        instantiate_rlock(FeatureMode.Concurrent)

        def _target_testing():
            # Save a time stamp into list
            try:
                with rlock_opts:
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
        TestRLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_in_green_thread(self):

        _done_timestamp = {}
        instantiate_rlock(FeatureMode.GreenThread)

        def _target_testing():
            _rlock_opts = RLockOperator()
            # Save a timestamp into list
            _rlock_opts.acquire()
            _rlock_opts.acquire()
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time
            _rlock_opts.release()
            _rlock_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_multi_green_thread(_function=_target_testing)
        TestRLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    @pytest.mark.skip(reason="The feature doesn't support with current version.")
    def test_feature_by_pykeyword_with_in_green_thread(self):

        _done_timestamp = {}
        instantiate_rlock(FeatureMode.GreenThread)

        def _target_testing():
            # Save a time stamp into list
            _lock_opts = RLockOperator()
            try:
                with _lock_opts:
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
        TestRLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp(_done_timestamp: dict):
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



class TestSemaphoreAdapterOperator(TestOperator):

    def test_get_feature_instance_with_parallel(self, semaphore_opts: SemaphoreOperator):
        _semaphore = instantiate_semaphore(FeatureMode.Parallel)
        _feature_instn = semaphore_opts._get_feature_instance()
        assert _feature_instn is _semaphore, f"The feature property should be the 'Semaphore' instance we set."


    def test_feature_instance_property_with_parallel(self, semaphore_opts: SemaphoreOperator):
        _semaphore = instantiate_semaphore(FeatureMode.Parallel)
        try:
            _feature_instn = semaphore_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _semaphore, f"The feature property should be the 'Semaphore' instance we set."


    @pytest.mark.skip(reason="Has something issue in testing code.")
    def test_feature_in_concurrent(self, semaphore_opts: SemaphoreOperator):

        import threading

        _done_timestamp = {}
        instantiate_semaphore(FeatureMode.Concurrent)

        def _target_testing():
            # Save a timestamp into list
            # semaphore_opts.acquire(blocking=False)
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time
            # semaphore_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_concurrent(self, semaphore_opts: SemaphoreOperator):

        import threading

        _done_timestamp = {}
        instantiate_semaphore(FeatureMode.Concurrent)

        def _target_testing():
            # Save a time stamp into list
            try:
                with semaphore_opts:
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
        TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    @pytest.mark.skip(reason="Has something issue in testing code.")
    def test_feature_in_green_thread(self):

        _done_timestamp = {}
        instantiate_semaphore(FeatureMode.GreenThread)

        def _target_testing():
            _smp_opts = SemaphoreOperator()
            # Save a timestamp into list
            _smp_opts.acquire()
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time
            _smp_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_multi_green_thread(_function=_target_testing)
        TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_green_thread(self):

        _done_timestamp = {}
        instantiate_semaphore(FeatureMode.GreenThread)

        def _target_testing():
            # Save a time stamp into list
            _smp_opts = SemaphoreOperator()
            try:
                with _smp_opts:
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
        TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_in_asynchronous_tasks(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}

        async def _target_testing():
            _smp_async_opts = SemaphoreAsyncOperator()
            # Save a timestamp into list
            await _smp_async_opts.acquire()
            await asyncio.sleep(_Sleep_Time)
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
            else:
                _async_task = asyncio.Task.current_task()
            _async_task_id = id(_async_task)
            _time = float(time.time())
            _done_timestamp[_async_task_id] = _time
            _smp_async_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=Semaphore(value=_Semaphore_Value))
        TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_asynchronous_task(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}

        async def _target_testing():
            # Save a time stamp into list
            _smp_async_opts = SemaphoreAsyncOperator()
            try:
                async with _smp_async_opts:
                    await asyncio.sleep(_Sleep_Time)
                    if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                        _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
                    else:
                        _async_task = asyncio.Task.current_task()
                    _async_task_id = id(_async_task)
                    _time = float(time.time())
                    _done_timestamp[_async_task_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. \n" \
                              f"Exception: {e}"
            else:
                assert True, f"Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=Semaphore(value=_Semaphore_Value))
        TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp(_done_timestamp: dict):
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



class TestBoundedSemaphoreAdapterOperator(TestOperator):

    def test_get_feature_instance_with_parallel(self, bounded_semaphore_opts: BoundedSemaphoreOperator):
        _bounded_semaphore = instantiate_bounded_semaphore(FeatureMode.Parallel)
        _feature_instn = bounded_semaphore_opts._get_feature_instance()
        assert _feature_instn is _bounded_semaphore, f"The feature property should be the 'BoundedSemaphore' instance we set."


    def test_feature_instance_property_with_parallel(self, bounded_semaphore_opts: BoundedSemaphoreOperator):
        _bounded_semaphore = instantiate_bounded_semaphore(FeatureMode.Parallel)
        try:
            _feature_instn = bounded_semaphore_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _bounded_semaphore, f"The feature property should be the 'BoundedSemaphore' instance we set."


    @pytest.mark.skip(reason="Has something issue in testing code.")
    def test_feature_in_concurrent(self, bounded_semaphore_opts: BoundedSemaphoreOperator):

        import threading

        _done_timestamp = {}
        instantiate_bounded_semaphore(FeatureMode.Concurrent)

        def _target_testing():
            # Save a timestamp into list
            # bounded_semaphore_opts.acquire(blocking=False)
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time
            # bounded_semaphore_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_concurrent(self, bounded_semaphore_opts: BoundedSemaphoreOperator):

        import threading

        _done_timestamp = {}
        instantiate_bounded_semaphore(FeatureMode.Concurrent)

        def _target_testing():
            # Save a time stamp into list
            try:
                with bounded_semaphore_opts:
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
        TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_in_green_thread(self):

        _done_timestamp = {}
        instantiate_bounded_semaphore(FeatureMode.GreenThread)

        def _target_testing():
            _bsmp_opts = BoundedSemaphoreOperator()
            # Save a timestamp into list
            _bsmp_opts.acquire()
            _thread_id = get_gevent_ident()
            gevent_sleep(_Sleep_Time)
            _time = float(time.time())
            _done_timestamp[_thread_id] = _time
            _bsmp_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_multi_green_thread(_function=_target_testing)
        TestBoundedSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_green_thread(self):

        _done_timestamp = {}
        instantiate_bounded_semaphore(FeatureMode.GreenThread)

        def _target_testing():
            # Save a time stamp into list
            _bsmp_opts = BoundedSemaphoreOperator()
            try:
                with _bsmp_opts:
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
        TestBoundedSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_in_asynchronous_tasks(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}

        async def _target_testing():
            _bsmp_async_opts = BoundedSemaphoreAsyncOperator()
            # Save a timestamp into list
            await _bsmp_async_opts.acquire()
            await asyncio.sleep(_Sleep_Time)
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
            else:
                _async_task = asyncio.Task.current_task()
            _async_task_id = id(_async_task)
            _time = float(time.time())
            _done_timestamp[_async_task_id] = _time
            _bsmp_async_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=BoundedSemaphore(value=_Semaphore_Value))
        TestBoundedSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_asynchronous_task(self):
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=_event_loop)

        _done_timestamp = {}

        async def _target_testing():
            # Save a time stamp into list
            _bsmp_async_opts = BoundedSemaphoreAsyncOperator()
            try:
                async with _bsmp_async_opts:
                    await asyncio.sleep(_Sleep_Time)
                    if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                        _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
                    else:
                        _async_task = asyncio.Task.current_task()
                    _async_task_id = id(_async_task)
                    _time = float(time.time())
                    _done_timestamp[_async_task_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. \n" \
                              f"Exception: {e}"
            else:
                assert True, f"Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        run_async(_function=_target_testing, _feature=BoundedSemaphore(value=_Semaphore_Value))
        TestBoundedSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp(_done_timestamp: dict):
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



class TestEventAdapterOperator(TestOperator):

    def test_get_feature_instance_with_parallel(self, event_opts: EventOperator):
        _event = instantiate_event(FeatureMode.Parallel)
        _feature_instn = event_opts._get_feature_instance()
        assert _feature_instn is _event, f"The feature property should be the 'Event' instance we set."


    def test_feature_instance_property_with_parallel(self, event_opts: EventOperator):
        _event = instantiate_event(FeatureMode.Parallel)
        try:
            _feature_instn = event_opts._event_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _event, f"The feature property should be the 'Event' instance we set."


    def test_feature_in_concurrent(self, event_opts: EventOperator):

        _thread_ids = {"producer": "", "consumer": ""}
        _thread_flag = {"producer": [], "consumer": []}
        instantiate_event(FeatureMode.Concurrent)

        def _target_producer():
            for _ in range(3):
                time.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _thread_flag["producer"].append(_thread_index)
                _thread_ids["producer"] = str(threading.get_ident())
                event_opts.set()

        def _target_consumer():
            while True:
                event_opts.wait()
                event_opts.clear()
                _thread_flag["consumer"].append(float(time.time()))
                _thread_ids["consumer"] = str(threading.get_ident())
                if len(_thread_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        map_multi_threads(_functions=[_target_producer, _target_consumer])
        TestEventAdapterOperator._chk_info(_thread_ids, _thread_flag)


    def test_feature_in_green_thread(self):

        _thread_ids = {"producer": "", "consumer": ""}
        _thread_flag = {"producer": [], "consumer": []}
        instantiate_event(FeatureMode.GreenThread)

        def _target_producer():
            _event_opts = EventOperator()
            for _ in range(3):
                gevent_sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _thread_flag["producer"].append(_thread_index)
                _thread_ids["producer"] = str(get_gevent_ident())
                _event_opts.set()

        def _target_consumer():
            _event_opts = EventOperator()
            while True:
                _event_opts.wait()
                _event_opts.clear()
                _thread_flag["consumer"].append(float(time.time()))
                _thread_ids["consumer"] = str(get_gevent_ident())
                if len(_thread_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        map_multi_green_thread(_functions=[_target_producer, _target_consumer])
        TestEventAdapterOperator._chk_info(_thread_ids, _thread_flag)


    def test_feature_in_asynchronous_task(self):

        _async_task_ids = {"producer": "", "consumer": ""}
        _async_task_flag = {"producer": [], "consumer": []}

        async def _target_producer():
            _event_opts = EventAsyncOperator()
            for _ in range(3):
                await asyncio.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _async_task_flag["producer"].append(_thread_index)
                if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                    _async_task_ids["producer"] = str(id(asyncio.current_task()))
                else:
                    _async_task_ids["producer"] = str(id(asyncio.Task.current_task()))
                _event_opts.set()

        async def _target_consumer():
            _event_opts = EventAsyncOperator()
            while True:
                await _event_opts.wait()
                _event_opts.clear()
                _async_task_flag["consumer"].append(float(time.time()))
                _async_task_ids["consumer"] = str(threading.get_ident())
                if len(_async_task_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        map_async(_functions=[_target_producer, _target_consumer], _feature=Event())
        TestEventAdapterOperator._chk_info(_async_task_ids, _async_task_flag)


    @staticmethod
    def _chk_info(_thread_ids: dict, _thread_flag: dict):
        assert len(set(_thread_ids.values())) == 2, f"The amount of thread ID (de-duplicate) should be equal to amount of functions '2'."
        assert len(_thread_flag["producer"]) == 3, f"The amount of producer's flags should be equal to '3'."
        assert len(_thread_flag["consumer"]) == 3, f"The amount of consumer's flags should be equal to '3'."

        for _p_index in _thread_flag["producer"]:
            assert _Random_Start_Time <= _p_index <= _Random_End_Time, f"All index of producer set should be in range '{_Random_Start_Time}' and '{_Random_End_Time}'."

        _int_unix_time_timestamps = [int(_v) for _v in _thread_flag["consumer"]]
        _previous_v = None
        for _v in sorted(_int_unix_time_timestamps):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time between them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_thread_flag['consumer']}"
                _previous_v = _v



class TestConditionAdapterOperator(TestOperator):

    def test_get_feature_instance_with_parallel(self, condition_opts: ConditionOperator):
        _condition = instantiate_condition(FeatureMode.Parallel)
        _feature_instn = condition_opts._get_feature_instance()
        assert _feature_instn is _condition, f"The feature property should be the 'Condition' instance we set."


    def test_feature_instance_property_with_parallel(self, condition_opts: ConditionOperator):
        _condition = instantiate_condition(FeatureMode.Parallel)
        try:
            _feature_instn = condition_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _condition, f"The feature property should be the 'Condition' instance we set."


    def test_feature_in_concurrent(self, condition_opts: ConditionOperator):

        _thread_ids = {"producer": "", "consumer": ""}
        _thread_flag = {"producer": [], "consumer": []}
        instantiate_condition(FeatureMode.Concurrent)

        def _target_producer():
            for _ in range(3):
                time.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _thread_flag["producer"].append(_thread_index)
                _thread_ids["producer"] = str(threading.get_ident())
                condition_opts.acquire()
                condition_opts.notify_all()
                condition_opts.release()

        def _target_consumer():
            while True:
                condition_opts.acquire()
                condition_opts.wait()
                _thread_flag["consumer"].append(float(time.time()))
                _thread_ids["consumer"] = str(threading.get_ident())
                condition_opts.release()
                if len(_thread_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        map_multi_threads(_functions=[_target_producer, _target_consumer])
        TestConditionAdapterOperator._chk_info(_thread_ids, _thread_flag)


    def test_feature_by_pykeyword_with_in_concurrent(self, condition_opts: ConditionOperator):

        _thread_ids = {"producer": "", "consumer": ""}
        _thread_flag = {"producer": [], "consumer": []}
        instantiate_condition(FeatureMode.Concurrent)

        def _target_producer():
            for _ in range(3):
                time.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _thread_flag["producer"].append(_thread_index)
                _thread_ids["producer"] = str(threading.get_ident())
                with condition_opts:
                    condition_opts.notify_all()

        def _target_consumer():
            while True:
                with condition_opts:
                    condition_opts.wait()
                    _thread_flag["consumer"].append(float(time.time()))
                    _thread_ids["consumer"] = str(threading.get_ident())
                    if len(_thread_flag["producer"]) == 3:
                        break

        # # # # Run multiple workers and save something info at the right time
        map_multi_threads(_functions=[_target_producer, _target_consumer])
        TestConditionAdapterOperator._chk_info(_thread_ids, _thread_flag)


    @pytest.mark.skip(reason="With GreenThread strategy, it doesn't support feature 'Condition' in current version.")
    def test_feature_in_green_thread(self):

        _thread_ids = {"producer": "", "consumer": ""}
        _thread_flag = {"producer": [], "consumer": []}
        instantiate_condition(FeatureMode.GreenThread)

        def _target_producer():
            _condition_opts = ConditionOperator()
            for _ in range(3):
                gevent_sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _thread_flag["producer"].append(_thread_index)
                _thread_ids["producer"] = str(get_gevent_ident())
                _condition_opts.acquire()
                _condition_opts.notify_all()
                _condition_opts.release()

        def _target_consumer():
            _condition_opts = ConditionOperator()
            while True:
                _condition_opts.acquire()
                _condition_opts.wait()
                _thread_flag["consumer"].append(float(time.time()))
                _thread_ids["consumer"] = str(get_gevent_ident())
                _condition_opts.release()
                if len(_thread_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        map_multi_green_thread(_functions=[_target_producer, _target_consumer])
        TestConditionAdapterOperator._chk_info(_thread_ids, _thread_flag)


    @pytest.mark.skip(reason="With GreenThread strategy, it doesn't support feature 'Condition' in current version.")
    def test_feature_by_pykeyword_with_in_green_thread(self):

        _thread_ids = {"producer": "", "consumer": ""}
        _thread_flag = {"producer": [], "consumer": []}
        instantiate_condition(FeatureMode.Concurrent)

        def _target_producer():
            _condition_opts = ConditionOperator()
            for _ in range(3):
                time.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _thread_flag["producer"].append(_thread_index)
                _thread_ids["producer"] = str(threading.get_ident())
                with _condition_opts:
                    _condition_opts.notify_all()

        def _target_consumer():
            _condition_opts = ConditionOperator()
            while True:
                with _condition_opts:
                    _condition_opts.wait()
                    _thread_flag["consumer"].append(float(time.time()))
                    _thread_ids["consumer"] = str(threading.get_ident())
                    if len(_thread_flag["producer"]) == 3:
                        break

        # # # # Run multiple workers and save something info at the right time
        map_multi_green_thread(_functions=[_target_producer, _target_consumer])
        TestConditionAdapterOperator._chk_info(_thread_ids, _thread_flag)


    def test_feature_in_asynchronous_task(self):
        _async_task_ids = {"producer": "", "consumer": ""}
        _async_task_flag = {"producer": [], "consumer": []}

        async def _target_producer():
            _condition_opts = ConditionAsyncOperator()
            for _ in range(3):
                await asyncio.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _async_task_flag["producer"].append(_thread_index)
                if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                    _async_task_ids["producer"] = str(id(asyncio.current_task()))
                else:
                    _async_task_ids["producer"] = str(id(asyncio.Task.current_task()))
                await _condition_opts.acquire()
                _condition_opts.notify_all()
                _condition_opts.release()

        async def _target_consumer():
            _condition_opts = ConditionAsyncOperator()
            while True:
                await _condition_opts.acquire()
                await _condition_opts.wait()
                _async_task_flag["consumer"].append(float(time.time()))
                _async_task_ids["consumer"] = str(threading.get_ident())
                _condition_opts.release()
                if len(_async_task_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        map_async(_functions=[_target_producer, _target_consumer], _feature=Condition())
        TestConditionAdapterOperator._chk_info(_async_task_ids, _async_task_flag)


    def test_feature_by_pykeyword_with_in_asynchronous_task(self):
        _async_task_ids = {"producer": "", "consumer": ""}
        _async_task_flag = {"producer": [], "consumer": []}

        async def _target_producer():
            _condition_opts = ConditionAsyncOperator()
            for _ in range(3):
                await asyncio.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _async_task_flag["producer"].append(_thread_index)
                _async_task_ids["producer"] = str(threading.get_ident())
                async with _condition_opts:
                    _condition_opts.notify_all()

        async def _target_consumer():
            _condition_opts = ConditionAsyncOperator()
            while True:
                async with _condition_opts:
                    await _condition_opts.wait()
                    _async_task_flag["consumer"].append(float(time.time()))
                    if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                        _async_task_ids["consumer"] = str(id(asyncio.current_task()))
                    else:
                        _async_task_ids["consumer"] = str(id(asyncio.Task.current_task()))
                    if len(_async_task_flag["producer"]) == 3:
                        break

        # # # # Run multiple workers and save something info at the right time
        map_async(_functions=[_target_producer, _target_consumer], _feature=Condition())
        TestConditionAdapterOperator._chk_info(_async_task_ids, _async_task_flag)


    @staticmethod
    def _chk_info(_thread_ids: dict, _thread_flag: dict):
        assert len(set(_thread_ids.values())) == 2, f"The amount of thread ID (de-duplicate) should be equal to amount of functions '2'."
        assert len(_thread_flag["producer"]) == 3, f"The amount of producer's flags should be equal to '3'."
        assert len(_thread_flag["consumer"]) == 3, f"The amount of consumer's flags should be equal to '3'."

        for _p_index in _thread_flag["producer"]:
            assert _Random_Start_Time <= _p_index <= _Random_End_Time, f"All index of producer set should be in range '{_Random_Start_Time}' and '{_Random_End_Time}'."

        _int_unix_time_timestamps = [int(_v) for _v in _thread_flag["consumer"]]
        _previous_v = None
        for _v in sorted(_int_unix_time_timestamps):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time between them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_thread_flag['consumer']}"
                _previous_v = _v


