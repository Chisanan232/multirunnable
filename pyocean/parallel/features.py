from pyocean.framework.features import PosixThreadLock, PosixThreadCommunication, BaseQueue, BaseAPI, BaseQueueType, FeatureUtils

from multiprocessing import Lock, RLock, Event, Condition, Semaphore, BoundedSemaphore
from multiprocessing import (
    Queue as Process_Queue,
    SimpleQueue as Process_SimpleQueue,
    JoinableQueue as Process_JoinableQueue)
from typing import Union

from deprecated.sphinx import deprecated



ProcessQueueDataType = Union[Process_Queue, Process_SimpleQueue, Process_JoinableQueue]


class MultiProcessingQueueType(BaseQueueType):

    Queue = Process_Queue()
    SimpleQueue = Process_SimpleQueue()
    JoinableQueue = Process_JoinableQueue()



class ProcessQueue(BaseQueue):

    def get_queue(self, qtype: MultiProcessingQueueType) -> ProcessQueueDataType:
        return qtype.value



class MultiProcessing(BaseAPI):

    def lock(self):
        return Lock()


    def rlock(self):
        return RLock()


    def event(self, **kwargs):
        return Event()


    def condition(self, **kwargs):
        __lock = FeatureUtils.chk_obj(param="lock", **kwargs)
        # __lock = self.__chk_lock_obj(**kwargs)
        return Condition(lock=__lock)


    @deprecated(version="0.6", reason="Move the method into class 'FeatureUtils'")
    def __chk_lock_obj(self, **kwargs):
        __lock = kwargs.get("lock", None)
        if __lock is None:
            raise Exception("Object 'Event' needs parameter 'Lock' object.")
        return __lock


    def semaphore(self, value: int):
        return Semaphore(value=value)


    def bounded_semaphore(self, value: int):
        return BoundedSemaphore(value=value)


    def queue(self, qtype: MultiProcessingQueueType):
        return qtype.value



class ProcessLock(PosixThreadLock):

    def get_lock(self) -> Lock:
        return Lock()


    def get_rlock(self) -> RLock:
        return RLock()


    def get_semaphore(self, value: int) -> Semaphore:
        return Semaphore(value=value)


    def get_bounded_semaphore(self, value: int) -> BoundedSemaphore:
        return BoundedSemaphore(value=value)



class ProcessCommunication(PosixThreadCommunication):

    def get_event(self, *args, **kwargs) -> Event:
        return Event()


    def get_condition(self, *args, **kwargs) -> Condition:
        __lock: Union[Lock, RLock, None] = kwargs.get("lock", None)
        return Condition(lock=__lock)

