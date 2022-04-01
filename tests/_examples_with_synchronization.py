from multirunnable import RunningMode, FeatureMode
from multirunnable.factory.lock import LockFactory, RLockFactory, SemaphoreFactory, BoundedSemaphoreFactory
from multirunnable.factory.communication import EventFactory, ConditionFactory

from .test_config import Worker_Size, Worker_Pool_Size, Task_Size, Semaphore_Value

from typing import Union


_Worker_Size = Worker_Size
_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size

_Semaphore_Value = Semaphore_Value

_Sleep_Time: int = 1
_Random_Start_Time: int = 60
_Random_End_Time: int = 80

_Default_Value: int = 1


def instantiate_lock(_mode: Union[RunningMode, FeatureMode], **kwargs):
    _lock = LockFactory()
    return _initial(_lock, _mode, **kwargs)


def instantiate_rlock(_mode: Union[RunningMode, FeatureMode], **kwargs):
    _rlock = RLockFactory()
    return _initial(_rlock, _mode, **kwargs)


def instantiate_semaphore(_mode: Union[RunningMode, FeatureMode], **kwargs):
    _semaphore = SemaphoreFactory(value=_Semaphore_Value)
    return _initial(_semaphore, _mode, **kwargs)


def instantiate_bounded_semaphore(_mode: Union[RunningMode, FeatureMode], **kwargs):
    _bounded_semaphore = BoundedSemaphoreFactory(value=_Semaphore_Value)
    return _initial(_bounded_semaphore, _mode, **kwargs)


def instantiate_event(_mode: Union[RunningMode, FeatureMode], **kwargs):
    _event = EventFactory()
    return _initial(_event, _mode, **kwargs)


def instantiate_condition(_mode: Union[RunningMode, FeatureMode], **kwargs):
    _condition = ConditionFactory()
    return _initial(_condition, _mode, **kwargs)


def _initial(_feature_factory, _mode: Union[RunningMode, FeatureMode], **kwargs):
    if type(_mode) is RunningMode:
        _feature_factory.feature_mode = _mode.value["feature"]
    else:
        _feature_factory.feature_mode = _mode

    _feature_instn = _feature_factory.get_instance(**kwargs)
    _feature_factory.globalize_instance(_feature_instn)

    return _feature_instn
