from multirunnable.framework.features import BaseGlobalizeAPI as _BaseGlobalizeAPI
from multirunnable.types import (
    OceanQueue as _OceanQueue,
    OceanLock as _OceanLock,
    OceanRLock as _OceanRLock,
    OceanSemaphore as _OceanSemaphore,
    OceanBoundedSemaphore as _OceanBoundedSemaphore,
    OceanEvent as _OceanEvent,
    OceanCondition as _OceanCondition)
from multirunnable.exceptions import GlobalizeObjectError as _GlobalizeObjectError

from typing import Dict, Optional


Running_Queue: Optional[Dict[str, _OceanQueue]] = {}
Running_Lock: Optional[_OceanLock] = None
Running_RLock: Optional[_OceanRLock] = None
Running_Semaphore: Optional[_OceanSemaphore] = None
Running_Bounded_Semaphore: Optional[_OceanBoundedSemaphore] = None
Running_Event: Optional[_OceanEvent] = None
Running_Condition: Optional[_OceanCondition] = None


class Globalize(_BaseGlobalizeAPI):

    @staticmethod
    def queue(name: str, queue: _OceanQueue) -> None:
        if queue is not None:
            global Running_Queue
            Running_Queue[name] = queue
        else:
            raise _GlobalizeObjectError


    @staticmethod
    def lock(lock: _OceanLock) -> None:
        """
        Description:
            Globalize Lock so that it could run between each different threads or processes.
        :param lock:
        :return:
        """

        if lock is not None:
            global Running_Lock
            Running_Lock = lock
        else:
            raise _GlobalizeObjectError


    @staticmethod
    def rlock(rlock: _OceanRLock) -> None:
        """
        Description:
            Globalize Lock so that it could run between each different threads or processes.
        :param rlock:
        :return:
        """

        if rlock is not None:
            global Running_RLock
            Running_RLock = rlock
        else:
            raise _GlobalizeObjectError


    @staticmethod
    def semaphore(smp: _OceanSemaphore) -> None:
        """
        Description:
            Globalize Semaphore so that it could run between each different threads or processes.
        :param smp:
        :return:
        """

        if smp is not None:
            global Running_Semaphore
            Running_Semaphore = smp
        else:
            raise _GlobalizeObjectError


    @staticmethod
    def bounded_semaphore(bsmp: _OceanBoundedSemaphore) -> None:
        """
        Description:
            Globalize Semaphore so that it could run between each different threads or processes.
        :param bsmp:
        :return:
        """

        if bsmp is not None:
            global Running_Bounded_Semaphore
            Running_Bounded_Semaphore = bsmp
        else:
            raise _GlobalizeObjectError


    @staticmethod
    def event(event: _OceanEvent) -> None:
        if event is not None:
            global Running_Event
            Running_Event = event
        else:
            raise _GlobalizeObjectError


    @staticmethod
    def condition(condition: _OceanCondition) -> None:
        if condition is not None:
            global Running_Condition
            Running_Condition = condition
        else:
            raise _GlobalizeObjectError

