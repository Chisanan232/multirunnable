from typing import Union
# import asyncio
import pytest
import sys

from multirunnable.adapter.lock import AsyncLock, AsyncSemaphore, AsyncBoundedSemaphore
from multirunnable.adapter import Lock, RLock, Semaphore, BoundedSemaphore
from multirunnable.mode import RunningMode, FeatureMode

from ...test_config import Semaphore_Value
from ..._examples import RunByStrategy
from ..framework.lock import LockTestSpec, RLockTestSpec, SemaphoreTestSpec, BoundedSemaphoreTestSpec


_Semaphore_Value: int = Semaphore_Value

_Sleep_Time: int = 1


def instantiate_lock(_mode: Union[RunningMode, FeatureMode], _init: bool, **kwargs) -> Union[Lock, AsyncLock]:
    if _mode is RunningMode.Asynchronous or _mode is FeatureMode.Asynchronous:
        return AsyncLock(mode=_mode, init=_init, **kwargs)
    else:
        return Lock(mode=_mode, init=_init, **kwargs)


def instantiate_rlock(_mode: Union[RunningMode, FeatureMode], _init: bool, **kwargs) -> RLock:
    return RLock(mode=_mode, init=_init, **kwargs)


def instantiate_semaphore(_mode: Union[RunningMode, FeatureMode], _init: bool, **kwargs) -> Union[Semaphore, AsyncSemaphore]:
    if _mode is RunningMode.Asynchronous or _mode is FeatureMode.Asynchronous:
        return AsyncSemaphore(mode=_mode, init=_init, value=_Semaphore_Value, **kwargs)
    else:
        return Semaphore(mode=_mode, init=_init, value=_Semaphore_Value, **kwargs)


def instantiate_bounded_semaphore(_mode: Union[RunningMode, FeatureMode], _init: bool, **kwargs) -> Union[BoundedSemaphore, AsyncBoundedSemaphore]:
    if _mode is RunningMode.Asynchronous or _mode is FeatureMode.Asynchronous:
        return AsyncBoundedSemaphore(mode=_mode, init=_init, value=_Semaphore_Value, **kwargs)
    else:
        return BoundedSemaphore(mode=_mode, init=_init, value=_Semaphore_Value, **kwargs)



class TestAdapterLock(LockTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode):
        _lock = instantiate_lock(_mode=mode, _init=True)
        self._feature_instance_testing(_lock_inst=_lock)


    def test_feature_in_parallel(self):
        _lock = instantiate_lock(_mode=FeatureMode.Parallel, _init=True)
        LockTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=_lock, running_function=RunByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self):
        _lock = instantiate_lock(_mode=FeatureMode.Parallel, _init=True)
        LockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=_lock, running_function=RunByStrategy.Parallel)


    def test_feature_in_concurrent(self):
        _lock = instantiate_lock(_mode=FeatureMode.Concurrent, _init=True)
        LockTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=_lock, running_function=RunByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self):
        _lock = instantiate_lock(_mode=FeatureMode.Concurrent, _init=True)
        LockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Concurrent, _lock=_lock, running_function=RunByStrategy.Concurrent)


    def test_feature_in_green_thread(self):
        _lock = instantiate_lock(_mode=FeatureMode.GreenThread, _init=True)
        LockTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=_lock, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_by_pykeyword_with_in_green_thread(self):
        _lock = instantiate_lock(_mode=FeatureMode.GreenThread, _init=True)
        LockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.GreenThread, _lock=_lock, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_in_asynchronous_tasks(self):
        # # # # For Python 3.10, it works finely.
        # # # # In Python 3.7, it run incorrectly. It's possible that the asyncio event loop conflict.
        # _event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop=_event_loop)

        # _lock = instantiate_lock(_mode=FeatureMode.Asynchronous, _init=True, event_loop=_event_loop)
        _async_lock = AsyncLock(mode=FeatureMode.Asynchronous)
        LockTestSpec._async_feature_testing(mode=FeatureMode.Asynchronous, _lock=_async_lock, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=_async_lock)


    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self):
        # _event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop=_event_loop)

        # _lock = instantiate_lock(_mode=FeatureMode.Asynchronous, _init=True, event_loop=_event_loop)
        _async_lock = AsyncLock(mode=FeatureMode.Asynchronous)
        LockTestSpec._async_feature_testing_by_pykeyword_with(mode=FeatureMode.Asynchronous, _lock=_async_lock, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=_async_lock)



class TestAdapterRLock(RLockTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode):
        _rlock = instantiate_rlock(_mode=mode, _init=True)
        self._feature_instance_testing(_lock_inst=_rlock)


    def test_feature_in_parallel(self):
        _rlock = instantiate_rlock(_mode=FeatureMode.Parallel, _init=True)
        RLockTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=_rlock, running_function=RunByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self):
        _rlock = instantiate_rlock(_mode=FeatureMode.Parallel, _init=True)
        RLockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=_rlock, running_function=RunByStrategy.Parallel)


    def test_feature_in_concurrent(self):
        _rlock = instantiate_rlock(_mode=FeatureMode.Concurrent, _init=True)
        RLockTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=_rlock, running_function=RunByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self):
        _rlock = instantiate_rlock(_mode=FeatureMode.Concurrent, _init=True)
        RLockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Concurrent, _lock=_rlock, running_function=RunByStrategy.Concurrent)


    def test_feature_in_green_thread(self):
        _rlock = instantiate_rlock(_mode=FeatureMode.GreenThread, _init=True)
        RLockTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=_rlock, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_by_pykeyword_with_in_green_thread(self):
        _rlock = instantiate_rlock(_mode=FeatureMode.GreenThread, _init=True)
        RLockTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.GreenThread, _lock=_rlock, running_function=RunByStrategy.CoroutineWithGreenThread)



class TestAdapterSemaphore(SemaphoreTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode):
        _semaphore = instantiate_semaphore(_mode=mode, _init=True)
        self._feature_instance_testing(_lock_inst=_semaphore)


    @pytest.mark.skipif(sys.platform != "win32", reason="On macOS, sem_timedwait is unsupported. Please refer to the multiprocessing documentation.")
    def test_feature_in_parallel(self):
        _semaphore = instantiate_semaphore(_mode=FeatureMode.Parallel, _init=True)
        SemaphoreTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=_semaphore, running_function=RunByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self):
        _semaphore = instantiate_semaphore(_mode=FeatureMode.Parallel, _init=True)
        SemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=_semaphore, running_function=RunByStrategy.Parallel)


    @pytest.mark.skip(reason="Still debug for this issue. Mark as XFail because it works finely via Python keyword 'with'.")
    def test_feature_in_concurrent(self):
        _semaphore = instantiate_semaphore(_mode=FeatureMode.Concurrent, _init=True)
        SemaphoreTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=_semaphore, running_function=RunByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self):
        _semaphore = instantiate_semaphore(_mode=FeatureMode.Concurrent, _init=True)
        SemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Concurrent, _lock=_semaphore, running_function=RunByStrategy.Concurrent)


    @pytest.mark.xfail(reason="Still debug for this issue. Mark as XFail because it works finely via Python keyword 'with'.")
    def test_feature_in_green_thread(self):

        # _done_timestamp = {}
        _semaphore = instantiate_semaphore(_mode=FeatureMode.GreenThread, _init=True)

        # def _target_testing():
        #     # Save a timestamp into list
        #     _semaphore.acquire()
        #     _thread_id = get_gevent_ident()
        #     gevent_sleep(_Sleep_Time)
        #     _time = float(time.time())
        #     _done_timestamp[_thread_id] = _time
        #     _semaphore.release()
        #
        # # # # # Run multiple workers and save something info at the right time
        # run_multi_green_thread(_function=_target_testing)
        # TestAdapterSemaphore._chk_done_timestamp(_done_timestamp)

        SemaphoreTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=_semaphore, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_by_pykeyword_with_in_green_thread(self):
        _semaphore = instantiate_semaphore(_mode=FeatureMode.GreenThread, _init=True)
        SemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.GreenThread, _lock=_semaphore, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_in_asynchronous_tasks(self):
        # _event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop=_event_loop)
        #
        # _semaphore = instantiate_semaphore(_mode=FeatureMode.Asynchronous, _init=True, event_loop=_event_loop)
        _semaphore = AsyncSemaphore(mode=FeatureMode.Asynchronous, value=_Semaphore_Value)
        SemaphoreTestSpec._async_feature_testing(_lock=_semaphore, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=_semaphore)


    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self):
        # _event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop=_event_loop)
        #
        # _semaphore = instantiate_semaphore(_mode=FeatureMode.Asynchronous, _init=True, event_loop=_event_loop)
        _semaphore = AsyncSemaphore(mode=FeatureMode.Asynchronous, value=_Semaphore_Value)
        SemaphoreTestSpec._async_feature_testing_by_pykeyword_with(_lock=_semaphore, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=_semaphore)



class TestAdapterBoundedSemaphore(BoundedSemaphoreTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode):
        _bounded_semaphore = instantiate_bounded_semaphore(_mode=mode, _init=True)
        self._feature_instance_testing(_lock_inst=_bounded_semaphore)


    @pytest.mark.skipif(sys.platform != "win32", reason="On macOS, sem_timedwait is unsupported. Please refer to the multiprocessing documentation.")
    def test_feature_in_parallel(self):
        _bounded_semaphore = instantiate_bounded_semaphore(_mode=FeatureMode.Parallel, _init=True)
        BoundedSemaphoreTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=_bounded_semaphore, running_function=RunByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self):
        _bounded_semaphore = instantiate_bounded_semaphore(_mode=FeatureMode.Parallel, _init=True)
        BoundedSemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=_bounded_semaphore, running_function=RunByStrategy.Parallel)


    def test_feature_in_concurrent(self):
        _bounded_semaphore = instantiate_bounded_semaphore(_mode=FeatureMode.Concurrent, _init=True)
        BoundedSemaphoreTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=_bounded_semaphore, running_function=RunByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self):
        _bounded_semaphore = instantiate_bounded_semaphore(_mode=FeatureMode.Concurrent, _init=True)
        BoundedSemaphoreTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=_bounded_semaphore, running_function=RunByStrategy.Concurrent)


    def test_feature_in_green_thread(self):
        _bounded_semaphore = instantiate_bounded_semaphore(_mode=FeatureMode.GreenThread, _init=True)
        BoundedSemaphoreTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=_bounded_semaphore, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_by_pykeyword_with_in_green_thread(self):
        _bounded_semaphore = instantiate_bounded_semaphore(_mode=FeatureMode.GreenThread, _init=True)
        BoundedSemaphoreTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.GreenThread, _lock=_bounded_semaphore, running_function=RunByStrategy.CoroutineWithGreenThread)


    def test_feature_in_asynchronous_tasks(self):
        # _event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop=_event_loop)
        #
        # _bounded_semaphore = instantiate_bounded_semaphore(_mode=FeatureMode.Asynchronous, _init=True, event_loop=_event_loop)
        _bounded_semaphore = AsyncBoundedSemaphore(mode=FeatureMode.Asynchronous, value=_Semaphore_Value)
        BoundedSemaphoreTestSpec._async_feature_testing(_lock=_bounded_semaphore, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=_bounded_semaphore)


    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self):
        # _event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop=_event_loop)
        #
        # _bounded_semaphore = instantiate_bounded_semaphore(_mode=FeatureMode.Asynchronous, _init=True, event_loop=_event_loop)
        _bounded_semaphore = AsyncBoundedSemaphore(mode=FeatureMode.Asynchronous, value=_Semaphore_Value)
        BoundedSemaphoreTestSpec._async_feature_testing_by_pykeyword_with(_lock=_bounded_semaphore, running_function=RunByStrategy.CoroutineWithAsynchronous, factory=_bounded_semaphore)

