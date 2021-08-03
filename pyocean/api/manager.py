from pyocean.framework.features import BaseGlobalizeAPI
from pyocean.types import (
    OceanQueue,
    OceanLock, OceanRLock,
    OceanSemaphore, OceanBoundedSemaphore,
    OceanEvent, OceanCondition)
from pyocean.exceptions import GlobalizeObjectError


Running_Lock: OceanLock = None
Running_RLock: OceanRLock = None
Running_Event: OceanEvent = None
Running_Condition: OceanCondition = None
Running_Semaphore: OceanSemaphore = None
Running_Bounded_Semaphore: OceanBoundedSemaphore = None
Running_Queue: OceanQueue


class Globalize(BaseGlobalizeAPI):

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
    def queue(queue: OceanQueue) -> None:
        if queue is not None:
            global Running_Queue
            Running_Queue = queue
        else:
            raise GlobalizeObjectError
