import traceback
import pytest
import re

from multirunnable.factory.lock import LockFactory, RLockFactory, SemaphoreFactory, BoundedSemaphoreFactory
from multirunnable.mode import FeatureMode

from ...test_config import Semaphore_Value


_Semaphore_Value = Semaphore_Value


@pytest.fixture(scope="function")
def mr_lock() -> LockFactory:
    return LockFactory()


@pytest.fixture(scope="function")
def mr_rlock() -> RLockFactory:
    return RLockFactory()


@pytest.fixture(scope="function")
def mr_semaphore() -> SemaphoreFactory:
    return SemaphoreFactory(value=_Semaphore_Value)


@pytest.fixture(scope="function")
def mr_bounded_semaphore() -> BoundedSemaphoreFactory:
    return BoundedSemaphoreFactory(value=_Semaphore_Value)



class TestLockFactory:

    def test__str__(self, mr_lock: LockFactory):
        _testing_mode = FeatureMode.Parallel
        mr_lock.feature_mode = _testing_mode
        _lock_str = str(mr_lock)
        _chksum = re.search(r"<Lock object with FeatureMode\.[a-zA-Z]{4,32} mode at \w{10,30}>", _lock_str)
        assert _chksum is not None, f"The '__str__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Lock object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_str}*."


    def test__repr__(self, mr_lock: LockFactory):
        _testing_mode = FeatureMode.Parallel
        mr_lock.feature_mode = _testing_mode
        _lock_repr = repr(mr_lock)
        _chksum = re.search(r"<Lock\(\) object with FeatureMode\.[a-zA-Z]{4,32} mode at \w{10,30}>", _lock_repr)
        assert _chksum is not None, f"The '__repr__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Lock() object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_repr}*."


    def test_feature_mode(self, mr_lock: LockFactory):
        _testing_mode = FeatureMode.Parallel

        assert mr_lock.feature_mode is None, "The default value of FeatureMode of Lock instance should be None."
        try:
            mr_lock.feature_mode = _testing_mode
        except Exception:
            assert False, f"It should set the FeatureMode into Lock instance without any issue.\n Error: {traceback.format_exc()}"
        else:
            _feature_mode = mr_lock.feature_mode
            assert _feature_mode is _testing_mode, f"The mode we got from Lock instance should be the same as we set '{_testing_mode}'."


    def test_get_instance_with_parallel_mode(self, mr_lock: LockFactory):
        try:
            _lock = mr_lock.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_lock.feature_mode = FeatureMode.Parallel
        _lock = mr_lock.get_instance()
        from multiprocessing.synchronize import Lock
        assert _lock is not None and isinstance(_lock, Lock) is True, "This type of Lock instance should be 'multiprocessing.synchronize.Lock'."


    def test_get_instance_with_concurrent_mode(self, mr_lock: LockFactory):
        try:
            _lock = mr_lock.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_lock.feature_mode = FeatureMode.Concurrent
        _lock = mr_lock.get_instance()
        from threading import Lock
        assert _lock is not None and isinstance(_lock, type(Lock())) is True, "This type of Lock instance should be 'threading.Lock'."


    def test_get_instance_with_coroutine_mode(self, mr_lock: LockFactory):
        try:
            _lock = mr_lock.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_lock.feature_mode = FeatureMode.GreenThread
        _lock = mr_lock.get_instance()
        from gevent.threading import Lock
        assert _lock is not None and isinstance(_lock, Lock) is True, "This type of Lock instance should be 'gevent.threading.Lock'."


    def test_get_instance_with_asynchronous_mode(self, mr_lock: LockFactory):
        from asyncio.locks import Lock
        from asyncio import new_event_loop

        try:
            _lock = mr_lock.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_lock.feature_mode = FeatureMode.Asynchronous
        _lock = mr_lock.get_instance(event_loop=new_event_loop())
        assert _lock is not None and isinstance(_lock, Lock) is True, "This type of Lock instance should be 'asyncio.locks.Lock'."


    def test_globalize_instance(self, mr_lock: LockFactory):
        from multirunnable.api.manage import Running_Lock
        assert Running_Lock is None, "It should be None before we do anything."

        mr_lock.feature_mode = FeatureMode.Parallel
        _lock = mr_lock.get_instance()
        mr_lock.globalize_instance(_lock)

        from multirunnable.api.manage import Running_Lock
        assert Running_Lock is _lock, "It should be the instance we instantiated."



class TestRLockFactory:

    def test__str__(self, mr_rlock: RLockFactory):
        _testing_mode = FeatureMode.Parallel
        mr_rlock.feature_mode = _testing_mode
        _rlock_str = str(mr_rlock)
        _chksum = re.search(r"<RLock object with FeatureMode\.[a-zA-Z]{4,32} mode at \w{10,30}>", _rlock_str)
        assert _chksum is not None, f"The '__str__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<RLock object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_rlock_str}*."


    def test__repr__(self, mr_rlock: RLockFactory):
        _testing_mode = FeatureMode.Parallel
        mr_rlock.feature_mode = _testing_mode
        _rlock_repr = repr(mr_rlock)
        _chksum = re.search(r"<RLock\(\) object with FeatureMode\.[a-zA-Z]{4,32} mode at \w{10,30}>", _rlock_repr)
        assert _chksum is not None, f"The '__repr__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<RLock() object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_rlock_repr}*."


    def test_feature_mode(self, mr_rlock: RLockFactory):
        _testing_mode = FeatureMode.Concurrent

        assert mr_rlock.feature_mode is None, "The default value of FeatureMode of RLock instance should be None."
        try:
            mr_rlock.feature_mode = _testing_mode
        except Exception:
            assert False, f"It should set the FeatureMode into RLock instance without any issue.\n Error: {traceback.format_exc()}"
        else:
            _feature_mode = mr_rlock.feature_mode
            assert _feature_mode is _testing_mode, f"The mode we got from RLock instance should be the same as we set '{_testing_mode}'."


    def test_get_instance_with_parallel_mode(self, mr_rlock: RLockFactory):
        try:
            _rlock = mr_rlock.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_rlock.feature_mode = FeatureMode.Parallel
        _rlock = mr_rlock.get_instance()
        from multiprocessing.synchronize import RLock
        assert _rlock is not None and isinstance(_rlock, RLock) is True, "This type of RLock instance should be 'multiprocessing.synchronize.RLock'."


    def test_get_instance_with_concurrent_mode(self, mr_rlock: RLockFactory):
        try:
            _rlock = mr_rlock.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_rlock.feature_mode = FeatureMode.Concurrent
        _rlock = mr_rlock.get_instance()
        from threading import RLock
        assert _rlock is not None and isinstance(_rlock, type(RLock())) is True, "This type of RLock instance should be 'threading.RLock'."


    def test_get_instance_with_coroutine_mode(self, mr_rlock: RLockFactory):
        try:
            _rlock = mr_rlock.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_rlock.feature_mode = FeatureMode.GreenThread
        _rlock = mr_rlock.get_instance()
        from gevent.lock import RLock
        assert _rlock is not None and isinstance(_rlock, RLock) is True, "This type of RLock instance should be 'gevent.lock.RLock'."


    def test_get_instance_with_asynchronous_mode(self, mr_rlock: RLockFactory):
        from asyncio.locks import Lock
        from asyncio import new_event_loop

        try:
            _rlock = mr_rlock.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_rlock.feature_mode = FeatureMode.Asynchronous
        _rlock = mr_rlock.get_instance(event_loop=new_event_loop())
        assert _rlock is not None and isinstance(_rlock, Lock) is True, "This type of RLock instance should be 'asyncio.locks.Lock'."


    def test_globalize_instance(self, mr_rlock: RLockFactory):
        from multirunnable.api.manage import Running_RLock
        assert Running_RLock is None, "It should be None before we do anything."

        mr_rlock.feature_mode = FeatureMode.Concurrent
        _rlock = mr_rlock.get_instance()
        mr_rlock.globalize_instance(_rlock)

        from multirunnable.api.manage import Running_RLock
        assert Running_RLock is _rlock, "It should be the instance we instantiated."



class TestSemaphoreFactory:

    def test__str__(self, mr_semaphore: SemaphoreFactory):
        _testing_mode = FeatureMode.Parallel
        mr_semaphore.feature_mode = _testing_mode
        _semaphore_str = str(mr_semaphore)
        _chksum = re.search(r"<Semaphore object with FeatureMode\.[a-zA-Z]{4,32} mode at \w{10,30}>", _semaphore_str)
        assert _chksum is not None, f"The '__str__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Semaphore object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_semaphore_str}*."


    def test__repr__(self, mr_semaphore: SemaphoreFactory):
        _testing_mode = FeatureMode.Parallel
        mr_semaphore.feature_mode = _testing_mode
        _semaphore_repr = repr(mr_semaphore)
        _chksum = re.search(r"<Semaphore\(value=[0-9]{1,4}\) object with FeatureMode\.[a-zA-Z]{4,32} mode at \w{10,30}>", _semaphore_repr)
        assert _chksum is not None, f"The '__repr__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Semaphore(value=<Semaphore mount>) object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_semaphore_repr}*."


    def test_feature_mode(self, mr_semaphore: SemaphoreFactory):
        _testing_mode = FeatureMode.GreenThread

        assert mr_semaphore.feature_mode is None, "The default value of FeatureMode of Semaphore instance should be None."
        try:
            mr_semaphore.feature_mode = _testing_mode
        except Exception:
            assert False, f"It should set the FeatureMode into Semaphore instance without any issue.\n Error: {traceback.format_exc()}"
        else:
            _feature_mode = mr_semaphore.feature_mode
            assert _feature_mode is _testing_mode, f"The mode we got from Semaphore instance should be the same as we set '{_testing_mode}'."


    def test_get_instance_with_parallel_mode(self, mr_semaphore: SemaphoreFactory):
        try:
            _semaphore = mr_semaphore.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_semaphore.feature_mode = FeatureMode.Parallel
        _semaphore = mr_semaphore.get_instance()
        from multiprocessing.synchronize import Semaphore
        assert _semaphore is not None and isinstance(_semaphore, Semaphore) is True, "This type of Semaphore instance should be 'multiprocessing.synchronize.Semaphore'."


    def test_get_instance_with_concurrent_mode(self, mr_semaphore: SemaphoreFactory):
        try:
            _semaphore = mr_semaphore.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_semaphore.feature_mode = FeatureMode.Concurrent
        _semaphore = mr_semaphore.get_instance()
        from threading import Semaphore
        assert _semaphore is not None and isinstance(_semaphore, Semaphore) is True, "This type of Semaphore instance should be 'threading.Lock'."


    def test_get_instance_with_coroutine_mode(self, mr_semaphore: SemaphoreFactory):
        try:
            _semaphore = mr_semaphore.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_semaphore.feature_mode = FeatureMode.GreenThread
        _semaphore = mr_semaphore.get_instance()
        from gevent.lock import Semaphore
        assert _semaphore is not None and isinstance(_semaphore, Semaphore) is True, "This type of Semaphore instance should be 'gevent.lock.Semaphore'."


    def test_get_instance_with_asynchronous_mode(self, mr_semaphore: SemaphoreFactory):
        from asyncio.locks import Semaphore
        from asyncio import new_event_loop

        try:
            _semaphore = mr_semaphore.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_semaphore.feature_mode = FeatureMode.Asynchronous
        _semaphore = mr_semaphore.get_instance(event_loop=new_event_loop())
        assert _semaphore is not None and isinstance(_semaphore, Semaphore) is True, "This type of Semaphore instance should be 'asyncio.locks.Semaphore'."


    def test_globalize_instance(self, mr_semaphore: SemaphoreFactory):
        from multirunnable.api.manage import Running_Semaphore
        assert Running_Semaphore is None, "It should be None before we do anything."

        mr_semaphore.feature_mode = FeatureMode.Parallel
        _semaphore = mr_semaphore.get_instance()
        mr_semaphore.globalize_instance(_semaphore)

        from multirunnable.api.manage import Running_Semaphore
        assert Running_Semaphore is _semaphore, "It should be the instance we instantiated."



class TestBoundedSemaphoreFactory:

    def test__str__(self, mr_bounded_semaphore: BoundedSemaphoreFactory):
        _testing_mode = FeatureMode.Parallel
        mr_bounded_semaphore.feature_mode = _testing_mode
        _bounded_semaphore_str = str(mr_bounded_semaphore)
        _chksum = re.search(r"<Bounded Semaphore object with FeatureMode\.[a-zA-Z]{4,32} mode at \w{10,30}>", _bounded_semaphore_str)
        assert _chksum is not None, f"The '__str__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Bounded Semaphore object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_bounded_semaphore_str}*."


    def test__repr__(self, mr_bounded_semaphore: BoundedSemaphoreFactory):
        _testing_mode = FeatureMode.Parallel
        mr_bounded_semaphore.feature_mode = _testing_mode
        _bounded_semaphore_repr = repr(mr_bounded_semaphore)
        _chksum = re.search(r"<BoundedSemaphore\(value=[0-9]{1,4}\) object with FeatureMode\.[a-zA-Z]{4,32} mode at \w{10,30}>", _bounded_semaphore_repr)
        assert _chksum is not None, f"The '__repr__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<BoundedSemaphore(value=<Semaphore mount>) object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_bounded_semaphore_repr}*."


    def test_feature_mode(self, mr_bounded_semaphore: BoundedSemaphoreFactory):
        _testing_mode = FeatureMode.Asynchronous

        assert mr_bounded_semaphore.feature_mode is None, "The default value of FeatureMode of BoundedSemaphore instance should be None."
        try:
            mr_bounded_semaphore.feature_mode = _testing_mode
        except Exception:
            assert False, f"It should set the FeatureMode into BoundedSemaphore instance without any issue.\n Error: {traceback.format_exc()}"
        else:
            _feature_mode = mr_bounded_semaphore.feature_mode
            assert _feature_mode is _testing_mode, f"The mode we got from BoundedSemaphore instance should be the same as we set '{_testing_mode}'."


    def test_get_instance_with_parallel_mode(self, mr_bounded_semaphore: BoundedSemaphoreFactory):
        try:
            _bounded_semaphore = mr_bounded_semaphore.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_bounded_semaphore.feature_mode = FeatureMode.Parallel
        _bounded_semaphore = mr_bounded_semaphore.get_instance()
        from multiprocessing.synchronize import BoundedSemaphore
        assert _bounded_semaphore is not None and isinstance(_bounded_semaphore, BoundedSemaphore) is True, "This type of BoundedSemaphore instance should be 'multiprocessing.synchronize.BoundedSemaphore'."


    def test_get_instance_with_concurrent_mode(self, mr_bounded_semaphore: BoundedSemaphoreFactory):
        try:
            _bounded_semaphore = mr_bounded_semaphore.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_bounded_semaphore.feature_mode = FeatureMode.Concurrent
        _bounded_semaphore = mr_bounded_semaphore.get_instance()
        from threading import BoundedSemaphore
        assert _bounded_semaphore is not None and isinstance(_bounded_semaphore, BoundedSemaphore) is True, "This type of BoundedSemaphore instance should be 'threading.BoundedSemaphore'."


    def test_get_instance_with_coroutine_mode(self, mr_bounded_semaphore: BoundedSemaphoreFactory):
        try:
            _bounded_semaphore = mr_bounded_semaphore.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_bounded_semaphore.feature_mode = FeatureMode.GreenThread
        _bounded_semaphore = mr_bounded_semaphore.get_instance()
        from gevent.lock import BoundedSemaphore
        assert _bounded_semaphore is not None and isinstance(_bounded_semaphore, BoundedSemaphore) is True, "This type of Semaphore instance should be 'gevent.lock.BoundedSemaphore'."


    def test_get_instance_with_asynchronous_mode(self, mr_bounded_semaphore: BoundedSemaphoreFactory):
        from asyncio.locks import BoundedSemaphore
        from asyncio import new_event_loop

        try:
            _bounded_semaphore = mr_bounded_semaphore.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_bounded_semaphore.feature_mode = FeatureMode.Asynchronous
        _bounded_semaphore = mr_bounded_semaphore.get_instance(event_loop=new_event_loop())
        assert _bounded_semaphore is not None and isinstance(_bounded_semaphore, BoundedSemaphore) is True, "This type of BoundedSemaphore instance should be 'asyncio.locks.BoundedSemaphore'."


    def test_globalize_instance(self, mr_bounded_semaphore: BoundedSemaphoreFactory):
        from multirunnable.api.manage import Running_Bounded_Semaphore
        assert Running_Bounded_Semaphore is None, "It should be None before we do anything."

        mr_bounded_semaphore.feature_mode = FeatureMode.Parallel
        _bounded_semaphore = mr_bounded_semaphore.get_instance()
        mr_bounded_semaphore.globalize_instance(_bounded_semaphore)

        from multirunnable.api.manage import Running_Bounded_Semaphore
        assert Running_Bounded_Semaphore is _bounded_semaphore, "It should be the instance we instantiated."


