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
import pytest
import time
import re


_Worker_Size = Worker_Size
_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size

_Semaphore_Value = Semaphore_Value

_Sleep_Time: int = 1


@pytest.fixture(scope="function")
def lock():
    _lock = Lock()
    return _initial(_lock)


@pytest.fixture(scope="function")
def rlock():
    _rlock = RLock()
    return _initial(_rlock)


@pytest.fixture(scope="function")
def semaphore():
    _semaphore = Semaphore(value=_Semaphore_Value)
    return _initial(_semaphore)


@pytest.fixture(scope="function")
def bounded_semaphore():
    _bounded_semaphore = BoundedSemaphore(value=_Semaphore_Value)
    return _initial(_bounded_semaphore)


@pytest.fixture(scope="function")
def event():
    _event = Event()
    return _initial(_event)


@pytest.fixture(scope="function")
def condition():
    _condition = Condition()
    return _initial(_condition)


def _initial(_feature_factory):
    _feature_factory.feature_mode = FeatureMode.Parallel
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



class TestOperator:
    pass



class TestLockAdapterOperator(TestOperator):

    def test_get_feature_instance(self, lock: Lock, lock_opts: LockAdapterOperator):
        _feature_instn = lock_opts._get_feature_instance()
        assert _feature_instn is lock, f"The feature property should be the 'Lock' instance we set."


    def test_feature_instance_property(self, lock: Lock, lock_opts: LockAdapterOperator):
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

        try:
            _feature_instn = lock_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is lock, f"The feature property should be the 'Lock' instance we set."


    @pytest.mark.skip(reason="Not finish this testing implementation yet.")
    def test_feature_in_parallel(self, lock: Lock, lock_opts: LockAdapterOperator):

        def _target_testing():
            # Save a timestamp into list
            lock_opts.acquire()
            pass
            lock_opts.release()
            assert False, f""

        # # # # Run multiple workers and save something info at the right time
        run_multi_process(_function=_target_testing)


    def test_feature_in_concurrent(self, lock: Lock, lock_opts: LockAdapterOperator):

        import threading

        _done_timestamp = {}

        def _target_testing():
            # Save a timestamp into list
            lock_opts.acquire()
            _thread_id = threading.get_ident()
            time.sleep(_Sleep_Time)
            _time = int(time.time())
            _done_timestamp[_thread_id] = _time
            lock_opts.release()

        # # # # Run multiple workers and save something info at the right time
        run_multi_threads(_function=_target_testing)
        TestLockAdapterOperator._chk_done_timestamp(_done_timestamp)


    def test_feature_by_pykeyword_with_in_concurrent(self, lock: Lock, lock_opts: LockAdapterOperator):

        import threading

        _done_timestamp = {}

        def _target_testing():
            # Save a time stamp into list
            try:
                with lock_opts:
                    _thread_id = threading.get_ident()
                    time.sleep(_Sleep_Time)
                    _time = int(time.time())
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
                assert int(abs(int(_v) - int(_previous_v))) == _Sleep_Time, \
                    f"The different time betweeen them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_done_timestamp}"
                _previous_v = _v



class TestRLockAdapterOperator(TestOperator):

    def test_get_feature_instance(self, rlock: RLock, rlock_opts: RLockOperator):
        _feature_instn = rlock_opts._get_feature_instance()
        assert _feature_instn is lock, f"The feature property should be the 'RLock' instance we set."


    def test_feature_instance_property(self, rlock: RLock, rlock_opts: RLockOperator):
        try:
            _feature_instn = rlock_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is rlock, f"The feature property should be the 'RLock' instance we set."



class TestSemaphoreAdapterOperator(TestOperator):

    def test_get_feature_instance(self, semaphore: Semaphore, semaphore_opts: SemaphoreOperator):
        _feature_instn = semaphore_opts._get_feature_instance()
        assert _feature_instn is semaphore, f"The feature property should be the 'Semaphore' instance we set."


    def test_feature_instance_property(self, semaphore: Semaphore, semaphore_opts: SemaphoreOperator):
        try:
            _feature_instn = semaphore_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is semaphore, f"The feature property should be the 'Semaphore' instance we set."



class TestBoundedSemaphoreAdapterOperator(TestOperator):

    def test_get_feature_instance(self, bounded_semaphore: BoundedSemaphore, bounded_semaphore_opts: BoundedSemaphoreOperator):
        _feature_instn = bounded_semaphore_opts._get_feature_instance()
        assert _feature_instn is bounded_semaphore, f"The feature property should be the 'BoundedSemaphore' instance we set."


    def test_feature_instance_property(self, bounded_semaphore: BoundedSemaphore, bounded_semaphore_opts: BoundedSemaphoreOperator):
        try:
            _feature_instn = bounded_semaphore_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is bounded_semaphore, f"The feature property should be the 'BoundedSemaphore' instance we set."



class TestEventAdapterOperator(TestOperator):

    def test_get_feature_instance(self, event: Event, event_opts: EventOperator):
        _feature_instn = event_opts._get_feature_instance()
        assert _feature_instn is event, f"The feature property should be the 'Event' instance we set."


    def test_feature_instance_property(self, event: Event, event_opts: EventOperator):
        try:
            _feature_instn = event_opts._event_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is event, f"The feature property should be the 'Event' instance we set."



class TestConditionAdapterOperator(TestOperator):

    def test_get_feature_instance(self, condition: Condition, condition_opts: ConditionOperator):
        _feature_instn = condition_opts._get_feature_instance()
        assert _feature_instn is condition, f"The feature property should be the 'Condition' instance we set."


    def test_feature_instance_property(self, condition: Condition, condition_opts: ConditionOperator):
        try:
            _feature_instn = condition_opts._feature_instance
        except ValueError as ve:
            assert False, f"It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is condition, f"The feature property should be the 'Condition' instance we set."


