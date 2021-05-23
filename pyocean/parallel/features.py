from pyocean.framework.features import BaseAPI, BaseQueueType, FeatureUtils

from multiprocessing import Lock, RLock, Event, Condition, Semaphore, BoundedSemaphore
from multiprocessing import Queue as Process_Queue, SimpleQueue as Process_SimpleQueue, JoinableQueue as Process_JoinableQueue

from deprecated.sphinx import deprecated



class MultiProcessingQueueType(BaseQueueType):

    Queue = Process_Queue()
    SimpleQueue = Process_SimpleQueue()
    JoinableQueue = Process_JoinableQueue()



class MultiProcessing(BaseAPI):

    def lock(self):
        return Lock()


    def rlock(self):
        return RLock()


    def event(self, **kwargs):
        __lock = FeatureUtils.chk_obj(param="lock", **kwargs)
        # __lock = self.__chk_lock_obj(**kwargs)
        return Event(lock=__lock)


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
