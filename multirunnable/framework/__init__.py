"""
The framework section code:

    1. Work Flow
    2. Features


1. Work Flow Description:
    Like words, classify the multi-working job by logic of work flow:

    Initialization -> Assign job -> Start to run -(wait for it done)-> Close the resource and get the result if it has
    recorded -(if it has result data)-> persistence the data.

    1-1. Initialization
    1-2. Assign job
    1-3. Start to run
    1-4. Close the resource and get the result if it has recorded
    1-5. Persistence the data


2. Features Description:
    The features part target record some features which usually be used in multi-working program. For instances, Lock,
    RLock, Semaphore, Bounded Semaphore, Event and condition.

    2-1. Lock
    2-2. RLock
    2-3. Event
    2-4. Condition
    2-5. Semaphore
    2-6. Bounded Semaphore
    2-7. Queue

"""

from multirunnable.framework.task import BaseTask, BaseQueueTask

from multirunnable.framework.strategy import RunnableStrategy, AsyncRunnableStrategy, Resultable
from multirunnable.framework.features import (
    BaseQueueType,
    PosixThread,
    PosixThreadCommunication,
    BaseFeatureAdapterFactory,
    BaseGlobalizeAPI)
from multirunnable.framework.result import OceanResult

from multirunnable.framework.api import (
    AdapterOperator, BaseLockAdapterOperator,
    AsyncAdapterOperator, BaseAsyncLockAdapterOperator)

from multirunnable.framework.adapter import BaseIterator, BaseList
