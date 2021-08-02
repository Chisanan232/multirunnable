from pyocean.framework.features import BaseQueueType, BaseGlobalizeAPI
# from pyocean.api.mode import FeatureMode
# from pyocean.api.features_adapter import QueueAdapter
from pyocean.types import (
    OceanTasks,
    OceanQueue,
    OceanLock, OceanRLock,
    OceanSemaphore, OceanBoundedSemaphore,
    OceanEvent, OceanCondition)
from pyocean.persistence.interface import OceanPersistence
from pyocean.exceptions import GlobalizeObjectError

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Iterable, Callable
import logging


Running_Lock: OceanLock = None
Running_RLock: OceanRLock = None
Running_Event: OceanEvent = None
Running_Condition: OceanCondition = None
Running_Semaphore: OceanSemaphore = None
Running_Bounded_Semaphore: OceanBoundedSemaphore = None
Running_Queue: OceanQueue

Database_Connection_Instance_Number = 1


# class InitializeUtils:
#
#     """
#     Sometimes it needs do something pre-process like initialize object or something configuration, etc. before start to
#     run multi-work simultaneously (or be close to). This class focus handling the initialize processes for each different
#     running strategy.
#     """
#
#     def __init__(self, running_mode: FeatureMode, persistence: OceanPersistence = None):
#         self.__running_mode = running_mode
#         self.__persistence_strategy = persistence
#
#
#     def initialize_queue(self, tasks: Iterable, qtype: BaseQueueType) -> None:
#         """
#         Description:
#             Initialize Queue object with the queue type. It should use the queue type which be annotated by each running
#         strategy.
#         Example:
#             from pyocean.concurrent.feature import MultiThreadingQueueType
#
#             queue = MultiThreadingQueueType.Queue
#             queue.put("This is your task content.")
#         :param tasks:
#         :param qtype:
#         :return:
#         """
#         __queue = self._init_tasks_queue(qtype=qtype)
#         __tasks_queue = self._add_task_to_queue(queue=__queue, task=tasks)
#         Globalize.queue(queue=__tasks_queue)
#
#
#     async def async_initialize_queue(self, tasks: Iterable, qtype: BaseQueueType) -> None:
#         """
#         Description:
#             Asynchronously initialize Queue object with the queue type. Here Queue type only for Asynchronous strategy queue.
#         Example:
#             from pyocean.coroutine.feature import AsynchronousQueueType
#
#             queue = AsynchronousQueueType.Queue
#             queue.put("This is your async task content.")
#         :param tasks:
#         :param qtype:
#         :return:
#         """
#         __queue = self._init_tasks_queue(qtype=qtype)
#         __tasks_queue = await self._async_add_task_to_queue(queue=__queue, task=tasks)
#         Globalize.queue(queue=__tasks_queue)
#
#
#     def _init_tasks_queue(self, qtype: BaseQueueType) -> OceanQueue:
#         """
#         Description:
#             Annotating Queue object with queue type.
#         :param qtype:
#         :return:
#         """
#         __queue_api = QueueAdapter(mode=self.__running_mode)
#         __queue = __queue_api.get_queue(qtype=qtype)
#         return __queue
#
#
#     def _add_task_to_queue(self, queue: OceanQueue, task: Iterable) -> OceanQueue:
#         """
#         Description:
#             Adding target tasks into queue object.
#         :param queue:
#         :param task:
#         :return:
#         """
#         for t in task:
#             queue.put(t)
#         return queue
#
#
#     async def _async_add_task_to_queue(self, queue: OceanQueue, task: Iterable) -> OceanQueue:
#         """
#         Description:
#             Adding target tasks into queue object asynchronously.
#         :param queue:
#         :param task:
#         :return:
#         """
#         for t in task:
#             await queue.put(t)
#         return queue
#
#
#     def initialize_persistence(self, **kwargs) -> None:
#         """
#         Description:
#             Initialize persistence strategy needed conditions.
#         :param kwargs:
#         :return:
#         """
#         if self.__persistence_strategy is None:
#             raise Exception
#         self.__persistence_strategy.initialize(mode=self.__running_mode, **kwargs)



class RunnableStrategy(metaclass=ABCMeta):

    def __init__(self, workers_num: int, persistence_strategy: OceanPersistence = None, **kwargs):
        self.__workers_num = workers_num
        self._persistence_strategy = persistence_strategy
        self.__db_conn_num = kwargs.get("db_connection_pool_size", None)


    @property
    def workers_number(self) -> int:
        """
        Description:
            The number of threads or processes be create and activate to do something.
        :return:
        """
        return self.__workers_num


    @property
    def db_connection_number(self) -> int:
        """
        Description:
            The number of the connection instances which target to do something operators with database.
        Note:
            The number be suggested to be roughly equal to the CPUs amount of host which the program be run.
        :return:
        """
        from multiprocessing import cpu_count

        if self.__db_conn_num is None:
            if self.__workers_num < cpu_count():
                return self.__workers_num
            else:
                return cpu_count()
        else:
            if self.__db_conn_num > cpu_count():
                logging.warning("Warning about suggestion is the best "
                                "configuration of database connection instance "
                                "should be less than CPU amounts.")
            return self.__db_conn_num


    def initialization(self, *args, **kwargs) -> None:
        """
        Description:
            Initialize something configurations or something which be needed to be already before run multiple
            threads or processes.
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def build_workers(self, function: Callable, *args, **kwargs) -> List[OceanTasks]:
        """
        Description:
            Assign tasks into each different threads or processes.
        :param function:
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def activate_workers(self, workers_list: List[OceanTasks]) -> None:
        """
        Description:
            Activate multiple threads or processes to run target task(s).
        :param workers_list:
        :return:
        """
        pass


    @abstractmethod
    def close(self) -> None:
        """
        Description:
            The final in procedure which the program should be run.
        :return:
        """
        pass



class AsyncRunnableStrategy(RunnableStrategy, ABC):

    async def initialization(self, tasks: Iterable, *args, **kwargs) -> None:
        pass


    @abstractmethod
    async def build_workers(self, function: Callable, *args, **kwargs) -> List[OceanTasks]:
        """
        Description:
            Assign tasks into each different threads or processes.
        :param function:
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    async def activate_workers(self, workers_list: List[OceanTasks]) -> None:
        """
        Description:
            Activate multiple threads or processes to run target task(s).
        :param workers_list:
        :return:
        """
        pass


    @abstractmethod
    async def close(self) -> None:
        """
        Description:
            The final in procedure which the progeram should be run.
        :return:
        """
        pass



class Resultable(metaclass=ABCMeta):

    @abstractmethod
    def get_result(self) -> Iterable[object]:
        """
        Description:
            Return the result of every tasks done.
        :return:
        """
        pass



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

