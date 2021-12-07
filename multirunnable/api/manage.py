from multirunnable.framework.features import BaseGlobalizeAPI as _BaseGlobalizeAPI
from multirunnable.types import (
    MRQueue as _MRQueue,
    MRLock as _MRLock,
    MRRLock as _MRRLock,
    MRSemaphore as _MRSemaphore,
    MRBoundedSemaphore as _MRBoundedSemaphore,
    MREvent as _MREvent,
    MRCondition as _MRCondition)
from multirunnable.exceptions import GlobalizeObjectError as _GlobalizeObjectError

from typing import Dict, Optional


Running_Queue: Optional[Dict[str, _MRQueue]] = {}
Running_Lock: Optional[_MRLock] = None
Running_RLock: Optional[_MRRLock] = None
Running_Semaphore: Optional[_MRSemaphore] = None
Running_Bounded_Semaphore: Optional[_MRBoundedSemaphore] = None
Running_Event: Optional[_MREvent] = None
Running_Condition: Optional[_MRCondition] = None


class Globalize(_BaseGlobalizeAPI):

    @staticmethod
    def queue(name: str, queue: _MRQueue) -> None:
        if queue is not None:
            global Running_Queue
            Running_Queue[name] = queue
        else:
            raise _GlobalizeObjectError


    @staticmethod
    def lock(lock: _MRLock) -> None:
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
    def rlock(rlock: _MRRLock) -> None:
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
    def semaphore(smp: _MRSemaphore) -> None:
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
    def bounded_semaphore(bsmp: _MRBoundedSemaphore) -> None:
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
    def event(event: _MREvent) -> None:
        if event is not None:
            global Running_Event
            Running_Event = event
        else:
            raise _GlobalizeObjectError


    @staticmethod
    def condition(condition: _MRCondition) -> None:
        if condition is not None:
            global Running_Condition
            Running_Condition = condition
        else:
            raise _GlobalizeObjectError

