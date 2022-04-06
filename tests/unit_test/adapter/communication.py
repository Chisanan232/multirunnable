from typing import Union
import pytest

from multirunnable.adapter.communication import AsyncEvent, AsyncCondition
from multirunnable.adapter import Event, Condition
from multirunnable.mode import RunningMode, FeatureMode

from ..._examples import MapByStrategy
from ..framework.lock import EventTestSpec, ConditionTestSpec


def instantiate_event(_mode: Union[RunningMode, FeatureMode], _init: bool, **kwargs) -> Union[Event, AsyncEvent]:
    if _mode is RunningMode.Asynchronous or _mode is FeatureMode.Asynchronous:
        return AsyncEvent(mode=_mode, init=_init, **kwargs)
    else:
        return Event(mode=_mode, init=_init, **kwargs)


def instantiate_condition(_mode: Union[RunningMode, FeatureMode], _init: bool, **kwargs) -> Union[Condition, AsyncCondition]:
    if _mode is RunningMode.Asynchronous or _mode is FeatureMode.Asynchronous:
        return AsyncCondition(mode=_mode, init=_init, **kwargs)
    else:
        return Condition(mode=_mode, init=_init, **kwargs)



class TestAdapterEvent(EventTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread])
    def test_get_feature_instance(self, mode):
        _event = instantiate_event(_mode=mode, _init=True)
        _event_operator = _event._feature_operator

        _global_feature_inst = _event_operator._get_feature_instance()
        _feature_inst = _event_operator._event_instance
        assert _feature_inst is _global_feature_inst, "The feature property should be the 'Semaphore' instance we set."


    def test_feature_in_parallel(self):
        _event = instantiate_event(_mode=FeatureMode.Parallel, _init=True)
        EventTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=_event, running_function=MapByStrategy.Parallel)


    def test_feature_in_concurrent(self):
        _event = instantiate_event(_mode=FeatureMode.Concurrent, _init=True)
        EventTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=_event, running_function=MapByStrategy.Concurrent)


    def test_feature_in_green_thread(self):
        _event = instantiate_event(_mode=FeatureMode.GreenThread, _init=True)
        EventTestSpec._feature_testing(mode=FeatureMode.GreenThread, _lock=_event, running_function=MapByStrategy.CoroutineWithGreenThread)


    def test_feature_in_asynchronous_tasks(self):
        # # # # For Python 3.10, it works finely.
        # # # # In Python 3.7, it run incorrectly. It's possible that the asyncio event loop conflict.
        # _event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop=_event_loop)
        #
        # _event = instantiate_event(_mode=FeatureMode.Asynchronous, _init=True, event_loop=_event_loop)
        _event = AsyncEvent(mode=FeatureMode.Asynchronous)
        EventTestSpec._async_feature_testing(_lock=_event, running_function=MapByStrategy.CoroutineWithAsynchronous, factory=_event)



class TestAdapterCondition(ConditionTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent])
    def test_get_feature_instance(self, mode):
        _condition = instantiate_condition(_mode=mode, _init=True)
        _condition_operator = _condition._feature_operator

        _global_feature_inst = _condition_operator._get_feature_instance()
        _feature_inst = _condition_operator._feature_instance
        assert _feature_inst is _global_feature_inst, "The feature property should be the 'Semaphore' instance we set."


    def test_feature_in_parallel(self):
        _condition = instantiate_condition(_mode=FeatureMode.Parallel, _init=True)
        ConditionTestSpec._feature_testing(mode=FeatureMode.Parallel, _lock=_condition, running_function=MapByStrategy.Parallel)


    def test_feature_by_pykeyword_with_in_parallel(self):
        _condition = instantiate_condition(_mode=FeatureMode.Parallel, _init=True)
        ConditionTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Parallel, _lock=_condition, running_function=MapByStrategy.Parallel)


    def test_feature_in_concurrent(self):
        _condition = instantiate_condition(_mode=FeatureMode.Concurrent, _init=True)
        ConditionTestSpec._feature_testing(mode=FeatureMode.Concurrent, _lock=_condition, running_function=MapByStrategy.Concurrent)


    def test_feature_by_pykeyword_with_in_concurrent(self):
        _condition = instantiate_condition(_mode=FeatureMode.Concurrent, _init=True)
        ConditionTestSpec._feature_testing_by_pykeyword_with(mode=FeatureMode.Concurrent, _lock=_condition, running_function=MapByStrategy.Concurrent)


    def test_feature_in_asynchronous_tasks(self):
        # _event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop=_event_loop)
        #
        # _condition = instantiate_condition(_mode=FeatureMode.Asynchronous, _init=True, event_loop=_event_loop)
        _condition = AsyncCondition(mode=FeatureMode.Asynchronous)
        ConditionTestSpec._async_feature_testing(_lock=_condition, running_function=MapByStrategy.CoroutineWithAsynchronous, factory=_condition)


    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self):
        # _event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop=_event_loop)
        #
        # _condition = instantiate_condition(_mode=FeatureMode.Asynchronous, _init=True, event_loop=_event_loop)
        _condition = AsyncCondition(mode=FeatureMode.Asynchronous)
        ConditionTestSpec._async_feature_testing_by_pykeyword_with(_lock=_condition, running_function=MapByStrategy.CoroutineWithAsynchronous, factory=_condition)


