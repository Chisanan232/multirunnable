from pyocean.framework.features import BaseGlobalizeAPI
from pyocean.types import (
    OceanQueue,
    OceanLock, OceanRLock,
    OceanSemaphore, OceanBoundedSemaphore,
    OceanEvent, OceanCondition)
from pyocean.exceptions import GlobalizeObjectError

from typing import Dict, Optional


Running_Queue: Optional[Dict[str, OceanQueue]] = None
Running_Lock: Optional[OceanLock] = None
Running_RLock: Optional[OceanRLock] = None
Running_Semaphore: Optional[OceanSemaphore] = None
Running_Bounded_Semaphore: Optional[OceanBoundedSemaphore] = None
Running_Event: Optional[OceanEvent] = None
Running_Condition: Optional[OceanCondition] = None


class Globalize(BaseGlobalizeAPI):

    @staticmethod
    def queue(name: str, queue: OceanQueue) -> None:
        if queue is not None:
            global Running_Queue
            Running_Queue[name] = queue
        else:
            raise GlobalizeObjectError


    @staticmethod
    def lock(lock: OceanLock) -> None:
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
            raise GlobalizeObjectError


    @staticmethod
    def rlock(rlock: OceanRLock) -> None:
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
            raise GlobalizeObjectError


    @staticmethod
    def semaphore(smp: OceanSemaphore) -> None:
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
            raise GlobalizeObjectError


    @staticmethod
    def bounded_semaphore(bsmp: OceanBoundedSemaphore) -> None:
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
            raise GlobalizeObjectError


    @staticmethod
    def event(event: OceanEvent) -> None:
        if event is not None:
            global Running_Event
            Running_Event = event
        else:
            raise GlobalizeObjectError


    @staticmethod
    def condition(condition: OceanCondition) -> None:
        if condition is not None:
            global Running_Condition
            Running_Condition = condition
        else:
            raise GlobalizeObjectError

