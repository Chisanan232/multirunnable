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
import pytest
import random
import time
import re


_Worker_Size = Worker_Size
_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size

_Semaphore_Value = Semaphore_Value

_Sleep_Time: int = 1
_Random_Start_Time: int = 60
_Random_End_Time: int = 80


# @pytest.fixture(scope="function")
def instantiate_lock(_mode):
    _lock = Lock()
    return _initial(_lock, _mode)


# @pytest.fixture(scope="function", params=[RunningMode.Concurrent])
def instantiate_rlock(_mode):
    _rlock = RLock()
    return _initial(_rlock, _mode)


# @pytest.fixture(scope="function")
def instantiate_semaphore(_mode):
    _semaphore = Semaphore(value=_Semaphore_Value)
    return _initial(_semaphore, _mode)


# @pytest.fixture(scope="function")
def instantiate_bounded_semaphore(_mode):
    _bounded_semaphore = BoundedSemaphore(value=_Semaphore_Value)
    return _initial(_bounded_semaphore, _mode)


# @pytest.fixture(scope="function")
def instantiate_event(_mode):
    _event = Event()
    return _initial(_event, _mode)


# @pytest.fixture(scope="function")
def instantiate_condition(_mode):
    _condition = Condition()
    return _initial(_condition, _mode)


def _initial(_feature_factory, _mode):
    _feature_factory.feature_mode = _mode
    _feature_instn = _feature_factory.get_instance()
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


def run_async(_function):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _run_with_multiple_workers(_strategy, _function)


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


def map_async(_functions: List):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _map_with_multiple_workers(_strategy, _functions)


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

        import threading

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

        import threading

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

        import threading

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

        import threading

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

        import threading

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

        import threading

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

        import threading

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


