from multirunnable.api.manage import Globalize as _Globalize
from multirunnable.api.decorator import (
    retry as _retry,
    async_retry as _async_retry,
    RunWith as _RunWith,
    AsyncRunWith as _AsyncRunWith)
from multirunnable.api.operator import (
    LockAdapterOperator as __LockOperator,
    RLockOperator as _RLockOperator,
    SemaphoreOperator as _SemaphoreOperator,
    BoundedSemaphoreOperator as _BoundedSemaphoreOperator,
    EventOperator as _EventOperator,
    ConditionOperator as _ConditionOperator,
    LockAsyncOperator as _LockAsyncOperator,
    SemaphoreAsyncOperator as _SemaphoreAsyncOperator,
    BoundedSemaphoreAsyncOperator as _BoundedSemaphoreAsyncOperator,
    EventAsyncOperator as _EventAsyncOperator,
    ConditionAsyncOperator as _ConditionAsyncOperator,
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


def LockAsyncOperator():
    return _LockAsyncOperator()


def SemaphoreAsyncOperator():
    return _SemaphoreAsyncOperator()


def BoundedSemaphoreAsyncOperator():
    return _BoundedSemaphoreAsyncOperator()


def EventAsyncOperator():
    return _EventAsyncOperator()


def ConditionAsyncOperator():
    return _ConditionAsyncOperator()


# def QueueOperator():
#     return _QueueOperator

QueueOperator = _QueueOperator

RunWith = _RunWith
AsyncRunWith = _AsyncRunWith

# The retry mechanism implementation which could be used as Python decorator
retry = _retry
async_retry = _async_retry

