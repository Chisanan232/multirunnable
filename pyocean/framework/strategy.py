from pyocean.framework.task import BaseQueueTask
from pyocean.framework.features import BaseFeatureAdapterFactory
from pyocean.framework.exceptions import FeatureFactoryCannotBeEmpty
from pyocean.types import OceanTasks
from pyocean.mode import FeatureMode
from pyocean.tool import Feature
from pyocean.persistence.interface import OceanPersistence
import pyocean._utils as _utils

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Iterable, Callable, Optional
import logging



class BaseRunnableStrategy(metaclass=ABCMeta):

    _Running_Feature_Mode: Optional[FeatureMode] = None

    def __init__(self, workers_num: int,
                 features_factory: BaseFeatureAdapterFactory = None,
                 persistence_strategy: OceanPersistence = None, **kwargs):
        self._workers_num = workers_num
        self._features_factory = features_factory
        self._persistence_strategy = persistence_strategy
        self._db_conn_num = kwargs.get("db_connection_pool_size", None)


    def __str__(self):
        """
        Description:
            Just a clear and pointed info about this "instance".

        Example:
            BaseRunnableStrategy(workers_num=X, features_factory=Y, persistence_strategy=Z)
        :return:
        """

        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(" \
                               f"workers_num={self._workers_num}, " \
                               f"features_factory={self._features_factory}, " \
                               f"persistence_strategy={self._persistence_strategy}, " \
                               f"db_connection_pool_size={self._db_conn_num})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    def __repr__(self):
        """
        Description:
            More information (like brief, not detail) about class.
        :return:
        """
        pass


    @property
    @abstractmethod
    def workers_number(self) -> int:
        """
        Description:
            The number of threads or processes be create and activate to do something.
        :return:
        """
        pass


    @property
    @abstractmethod
    def db_connection_number(self) -> int:
        """
        Description:
            The number of the connection instances which target to do something operators with database.
        Note:
            The number be suggested to be roughly equal to the CPUs amount of host which the program be run.
        :return:
        """
        pass


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



class RunnableStrategy(BaseRunnableStrategy, ABC):

    @property
    def workers_number(self) -> int:
        """
        Description:
            The number of threads or processes be create and activate to do something.
        :return:
        """
        return self._workers_num


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

        if self._db_conn_num is None:
            if self._workers_num < cpu_count():
                return self._workers_num
            else:
                return cpu_count()
        else:
            if self._db_conn_num > cpu_count():
                logging.warning("Warning about suggestion is the best "
                                "configuration of database connection instance "
                                "should be less than CPU amounts.")
            return self._db_conn_num


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

        # # # # Think about how to design the initialization like lock, semaphore or queue
        # # # # beside design, needs to more think about how to use it? how to extend it? how to maintain it?
        # # Queue initialization
        if queue_tasks is not None:
            self._features_factory_exist(factory=self._features_factory)
            self._init_queue_process(tasks=queue_tasks)

        # # Filter mechanism
        __lock_features = filter(lambda __feature: __feature not in [Feature.Event, Feature.Condition], features)
        __communication_features = filter(lambda __feature: __feature in [Feature.Event, Feature.Condition], features)

        # # Lock initialization
        if __lock_features:
            self._features_factory_exist(factory=self._features_factory)
            self._init_lock_process(features=__lock_features)

        # # Communication initialization
        if __communication_features:
            self._features_factory_exist(factory=self._features_factory)
            self._init_communication_process(features=__communication_features)


    def _features_factory_exist(self, factory: BaseFeatureAdapterFactory, force: bool = True) -> bool:
        if factory is not None:
            return True
        else:
            if force is True:
                raise FeatureFactoryCannotBeEmpty
            else:
                return False


    def _init_queue_process(self, tasks: List[BaseQueueTask]) -> None:
        """
        Initialize Queue object which be needed to handle in Queue-Task-List.
        :param tasks:
        :return:
        """

        __queue_adapter = self._features_factory.get_queue_adapter()
        __globalize = self._features_factory.get_globalization()
        for task in tasks:
            __queue = __queue_adapter.init_queue_with_values(qtype=task.queue_type, values=task.value)
            __globalize.queue(name=task.name, queue=__queue)


    def _init_lock_process(self, features: Iterable[Feature], **adapter_kwargs) -> None:
        """
        Initialize Lock object (Lock, RLock, Semaphore, Bounded Semaphore)
        which be needed to handle in Feature-List.
        :param features:
        :return:
        """

        __lock_adapter = self._features_factory.get_lock_adapter(**adapter_kwargs)
        __globalize = self._features_factory.get_globalization()
        for feature in features:
            if feature == Feature.Lock:
                __lock = __lock_adapter.get_lock()
                __globalize.lock(lock=__lock)
            if feature == Feature.RLock:
                __rlock = __lock_adapter.get_rlock()
                __globalize.rlock(rlock=__rlock)
            if feature == Feature.Semaphore:
                __semaphore = __lock_adapter.get_semaphore(value=self.db_connection_number)
                __globalize.semaphore(smp=__semaphore)
            if feature == Feature.Bounded_Semaphore:
                __bounded_semaphore = __lock_adapter.get_bounded_semaphore(value=self.db_connection_number)
                __globalize.bounded_semaphore(bsmp=__bounded_semaphore)


    def _init_communication_process(self, features: Iterable[Feature], **adapter_kwargs) -> None:
        """
        Initialize Lock object (Event, Condition) which be needed to
        handle in Feature-List.
        :param features:
        :return:
        """

        __communication_adapter = self._features_factory.get_communication_adapter(**adapter_kwargs)
        __globalize = self._features_factory.get_globalization()
        for feature in features:
            if feature == feature.Event:
                __event = __communication_adapter.get_event()
                __globalize.event(event=__event)
            if feature == feature.Condition:
                __condition = __communication_adapter.get_condition()
                __globalize.condition(condition=__condition)



class AsyncRunnableStrategy(RunnableStrategy, ABC):

    async def initialization(self, queue_tasks: Optional[List[BaseQueueTask]] = None,
                             features: Optional[List[Feature]] = None, *args, **kwargs) -> None:
        """
        Description:
            Asynchronous version of method 'initialization'.
        :param queue_tasks:
        :param features:
        :param args:
        :param kwargs:
        :return:
        """

        # # Queue initialization
        if queue_tasks is not None:
            self._features_factory_exist(factory=self._features_factory)
            await self._init_queue_process(tasks=queue_tasks)

        # # Filter mechanism
        __lock_features = filter(lambda __feature: __feature not in [Feature.Event, Feature.Condition], features)
        __communication_features = filter(lambda __feature: __feature in [Feature.Event, Feature.Condition], features)

        __async_kwgs = {}
        __event_loop = kwargs.get("event_loop", None)
        if __event_loop is None:
            raise Exception("Async Event Loop object cannot be empty.")
        __async_kwgs["event_loop"] = __event_loop

        # # Lock initialization
        if __lock_features:
            self._features_factory_exist(factory=self._features_factory)
            super()._init_lock_process(features=features, **__async_kwgs)

        # # Communication initialization
        if __communication_features:
            self._features_factory_exist(factory=self._features_factory)
            super()._init_communication_process(features=features, **__async_kwgs)


    async def _init_queue_process(self, tasks: List[BaseQueueTask]) -> None:
        """
        Description:
            Asynchronous version of method '_init_queue_process'.
        :param tasks:
        :return:
        """

        __queue_adapter = self._features_factory.get_queue_adapter()
        __globalize = self._features_factory.get_globalization()
        for task in tasks:
            __queue = await __queue_adapter.async_init_queue_with_values(qtype=task.queue_type, values=task.value)
            __globalize.queue(name=task.name, queue=__queue)


    @abstractmethod
    async def build_workers(self, function: Callable, *args, **kwargs) -> List[OceanTasks]:
        """
        Description:
            Asynchronous version of method 'build_workers'.
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
            Asynchronous version of method 'activate_workers'.
        :param workers_list:
        :return:
        """
        pass


    @abstractmethod
    async def close(self) -> None:
        """
        Description:
            Asynchronous version of method 'close'.
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


