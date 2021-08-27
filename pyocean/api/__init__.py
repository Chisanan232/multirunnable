from pyocean.api.manager import Globalize as _Globalize
from pyocean.api.decorator import (
    ReTryMechanism as _ReTryMechanism,
    retry as _retry,
    LockDecorator as _LockDecorator,
    RunWith as _RunWith,
    AsyncRunWith as _AsyncRunWith)
from pyocean.api.operator import (
    LockOperator as __LockOperator,
    RLockOperator as _RLockOperator,
    SemaphoreOperator as _SemaphoreOperator,
    BoundedSemaphoreOperator as _BoundedSemaphoreOperator,
    EventOperator as _EventOperator,
    ConditionOperator as _ConditionOperator,
    QueueOperator as _QueueOperator)



def LockOperator():
    return __LockOperator()


def RLockOperator():
    return _RLockOperator()


def SemaphoreOperator():
    return _SemaphoreOperator()


def BoundedSemaphoreOperator():
    return _BoundedSemaphoreOperator()


def EventOperator():
    return _EventOperator()


def ConditionOperator():
    return _ConditionOperator()


# def QueueOperator():
#     return _QueueOperator

QueueOperator = _QueueOperator

LockDecorator = _LockDecorator
RunWith = _RunWith
AsyncRunWith = _AsyncRunWith

# The retry mechanism implementation which could be used as Python decorator
retry = _retry

