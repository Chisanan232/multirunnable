from multirunnable.mode import FeatureMode
from multirunnable.factory.lock import LockFactory, RLockFactory, SemaphoreFactory, BoundedSemaphoreFactory
from multirunnable.factory.communication import EventFactory, ConditionFactory
from multirunnable.api.operator import (
    LockAdapterOperator, RLockOperator,
    SemaphoreOperator, BoundedSemaphoreOperator,
    EventOperator, ConditionOperator,
    LockAsyncOperator,
    SemaphoreAsyncOperator, BoundedSemaphoreAsyncOperator,
    EventAsyncOperator, ConditionAsyncOperator)

from ..test_config import Semaphore_Value
from .._examples import RunByStrategy, MapByStrategy
from ..framework.lock import LockTestSpec, RLockTestSpec, SemaphoreTestSpec, BoundedSemaphoreTestSpec, EventTestSpec, ConditionTestSpec

import asyncio
import pytest
import sys


_Semaphore_Value = Semaphore_Value

_Sleep_Time: int = 1


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
    """
    Description:
        Instantiate a new instance via Factory and annotate it as a global object.
    :param _feature_factory:
    :param _mode:
    :param kwargs:
    :return:
    """
    _feature_factory.feature_mode = _mode
    _feature_instn = _feature_factory.get_instance(**kwargs)
    _feature_factory.globalize_instance(_feature_instn)
    return _feature_instn


@pytest.fixture(scope="function")
def lock_opts():
    return LockAdapterOperator()


@pytest.fixture(scope="function")
def rlock_opts():
    return RLockOperator()


@pytest.fixture(scope="function")
def semaphore_opts():
    return SemaphoreOperator()


@pytest.fixture(scope="function")
def bounded_semaphore_opts():
    return BoundedSemaphoreOperator()


@pytest.fixture(scope="function")
def event_opts():
    return EventOperator()


@pytest.fixture(scope="function")
def condition_opts():
    return ConditionOperator()



class TestLockAdapterOperator(LockTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode, lock_opts: LockAdapterOperator):
        _lock = instantiate_lock(mode)
        _feature_instn = lock_opts._get_feature_instance()
        assert _feature_instn is _lock, "The feature property should be the 'Lock' instance we set."


    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_feature_instance_property(self, mode, lock_opts: LockAdapterOperator):
        _lock = instantiate_lock(mode)

        try:
            _feature_instn = lock_opts._feature_instance
        except ValueError as ve:
            assert False, "It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _lock, "The feature property should be the 'Lock' instance we set."


    def test_feature_in_parallel(self, lock_opts: LockAdapterOperator):
        instantiate_lock(FeatureMode.Parallel)
        LockTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=lock_opts, running_function=RunByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self, lock_opts: LockAdapterOperator):
        instantiate_lock(FeatureMode.Parallel)
        LockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=lock_opts, running_function=RunByStrategy.Parallel)


    def test_feature_in_concurrent(self, lock_opts: LockAdapterOperator):
        instantiate_lock(FeatureMode.Concurrent)
        LockTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=lock_opts, running_function=RunByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self, lock_opts: LockAdapterOperator):
        instantiate_lock(FeatureMode.Concurrent)
        LockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Concurrent, _lock=lock_opts, running_function=RunByStrategy.Concurrent)


    def test_feature_in_green_thread(self, lock_opts: LockAdapterOperator):
        instantiate_lock(FeatureMode.GreenThread)
        LockTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=lock_opts, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_by_pykeyword_with_in_green_thread(self, lock_opts: LockAdapterOperator):
        instantiate_lock(FeatureMode.GreenThread)
        LockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.GreenThread, _lock=lock_opts, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_in_asynchronous_tasks(self):
        lock_opts = LockAsyncOperator()
        LockTestSpec._async_feature_testing(mode=FeatureMode.Asynchronous, _lock=lock_opts, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=LockFactory())


    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self):
        lock_opts = LockAsyncOperator()
        LockTestSpec._async_feature_testing_by_pykeyword_with(mode=FeatureMode.Asynchronous, _lock=lock_opts, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=LockFactory())



class TestRLockAdapterOperator(RLockTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode, rlock_opts: RLockOperator):
        _rlock = instantiate_rlock(mode)
        _feature_instn = rlock_opts._get_feature_instance()
        assert _feature_instn is _rlock, "The feature property should be the 'RLock' instance we set."


    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_feature_instance_property(self, mode, rlock_opts: RLockOperator):
        _rlock = instantiate_rlock(mode)
        try:
            _feature_instn = rlock_opts._feature_instance
        except ValueError as ve:
            assert False, "It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _rlock, "The feature property should be the 'RLock' instance we set."


    def test_feature_in_parallel(self, rlock_opts: RLockOperator):
        instantiate_rlock(FeatureMode.Parallel)
        RLockTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=rlock_opts, running_function=RunByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self, rlock_opts: RLockOperator):
        instantiate_rlock(FeatureMode.Parallel)
        RLockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=rlock_opts, running_function=RunByStrategy.Parallel)


    def test_feature_in_concurrent(self, rlock_opts: RLockOperator):
        instantiate_rlock(FeatureMode.Concurrent)
        RLockTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=rlock_opts, running_function=RunByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self, rlock_opts: RLockOperator):
        instantiate_rlock(FeatureMode.Concurrent)
        RLockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Concurrent, _lock=rlock_opts, running_function=RunByStrategy.Concurrent)


    def test_feature_in_green_thread(self, rlock_opts: RLockOperator):
        instantiate_rlock(FeatureMode.GreenThread)
        RLockTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=rlock_opts, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_by_pykeyword_with_in_green_thread(self, rlock_opts: RLockOperator):
        instantiate_rlock(FeatureMode.GreenThread)
        RLockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.GreenThread, _lock=rlock_opts, running_function=RunByStrategy.CoroutineWithGreenThread)



class TestSemaphoreAdapterOperator(SemaphoreTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode, semaphore_opts: SemaphoreOperator):
        _semaphore = instantiate_semaphore(mode)
        _feature_instn = semaphore_opts._get_feature_instance()
        assert _feature_instn is _semaphore, "The feature property should be the 'Semaphore' instance we set."


    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_feature_instance_property(self, mode, semaphore_opts: SemaphoreOperator):
        _semaphore = instantiate_semaphore(mode)
        try:
            _feature_instn = semaphore_opts._feature_instance
        except ValueError as ve:
            assert False, "It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _semaphore, "The feature property should be the 'Semaphore' instance we set."


    @pytest.mark.skipif(sys.platform != "win32", reason="On macOS, sem_timedwait is unsupported. Please refer to the multiprocessing documentation.")
    def test_feature_in_parallel(self, semaphore_opts: SemaphoreOperator):
        instantiate_semaphore(FeatureMode.Parallel)
        SemaphoreTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=semaphore_opts, running_function=RunByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self, semaphore_opts: SemaphoreOperator):
        instantiate_semaphore(FeatureMode.Parallel)
        SemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=semaphore_opts, running_function=RunByStrategy.Parallel)


    @pytest.mark.skip(reason="Still debug for this issue. Mark as XFail because it works finely via Python keyword 'with'.")
    def test_feature_in_concurrent(self, semaphore_opts: SemaphoreOperator):
        instantiate_semaphore(FeatureMode.Concurrent)
        SemaphoreTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=semaphore_opts, running_function=RunByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self, semaphore_opts: SemaphoreOperator):
        instantiate_semaphore(FeatureMode.Concurrent)
        SemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Concurrent, _lock=semaphore_opts, running_function=RunByStrategy.Concurrent)


    @pytest.mark.xfail(reason="Still debug for this issue. Mark as XFail because it works finely via Python keyword 'with'.")
    def test_feature_in_green_thread(self, semaphore_opts: SemaphoreOperator):

        # _done_timestamp = {}
        instantiate_semaphore(FeatureMode.GreenThread)

        # def _target_testing():
        #     _smp_opts = SemaphoreOperator()
        #     # Save a timestamp into list
        #     _smp_opts.acquire()
        #     _thread_id = get_gevent_ident()
        #     gevent_sleep(_Sleep_Time)
        #     _time = float(time.time())
        #     _done_timestamp[_thread_id] = _time
        #     _smp_opts.release()
        #
        # # # # # Run multiple workers and save something info at the right time
        # run_multi_green_thread(_function=_target_testing)
        # TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)

        SemaphoreTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=semaphore_opts, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_by_pykeyword_with_in_green_thread(self, semaphore_opts: SemaphoreOperator):
        instantiate_semaphore(FeatureMode.GreenThread)
        SemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.GreenThread, _lock=semaphore_opts, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_in_asynchronous_tasks(self):
        semaphore_opts = SemaphoreAsyncOperator()
        SemaphoreTestSpec._async_feature_testing(factory=SemaphoreFactory(value=_Semaphore_Value), _lock=semaphore_opts, running_function=RunByStrategy.CoroutineWithAsynchronous)


    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self):
        semaphore_opts = SemaphoreAsyncOperator()
        SemaphoreTestSpec._async_feature_testing_by_pykeyword_with(factory=SemaphoreFactory(value=_Semaphore_Value), _lock=semaphore_opts, running_function=RunByStrategy.CoroutineWithAsynchronous)



class TestBoundedSemaphoreAdapterOperator(BoundedSemaphoreTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode, bounded_semaphore_opts: BoundedSemaphoreOperator):
        _bounded_semaphore = instantiate_bounded_semaphore(mode)
        _feature_instn = bounded_semaphore_opts._get_feature_instance()
        assert _feature_instn is _bounded_semaphore, "The feature property should be the 'BoundedSemaphore' instance we set."


    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_feature_instance_property(self, mode, bounded_semaphore_opts: BoundedSemaphoreOperator):
        _bounded_semaphore = instantiate_bounded_semaphore(mode)
        try:
            _feature_instn = bounded_semaphore_opts._feature_instance
        except ValueError as ve:
            assert False, "It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _bounded_semaphore, "The feature property should be the 'BoundedSemaphore' instance we set."


    @pytest.mark.skipif(sys.platform != "win32", reason="On macOS, sem_timedwait is unsupported. Please refer to the multiprocessing documentation.")
    def test_feature_in_parallel(self, bounded_semaphore_opts: BoundedSemaphoreOperator):

        # _done_timestamp = _Process_Manager.dict()
        instantiate_bounded_semaphore(FeatureMode.Parallel)

        # def _target_testing():
        #     # Save a timestamp into list
        #     bounded_semaphore_opts.acquire()
        #     _pid = multiprocessing.current_process().pid
        #     time.sleep(_Sleep_Time)
        #     _time = float(time.time())
        #     _done_timestamp[_pid] = _time
        #     bounded_semaphore_opts.release()
        #
        # # # # # Run multiple workers and save something info at the right time
        # run_multi_process(_function=_target_testing)
        # TestSemaphoreAdapterOperator._chk_done_timestamp(_done_timestamp)

        BoundedSemaphoreTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=bounded_semaphore_opts, running_function=RunByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self, bounded_semaphore_opts: BoundedSemaphoreOperator):
        instantiate_bounded_semaphore(FeatureMode.Parallel)
        BoundedSemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=bounded_semaphore_opts, running_function=RunByStrategy.Parallel)


    def test_feature_in_concurrent(self, bounded_semaphore_opts: BoundedSemaphoreOperator):
        instantiate_bounded_semaphore(FeatureMode.Concurrent)
        BoundedSemaphoreTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=bounded_semaphore_opts, running_function=RunByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self, bounded_semaphore_opts: BoundedSemaphoreOperator):
        instantiate_bounded_semaphore(FeatureMode.Concurrent)
        BoundedSemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Concurrent, _lock=bounded_semaphore_opts, running_function=RunByStrategy.Concurrent)


    def test_feature_in_green_thread(self, bounded_semaphore_opts: BoundedSemaphoreOperator):
        instantiate_bounded_semaphore(FeatureMode.GreenThread)
        BoundedSemaphoreTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=bounded_semaphore_opts, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_by_pykeyword_with_in_green_thread(self, bounded_semaphore_opts: BoundedSemaphoreOperator):
        instantiate_bounded_semaphore(FeatureMode.GreenThread)
        BoundedSemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.GreenThread, _lock=bounded_semaphore_opts, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_in_asynchronous_tasks(self):
        bounded_semaphore_opts = BoundedSemaphoreAsyncOperator()
        BoundedSemaphoreTestSpec._async_feature_testing(_lock=bounded_semaphore_opts, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=BoundedSemaphoreFactory(value=_Semaphore_Value))


    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self):
        bounded_semaphore_opts = BoundedSemaphoreAsyncOperator()
        BoundedSemaphoreTestSpec._async_feature_testing_by_pykeyword_with(_lock=bounded_semaphore_opts, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=BoundedSemaphoreFactory(value=_Semaphore_Value))



class TestEventAdapterOperator(EventTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode, event_opts: EventOperator):
        _event = instantiate_event(mode)
        _feature_instn = event_opts._get_feature_instance()
        assert _feature_instn is _event, "The feature property should be the 'Event' instance we set."


    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_feature_instance_property(self, mode, event_opts: EventOperator):
        _event = instantiate_event(mode)
        try:
            _feature_instn = event_opts._event_instance
        except ValueError as ve:
            assert False, "It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _event, "The feature property should be the 'Event' instance we set."


    def test_feature_in_parallel(self, event_opts: EventOperator):
        instantiate_event(FeatureMode.Parallel)
        EventTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=event_opts, running_function=MapByStrategy.Parallel)


    def test_feature_in_concurrent(self, event_opts: EventOperator):
        instantiate_event(FeatureMode.Concurrent)
        EventTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=event_opts, running_function=MapByStrategy.Concurrent)


    def test_feature_in_green_thread(self, event_opts: EventOperator):
        instantiate_event(FeatureMode.GreenThread)
        EventTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=event_opts, running_function=MapByStrategy.CoroutineWithGreenThread)


    def test_feature_in_asynchronous_tasks(self):
        _event_opt = EventAsyncOperator()
        EventTestSpec._async_feature_testing(_lock=_event_opt, running_function=MapByStrategy.CoroutineWithAsynchronous, factory=EventFactory())



class TestConditionAdapterOperator(ConditionTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent])
    def test_get_feature_instance(self, mode, condition_opts: ConditionOperator):
        _condition = instantiate_condition(mode)
        _feature_instn = condition_opts._get_feature_instance()
        assert _feature_instn is _condition, "The feature property should be the 'Condition' instance we set."


    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent])
    def test_feature_instance_property(self, mode, condition_opts: ConditionOperator):
        _condition = instantiate_condition(mode)
        try:
            _feature_instn = condition_opts._feature_instance
        except ValueError as ve:
            assert False, "It must to raise a ValueError exception when we try to get feature instance without FeatureMode."
        else:
            assert _feature_instn is _condition, "The feature property should be the 'Condition' instance we set."


    def test_feature_in_parallel(self, condition_opts: ConditionOperator):
        instantiate_condition(FeatureMode.Parallel)
        ConditionTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=condition_opts, running_function=MapByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self, condition_opts: ConditionOperator):
        instantiate_condition(FeatureMode.Parallel)
        ConditionTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=condition_opts, running_function=MapByStrategy.Parallel)


    def test_feature_in_concurrent(self, condition_opts: ConditionOperator):
        instantiate_condition(FeatureMode.Concurrent)
        ConditionTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=condition_opts, running_function=MapByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self, condition_opts: ConditionOperator):
        instantiate_condition(FeatureMode.Concurrent)
        ConditionTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Concurrent, _lock=condition_opts, running_function=MapByStrategy.Concurrent)


    def test_feature_in_asynchronous_tasks(self):
        _condition_opt = ConditionAsyncOperator()
        ConditionTestSpec._async_feature_testing(_lock=_condition_opt, running_function=MapByStrategy.CoroutineWithAsynchronous, factory=ConditionFactory())


    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self):
        _condition_opt = ConditionAsyncOperator()
        ConditionTestSpec._async_feature_testing_by_pykeyword_with(_lock=_condition_opt, running_function=MapByStrategy.CoroutineWithAsynchronous, factory=ConditionFactory())


