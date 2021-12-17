from multirunnable.api.manage import Globalize
from multirunnable.exceptions import GlobalizeObjectError

import pytest



class TestGlobalize:

    def test_queue_with_none_value(self):
        _test_name = "test_name"

        try:
            Globalize.queue(name=_test_name, queue=None)
        except GlobalizeObjectError as e:
            assert "Cannot globalize target object because it is None object" in str(e), f"It should raise an exception about target object could not be a None object."
        else:
            assert False, f"It should raise an exception if the value is None."


    def test_queue_with_normal_value(self):
        _test_name = "test_name"
        _test_value = "test_value"

        try:
            Globalize.queue(name=_test_name, queue=None)
        except GlobalizeObjectError as e:
            assert "Cannot globalize target object because it is None object" in str(e), f"It should raise an exception about target object could not be a None object."
        else:
            assert False, f"It should raise an exception if the value is None."

        Globalize.queue(name=_test_name, queue=_test_value)
        from multirunnable.api.manage import Running_Queue
        assert _test_name in Running_Queue.keys(), f"The testing name '{_test_name}' should be in the keys."
        assert _test_value == Running_Queue[_test_name], f"The value should be the same as we set '{_test_value}'."


    def test_lock_with_none_value(self):
        try:
            Globalize.lock(lock=None)
        except GlobalizeObjectError as e:
            assert "Cannot globalize target object because it is None object" in str(e), f"It should raise an exception about target object could not be a None object."
        else:
            assert False, f"It should raise an exception if the value is None."


    def test_lock_with_normal_value(self):
        from multiprocessing.synchronize import Lock as synchronize_Lock
        from multiprocessing import Lock

        Globalize.lock(lock=Lock())
        from multirunnable.api.manage import Running_Lock
        assert isinstance(Running_Lock, synchronize_Lock) is True, f"It should save instance to the target global variable *Running_Lock*."


    def test_rlock_with_none_value(self):
        try:
            Globalize.rlock(rlock=None)
        except GlobalizeObjectError as e:
            assert "Cannot globalize target object because it is None object" in str(e), f"It should raise an exception about target object could not be a None object."
        else:
            assert False, f"It should raise an exception if the value is None."


    def test_rlock_with_normal_value(self):
        from multiprocessing.synchronize import RLock as synchronize_RLock
        from multiprocessing import RLock

        Globalize.rlock(rlock=RLock())
        from multirunnable.api.manage import Running_RLock
        assert isinstance(Running_RLock, synchronize_RLock) is True, f"It should save instance to the target global variable *Running_RLock*."


    def test_semaphore_with_none_value(self):
        try:
            Globalize.semaphore(smp=None)
        except GlobalizeObjectError as e:
            assert "Cannot globalize target object because it is None object" in str(e), f"It should raise an exception about target object could not be a None object."
        else:
            assert False, f"It should raise an exception if the value is None."


    def test_semaphore_with_normal_value(self):
        from multiprocessing.synchronize import Semaphore as synchronize_Semaphore
        from multiprocessing import Semaphore

        Globalize.semaphore(smp=Semaphore())
        from multirunnable.api.manage import Running_Semaphore
        assert isinstance(Running_Semaphore, synchronize_Semaphore) is True, f"It should save instance to the target global variable *Running_Semaphore*."


    def test_bounded_semaphore_with_none_value(self):
        try:
            Globalize.bounded_semaphore(bsmp=None)
        except GlobalizeObjectError as e:
            assert "Cannot globalize target object because it is None object" in str(e), f"It should raise an exception about target object could not be a None object."
        else:
            assert False, f"It should raise an exception if the value is None."


    def test_bounded_semaphore_with_normal_value(self):
        from multiprocessing.synchronize import Semaphore as synchronize_Semaphore
        from multiprocessing import BoundedSemaphore

        Globalize.bounded_semaphore(bsmp=BoundedSemaphore())
        from multirunnable.api.manage import Running_Bounded_Semaphore
        assert isinstance(Running_Bounded_Semaphore, synchronize_Semaphore) is True, f"It should save instance to the target global variable *Running_Bounded_Semaphore*."


    def test_event_with_none_value(self):
        try:
            Globalize.event(event=None)
        except GlobalizeObjectError as e:
            assert "Cannot globalize target object because it is None object" in str(e), f"It should raise an exception about target object could not be a None object."
        else:
            assert False, f"It should raise an exception if the value is None."


    def test_event_with_normal_value(self):
        from multiprocessing.synchronize import Event as synchronize_Event
        from multiprocessing import Event

        Globalize.event(event=Event())
        from multirunnable.api.manage import Running_Event
        assert isinstance(Running_Event, synchronize_Event) is True, f"It should save instance to the target global variable *Running_Event*."


    def test_condition_with_none_value(self):
        try:
            Globalize.condition(condition=None)
        except GlobalizeObjectError as e:
            assert "Cannot globalize target object because it is None object" in str(e), f"It should raise an exception about target object could not be a None object."
        else:
            assert False, f"It should raise an exception if the value is None."


    def test_condition_with_normal_value(self):
        from multiprocessing.synchronize import Condition as synchronize_Condition
        from multiprocessing import Condition

        Globalize.condition(condition=Condition())
        from multirunnable.api.manage import Running_Condition
        assert isinstance(Running_Condition, synchronize_Condition) is True, f"It should save instance to the target global variable *Running_Condition*."

