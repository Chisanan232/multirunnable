from pyocean.types import OceanTasks
from pyocean.framework.task import BaseQueueTask
from pyocean.api.mode import FeatureMode
from pyocean.api.features_adapter import Feature, QueueAdapter, LockAdapter, CommunicationAdapter
from pyocean.api.manager import Globalize as RunningGlobalize
from pyocean.persistence.interface import OceanPersistence

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Iterable, Callable, Optional
import logging



class RunnableStrategy(metaclass=ABCMeta):

    _Running_Feature_Mode: Optional[FeatureMode] = None

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


    def initialization(self, queue_tasks: Optional[List[BaseQueueTask]] = None,
                       features: Optional[List[Feature]] = None, *args, **kwargs) -> None:
        """
        Description:
            Initialize something configurations or something which be needed to be already before run multiple
            threads or processes.
        :param queue_tasks:
        :param features:
        :param args:
        :param kwargs:
        :return:
        """

        # # Semaphore part (Limitation)
        # # # # Think about how to design the initialization like lock, semaphore or queue
        # # # # beside design, needs to more think about how to use it? how to extend it? how to maintain it?
        # # Queue initialization
        if queue_tasks is not None:
            self._init_queue_process(tasks=queue_tasks)

        # # Filter mechanism
        __lock_features = filter(lambda __feature: __feature not in [Feature.Event, Feature.Condition], features)
        __communication_features = filter(lambda __feature: __feature in [Feature.Event, Feature.Condition], features)

        # # Lock initialization
        if __lock_features:
            self._init_lock_process(features=__lock_features)

        # # Communication initialization
        if __communication_features:
            self._init_communication_process(features=__communication_features)


    def _init_queue_process(self, tasks: List[BaseQueueTask]) -> None:
        """
        Initialize Queue object which be needed to handle in Queue-Task-List.
        :param tasks:
        :return:
        """

        __queue_adapter = QueueAdapter(mode=self._Running_Feature_Mode)
        for task in tasks:
            __queue = __queue_adapter.init_queue_with_values(qtype=task.queue_type, values=task.value)
            RunningGlobalize.queue(name=task.name, queue=__queue)


    def _init_lock_process(self, features: Iterable[Feature], **adapter_kwargs) -> None:
        """
        Initialize Lock object (Lock, RLock, Semaphore, Bounded Semaphore)
        which be needed to handle in Feature-List.
        :param features:
        :return:
        """

        __lock_adapter = LockAdapter(mode=self._Running_Feature_Mode, **adapter_kwargs)
        for feature in features:
            if feature == Feature.Lock:
                __lock = __lock_adapter.get_lock()
                RunningGlobalize.lock(lock=__lock)
            if feature == Feature.RLock:
                __rlock = __lock_adapter.get_rlock()
                RunningGlobalize.rlock(rlock=__rlock)
            if feature == Feature.Semaphore:
                __semaphore = __lock_adapter.get_semaphore(value=self.db_connection_number)
                RunningGlobalize.semaphore(smp=__semaphore)
            if feature == Feature.Bounded_Semaphore:
                __bounded_semaphore = __lock_adapter.get_bounded_semaphore(value=self.db_connection_number)
                RunningGlobalize.bounded_semaphore(bsmp=__bounded_semaphore)


    def _init_communication_process(self, features: Iterable[Feature], **adapter_kwargs) -> None:
        """
        Initialize Lock object (Event, Condition) which be needed to
        handle in Feature-List.
        :param features:
        :return:
        """

        __communication_adapter = CommunicationAdapter(mode=self._Running_Feature_Mode, **adapter_kwargs)
        for feature in features:
            if feature.Event:
                __event = __communication_adapter.get_event()
                RunningGlobalize.event(event=__event)
            if feature.Condition:
                __condition = __communication_adapter.get_event()
                RunningGlobalize.condition(condition=__condition)


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

    async def initialization(self, queue_tasks: Optional[List[BaseQueueTask]] = None,
                             features: Optional[List[Feature]] = None, *args, **kwargs) -> None:
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


