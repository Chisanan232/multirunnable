from abc import ABCMeta, abstractmethod

from ...types import (
    MRLock as _MRLock, MRRLock as _MRRLock,
    MRSemaphore as _MRSemaphore, MRBoundedSemaphore as _MRBoundedSemaphore,
    MREvent as _MREvent, MRCondition as _MRCondition
)
import multirunnable._utils as _utils



class PosixThread(metaclass=ABCMeta):

    """
    POSIX (Portable Operating System Interface) Thread Specification

    POSIX.1  IEEE Std 1003.1 - 1988
        Process
        Signal: (IPC)
            Floating Point Exception
            Segmentation / Memory Violations
            Illegal Instructions
            Bus Errors
            Timers
        File and Directory Operations
        Pipes
        C library
        I/O Port Interface and Control
        Process Triggers

    POSIX.1b  IEEE Std 1003.1b - 1993
        Priority Scheduling
        Real-Time Signals
        Clocks and Timers
        Semaphores
        Message Passing
        Shared Memory
        Asynchronous and synchronous I/O
        Memory Locking Interface

    POSIX.1c  IEEE Std 1003.1c - 1995
        Thread Creation, Control, and Cleanup
        Thread Scheduling
        Thread Synchronization
        Signal Handling

    POSIX.2  IEEE Std 1003.2 - 1992
        Command Interface
        Utility Programs


    Refer:
    1. https://en.wikipedia.org/wiki/POSIX

    """

    def __str__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    def __repr__(self):
        return f"{self.__str__()} at {id(self.__class__)}"



class PosixThreadLock(PosixThread):

    @abstractmethod
    def get_lock(self, **kwargs) -> _MRLock:
        """
        Description:
            Get Lock object.
        :return:
        """
        pass


    @abstractmethod
    def get_rlock(self, **kwargs) -> _MRRLock:
        """
        Description:
            Get RLock object.
        :return:
        """
        pass


    @abstractmethod
    def get_semaphore(self, value: int, **kwargs) -> _MRSemaphore:
        """
        Description:
            Get Semaphore object.
        :param value:
        :return:
        """
        pass


    @abstractmethod
    def get_bounded_semaphore(self, value: int, **kwargs) -> _MRBoundedSemaphore:
        """
        Description:
            Get Bounded Semaphore object.
        :param value:
        :return:
        """
        pass



class PosixThreadCommunication(PosixThread):

    @abstractmethod
    def get_event(self, *args, **kwargs) -> _MREvent:
        """
        Description:
            Get Event object.
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def get_condition(self, *args, **kwargs) -> _MRCondition:
        """
        Description:
            Get Condition object.
        :param kwargs:
        :return:
        """
        pass

