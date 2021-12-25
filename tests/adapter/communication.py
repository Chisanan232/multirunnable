from multirunnable.mode import FeatureMode
from multirunnable.adapter.communication import Event, Condition

import pytest
import re


@pytest.fixture(scope="function")
def mr_event() -> Event:
    return Event()


@pytest.fixture(scope="function")
def mr_condition() -> Condition:
    return Condition()



class TestAdapterEvent:

    def test__str__(self, mr_event: Event):
        _lock_str = str(mr_event)
        _chksum = re.search(r"<Event Adapter object with [a-zA-Z]{4,64} mode at [0-9]{10,30}>", _lock_str)
        assert _chksum is not None, f"The '__str__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Event Adapter object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_str}*."


    def test__repr__(self, mr_event: Event):
        _lock_repr = repr(mr_event)
        _chksum = re.search(r"<Event\(\) Adapter object with [a-zA-Z]{4,64} mode at [0-9]{10,30}>", _lock_repr)
        assert _chksum is not None, f"The '__repr__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Event() Adapter object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_repr}*."


    @pytest.mark.skip(reason="not implement testing logic.")
    def test__add__(self, mr_event: Event):
        pass


    def test_feature_mode(self, mr_event: Event):
        _testing_mode = FeatureMode.Parallel

        assert mr_event.feature_mode is None, f"The default value of FeatureMode of Event instance should be None."
        try:
            mr_event.feature_mode = _testing_mode
        except Exception as e:
            assert False, f"It should set the FeatureMode into Event instance without any issue."
        else:
            _feature_mode = mr_event.feature_mode
            assert _feature_mode is _testing_mode, f"The mode we got from Event instance should be the same as we set '{_testing_mode}'."


    def test_get_instance_with_parallel_mode(self, mr_event: Event):
        try:
            _event = mr_event.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."

        mr_event.feature_mode = FeatureMode.Parallel
        _event = mr_event.get_instance()
        from multiprocessing.synchronize import Event
        assert _event is not None and isinstance(_event, Event) is True, f"This type of Lock instance should be 'multiprocessing.synchronize.Event'."


    def test_get_instance_with_concurrent_mode(self, mr_event: Event):
        try:
            _event = mr_event.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."

        mr_event.feature_mode = FeatureMode.Concurrent
        _event = mr_event.get_instance()
        from threading import Event
        assert _event is not None and isinstance(_event, Event) is True, f"This type of Event instance should be 'threading.Event'."


    @pytest.mark.skip(reason="Still thinking about implementing Event, Condition feature of Coroutine.")
    def test_get_instance_with_coroutine_mode(self, mr_event: Event):
        pass
        # try:
        #     _lock = mr_event.get_instance()
        # except ValueError as ve:
        #     assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."
        #
        # mr_event.feature_mode = FeatureMode.GreenThread
        # _lock = mr_event.get_instance()
        # from gevent.threading import Lock
        # assert _lock is not None and isinstance(_lock, Lock) is True, f"This type of Lock instance should be 'gevent.threading.Lock'."


    def test_get_instance_with_asynchronous_mode(self, mr_event: Event):
        from asyncio.locks import Event
        from asyncio import new_event_loop

        try:
            _event = mr_event.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."

        mr_event.feature_mode = FeatureMode.Asynchronous
        _event = mr_event.get_instance(event_loop=new_event_loop())
        assert _event is not None and isinstance(_event, Event) is True, f"This type of Event instance should be 'asyncio.locks.Event'."


    def test_globalize_instance(self, mr_event: Event):
        from multirunnable.api.manage import Running_Event
        assert Running_Event is None, f"It should be None before we do anything."

        mr_event.feature_mode = FeatureMode.Parallel
        _event = mr_event.get_instance()
        mr_event.globalize_instance(_event)

        from multirunnable.api.manage import Running_Event
        assert Running_Event is _event, f"It should be the instance we instantiated."



class TestAdapterCondition:

    def test__str__(self, mr_condition: Condition):
        _lock_str = str(mr_condition)
        _chksum = re.search(r"<Condition Adapter object with [a-zA-Z]{4,64} mode at [0-9]{10,30}>", _lock_str)
        assert _chksum is not None, f"The '__str__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Condition Adapter object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_str}*."


    def test__repr__(self, mr_condition: Condition):
        _lock_repr = repr(mr_condition)
        _chksum = re.search(r"<Condition Adapter object with [a-zA-Z]{4,64} mode at [0-9]{10,30}>", _lock_repr)
        assert _chksum is not None, f"The '__repr__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Condition() Adapter object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_repr}*."


    @pytest.mark.skip(reason="not implement testing logic.")
    def test__add__(self, mr_condition: Condition):
        pass


    def test_feature_mode(self, mr_condition: Condition):
        _testing_mode = FeatureMode.Parallel

        assert mr_condition.feature_mode is None, f"The default value of FeatureMode of Condition instance should be None."
        try:
            mr_condition.feature_mode = _testing_mode
        except Exception as e:
            assert False, f"It should set the FeatureMode into Condition instance without any issue."
        else:
            _feature_mode = mr_condition.feature_mode
            assert _feature_mode is _testing_mode, f"The mode we got from Condition instance should be the same as we set '{_testing_mode}'."


    def test_get_instance_with_parallel_mode(self, mr_condition: Condition):
        try:
            _condition = mr_condition.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."

        mr_condition.feature_mode = FeatureMode.Parallel
        _condition = mr_condition.get_instance()
        from multiprocessing.synchronize import Condition
        assert _condition is not None and isinstance(_condition, Condition) is True, f"This type of Condition instance should be 'multiprocessing.synchronize.Condition'."


    def test_get_instance_with_concurrent_mode(self, mr_condition: Condition):
        try:
            _condition = mr_condition.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."

        mr_condition.feature_mode = FeatureMode.Concurrent
        _condition = mr_condition.get_instance()
        from threading import Condition
        assert _condition is not None and isinstance(_condition, Condition) is True, f"This type of Condition instance should be 'threading.Condition'."


    @pytest.mark.skip(reason="Still thinking about implementing Event, Condition feature of Coroutine.")
    def test_get_instance_with_coroutine_mode(self, mr_condition: Condition):
        pass
        # try:
        #     _lock = mr_event.get_instance()
        # except ValueError as ve:
        #     assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."
        #
        # mr_event.feature_mode = FeatureMode.GreenThread
        # _lock = mr_event.get_instance()
        # from gevent.threading import Lock
        # assert _lock is not None and isinstance(_lock, Lock) is True, f"This type of Condition instance should be 'gevent.threading.Lock'."


    def test_get_instance_with_asynchronous_mode(self, mr_condition: Condition):
        from asyncio.locks import Condition
        from asyncio import new_event_loop

        try:
            _condition = mr_condition.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."

        mr_condition.feature_mode = FeatureMode.Asynchronous
        _condition = mr_condition.get_instance(event_loop=new_event_loop())
        assert _condition is not None and isinstance(_condition, Condition) is True, f"This type of Condition instance should be 'asyncio.locks.Condition'."


    def test_globalize_instance(self, mr_condition: Condition):
        from multirunnable.api.manage import Running_Condition
        assert Running_Condition is None, f"It should be None before we do anything."

        mr_condition.feature_mode = FeatureMode.Parallel
        _condition = mr_condition.get_instance()
        mr_condition.globalize_instance(_condition)

        from multirunnable.api.manage import Running_Condition
        assert Running_Condition is _condition, f"It should be the instance we instantiated."

