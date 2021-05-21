from pyocean.framework.features import BaseAPI, BaseQueueType, BaseGlobalizeAPI
from pyocean.persistence.interface import OceanPersistence
from pyocean.exceptions import GlobalizeObjectError

from abc import ABCMeta, abstractmethod
from typing import List, Iterable, Callable, Union
from multiprocessing import Lock as ProcessLock, RLock as ProcessRLock, Semaphore as ProcessSemaphore, Queue as Process_Queue
from multiprocessing.pool import ApplyResult
from threading import Thread, Lock as ThreadLock, RLock as ThreadRLock, Semaphore as ThreadSemaphore
from queue import Queue

from deprecated.sphinx import deprecated


Running_Lock: Union[ProcessLock, ThreadLock] = None
Running_RLock: Union[ProcessRLock, ThreadRLock] = None
Running_Event = None
Running_Condition = None
Running_Semaphore: Union[ProcessSemaphore, ThreadSemaphore] = None
Running_Bounded_Semaphore: Union[ProcessSemaphore, ThreadSemaphore] = None
Running_Queue: Union[Process_Queue, Queue]


class RunnableStrategy(metaclass=ABCMeta):

    def __init__(self, threads_num: int, persistence_strategy: OceanPersistence = None,
                 db_connection_pool_size: int = None, **kwargs):
        self._persistence_strategy = persistence_strategy
        self.__db_conn_instance_num = kwargs.get("db_connection_pool_size", None)
        # # Note:
        # Modify the code to be persistence_mode and it would determine the strategy should use database or file.
        # Question (?) Hoe to handle with the option 'db_connection_pool_size' parameterize?
        # if isinstance(persistence_strategy, BaseFileSaver):
        #     self.__Persistence_Mode = PersistenceMode.FILE_MODE
        #     self._persistence_strategy = persistence_strategy
        # elif isinstance(persistence_strategy, BaseConnection):
        #     self.__Persistence_Mode = PersistenceMode.DATABASE_MODE
        #     self._persistence_strategy = persistence_strategy
        #     if isinstance(persistence_strategy, MultiConnections):
        #         # The database connection instance number should be configure if the persistence mode is database.
        #         # self.__db_conn_instance_num = db_connection_pool_size
        #         self.__db_conn_instance_num = kwargs.get("db_connection_pool_size", None)
        # else:
        #     # Remove the typeerror raised in the future.
        #     raise TypeError("The strategy object should be 'BaseFileSaver' type or 'BaseConnection' type. "
        #                     "Please import pyocean.database.connection.BaseConnection to build one.")

        self.__threads_num = threads_num


    @property
    def threads_number(self) -> int:
        """
        Description:
            The number of threads or processes be create and activate to do something.
        :return:
        """
        return self.__threads_num


    @property
    def db_connection_instances_number(self) -> int:
        """
        Description:
            The number of the connection instances which target to do something operators with database.
        Note:
            The number be suggested to be roughly equal to the CPUs amount of host which the program be run.
        :return:
        """
        from multiprocessing import cpu_count

        if self.__db_conn_instance_num is None:
            if self.__threads_num < cpu_count():
                return self.__threads_num
            else:
                return cpu_count()
        else:
            if self.__db_conn_instance_num > cpu_count():
                print("Warning about suggestion is the best configuration of database connection instance should be "
                      "less than CPU amounts.")
            return self.__db_conn_instance_num


    def init_multi_working(self, tasks: Iterable, *args, **kwargs) -> None:
        """
        Description:
            Initialize something configurations or something which be needed to be already before run multiple
            threads or processes.
        :param tasks:
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def init_tasks_queue(self, qtype: BaseQueueType) -> Union[Process_Queue, Queue]:
        """
        Description:
            Initialize a queue object.

        Note:
            For multiprocessing part, the queue should be determined by parameter which be initialized as general queue
            or others special object like SimpleQueue or JoinableQueue.
        :return:
        """
        pass


    @abstractmethod
    def add_task_to_queue(self, queue: Union[Process_Queue, Queue], task: Iterable) -> Union[Process_Queue, Queue]:
        """
        Description:
            Add target task(s) to appointed queue object.
        :return:
        """
        pass


    @abstractmethod
    def build_multi_workers(self, function: Callable, *args, **kwargs) -> List[Union[Thread, ApplyResult]]:
        """
        Description:
            Assign tasks into each different threads or processes.
        :param function:
        :param args:
        :param kwargs:
        :return:
        """
        pass


    def activate_multi_workers(self, workers_list: List[Union[Thread, ApplyResult]]) -> None:
        """
        Description:
            Activate multiple threads or processes to run target task(s).
        :param workers_list:
        :return:
        """

        # # Method 1.
        for worker in workers_list:
            self.activate_worker(worker=worker)

        # # Method 2.
        # with workers_list as worker:
        #     self.activate_worker(worker=worker)


    @abstractmethod
    def activate_worker(self, worker: Union[Thread, ApplyResult]) -> None:
        """
        Description:
            Each one thread or process running task implementation.
        :param worker:
        :return:
        """
        pass


    @abstractmethod
    def end_multi_working(self) -> None:
        """
        Description:
            The final in procedure which the progeram should be run.
        :return:
        """
        pass



class Resultable(metaclass=ABCMeta):

    @abstractmethod
    def get_multi_working_result(self) -> Iterable[object]:
        """
        Description:
            Return the result of every tasks done.
        :return:
        """
        pass



class Globalize(BaseGlobalizeAPI):

    @staticmethod
    def lock(lock: Union[ThreadLock, ProcessLock]) -> None:
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
    def rlock(rlock: Union[ThreadLock, ProcessLock]) -> None:
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
    def event(event) -> None:
        if event is not None:
            global Running_Event
            Running_Event = event
        else:
            raise GlobalizeObjectError


    @staticmethod
    def condition(condition) -> None:
        if condition is not None:
            global Running_Condition
            Running_Condition = condition
        else:
            raise GlobalizeObjectError


    @staticmethod
    def semaphore(smp: Union[ThreadSemaphore, ProcessSemaphore]) -> None:
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
    def bounded_semaphore(bsmp: Union[ThreadSemaphore, ProcessSemaphore]) -> None:
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
    def queue(queue) -> None:
        if queue is not None:
            global Running_Queue
            Running_Queue = queue
        else:
            raise GlobalizeObjectError


    @staticmethod
    @deprecated(version="0.7", reason="Rename the method to 'queue'.")
    def tasks_queue(tasks_queue: Union[ThreadSemaphore, ProcessSemaphore]) -> None:
        """
        Description:
            Globalize Queue object which saving target tasks the thread or process, etc. target to do so that it could
            run between each different threads or processes.
        :param tasks_queue:
        :return:
        """

        if tasks_queue is not None:
            global Running_Queue
            Running_Queue = tasks_queue
        else:
            raise GlobalizeObjectError

