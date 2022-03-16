from multirunnable.mode import FeatureMode
from multirunnable.factory.communication import EventFactory, ConditionFactory

import traceback
import pytest
import re


@pytest.fixture(scope="function")
def mr_event() -> EventFactory:
    return EventFactory()


@pytest.fixture(scope="function")
def mr_condition() -> ConditionFactory:
    return ConditionFactory()



class TestAdapterEvent:

    def test__str__(self, mr_event: EventFactory):
        _testing_mode = FeatureMode.Parallel
        mr_event.feature_mode = _testing_mode
        _lock_str = str(mr_event)
        _chksum = re.search(r"<Event object with FeatureMode.[a-zA-Z]{4,32} mode at \w{10,30}>", _lock_str)
        assert _chksum is not None, f"The '__str__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Event object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_str}*."


    def test__repr__(self, mr_event: EventFactory):
        _testing_mode = FeatureMode.Parallel
        mr_event.feature_mode = _testing_mode
        _lock_repr = repr(mr_event)
        _chksum = re.search(r"<Event\(\) object with FeatureMode.[a-zA-Z]{4,32} mode at \w{10,30}>", _lock_repr)
        assert _chksum is not None, f"The '__repr__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Event() object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_repr}*."


    def test_feature_mode(self, mr_event: EventFactory):
        _testing_mode = FeatureMode.Parallel

        assert mr_event.feature_mode is None, "The default value of FeatureMode of Event instance should be None."
        try:
            mr_event.feature_mode = _testing_mode
        except Exception:
            assert False, f"It should set the FeatureMode into Event instance without any issue.\n Error: {traceback.format_exc()}"
        else:
            _feature_mode = mr_event.feature_mode
            assert _feature_mode is _testing_mode, f"The mode we got from Event instance should be the same as we set '{_testing_mode}'."


    def test_get_instance_with_parallel_mode(self, mr_event: EventFactory):
        try:
            _event = mr_event.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_event.feature_mode = FeatureMode.Parallel
        _event = mr_event.get_instance()
        from multiprocessing.synchronize import Event
        assert _event is not None and isinstance(_event, Event) is True, "This type of Lock instance should be 'multiprocessing.synchronize.Event'."


    def test_get_instance_with_concurrent_mode(self, mr_event: EventFactory):
        try:
            _event = mr_event.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_event.feature_mode = FeatureMode.Concurrent
        _event = mr_event.get_instance()
        from threading import Event
        assert _event is not None and isinstance(_event, Event) is True, "This type of Event instance should be 'threading.Event'."


    def test_get_instance_with_coroutine_mode(self, mr_event: EventFactory):
        try:
            _event = mr_event.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."

        mr_event.feature_mode = FeatureMode.GreenThread
        _event = mr_event.get_instance()
        from gevent.event import Event
        assert _event is not None and isinstance(_event, Event) is True, f"This type of Lock instance should be 'gevent.threading.Lock'."


    def test_get_instance_with_asynchronous_mode(self, mr_event: EventFactory):
        from asyncio.locks import Event
        from asyncio import new_event_loop

        try:
            _event = mr_event.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_event.feature_mode = FeatureMode.Asynchronous
        _event = mr_event.get_instance(event_loop=new_event_loop())
        assert _event is not None and isinstance(_event, Event) is True, "This type of Event instance should be 'asyncio.locks.Event'."


    def test_globalize_instance(self, mr_event: EventFactory):
        from multirunnable.api.manage import Running_Event
        assert Running_Event is None, "It should be None before we do anything."

        mr_event.feature_mode = FeatureMode.Parallel
        _event = mr_event.get_instance()
        mr_event.globalize_instance(_event)

        from multirunnable.api.manage import Running_Event
        assert Running_Event is _event, "It should be the instance we instantiated."



class TestAdapterCondition:

    def test__str__(self, mr_condition: ConditionFactory):
        _testing_mode = FeatureMode.Parallel
        mr_condition.feature_mode = _testing_mode
        _lock_str = str(mr_condition)
        _chksum = re.search(r"<Condition object with FeatureMode.[a-zA-Z]{4,32} mode at \w{10,30}>", _lock_str)
        assert _chksum is not None, f"The '__str__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Condition object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_str}*."


    def test__repr__(self, mr_condition: ConditionFactory):
        _testing_mode = FeatureMode.Parallel
        mr_condition.feature_mode = _testing_mode
        _lock_repr = repr(mr_condition)
        _chksum = re.search(r"<Condition object with FeatureMode.[a-zA-Z]{4,32} mode at \w{10,30}>", _lock_repr)
        assert _chksum is not None, f"The '__repr__' format is incorrect. Please check its value. \n" \
                                    f"Its format should be like *<Condition() object with <Feature Mode> mode at <ID of instance>>*. \n" \
                                    f"But it got *{_lock_repr}*."


    def test_feature_mode(self, mr_condition: ConditionFactory):
        _testing_mode = FeatureMode.Parallel

        assert mr_condition.feature_mode is None, "The default value of FeatureMode of Condition instance should be None."
        try:
            mr_condition.feature_mode = _testing_mode
        except Exception:
            assert False, f"It should set the FeatureMode into Event instance without any issue.\n Error: {traceback.format_exc()}"
        else:
            _feature_mode = mr_condition.feature_mode
            assert _feature_mode is _testing_mode, f"The mode we got from Condition instance should be the same as we set '{_testing_mode}'."


    def test_get_instance_with_parallel_mode(self, mr_condition: ConditionFactory):
        try:
            _condition = mr_condition.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_condition.feature_mode = FeatureMode.Parallel
        _condition = mr_condition.get_instance()
        from multiprocessing.synchronize import Condition
        assert _condition is not None and isinstance(_condition, Condition) is True, "This type of Condition instance should be 'multiprocessing.synchronize.Condition'."


    def test_get_instance_with_concurrent_mode(self, mr_condition: ConditionFactory):
        try:
            _condition = mr_condition.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_condition.feature_mode = FeatureMode.Concurrent
        _condition = mr_condition.get_instance()
        from threading import Condition
        assert _condition is not None and isinstance(_condition, Condition) is True, "This type of Condition instance should be 'threading.Condition'."


    def test_get_instance_with_coroutine_mode(self, mr_condition: ConditionFactory):
        try:
            _lock = mr_condition.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), f"It should set the FeatureMode first."

        mr_condition.feature_mode = FeatureMode.GreenThread
        try:
            _lock = mr_condition.get_instance()
        except RuntimeError as re:
            assert "Greenlet doesn't have condition attribute" in str(re), f"It should raise an exception about it doesn't support this feature 'Condition'."
        else:
            assert False, f"It should raise an exception about it doesn't support this feature 'Condition'."


    def test_get_instance_with_asynchronous_mode(self, mr_condition: ConditionFactory):
        from asyncio.locks import Condition
        from asyncio import new_event_loop

        try:
            _condition = mr_condition.get_instance()
        except ValueError as ve:
            assert "FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'." in str(ve), "It should set the FeatureMode first."

        mr_condition.feature_mode = FeatureMode.Asynchronous
        _condition = mr_condition.get_instance(event_loop=new_event_loop())
        assert _condition is not None and isinstance(_condition, Condition) is True, "This type of Condition instance should be 'asyncio.locks.Condition'."


    def test_globalize_instance(self, mr_condition: ConditionFactory):
        from multirunnable.api.manage import Running_Condition
        assert Running_Condition is None, "It should be None before we do anything."

        mr_condition.feature_mode = FeatureMode.Parallel
        _condition = mr_condition.get_instance()
        mr_condition.globalize_instance(_condition)

        from multirunnable.api.manage import Running_Condition
        assert Running_Condition is _condition, "It should be the instance we instantiated."

