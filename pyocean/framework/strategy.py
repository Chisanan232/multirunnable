from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.task import BaseQueueTask as _BaseQueueTask
from pyocean.framework.features import BaseFeatureAdapterFactory as  _BaseFeatureAdapterFactory
from pyocean.persistence.interface import OceanPersistence as _OceanPersistence
from pyocean.mode import FeatureMode as _FeatureMode
from pyocean.types import OceanTasks as _OceanTasks
import pyocean._utils as _utils

from abc import ABCMeta, ABC, abstractmethod
from typing import cast, List, Iterable, Callable, Optional, Union
from multipledispatch import dispatch
import logging



class BaseRunnableStrategy(metaclass=ABCMeta):

    def __init__(self, workers_num: int, persistence_strategy: _OceanPersistence = None, **kwargs):
        self._workers_num = workers_num
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
        return f"{self.__str__()} at {id(self.__class__)}"


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


    def initialization(
            self,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
            *args, **kwargs) -> None:
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
    def build_workers(self, function: Callable, *args, **kwargs) -> List[_OceanTasks]:
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
    def activate_workers(self, workers_list: List[_OceanTasks]) -> None:
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

    _Strategy_Feature_Mode: _FeatureMode = None

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


    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        """
        Description:
            Initialize something configurations or something which be
            needed to be already before run multiple threads or processes.
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
            self._init_queue_process(queue_tasks)

        # # Lock and communication features initialization
        if features is not None:
            self._init_lock_or_communication_process(features, **kwargs)


    @dispatch(_BaseQueueTask)
    def _init_queue_process(self, queue_tasks: _BaseQueueTask) -> None:
        """
        Description:
            Initialize Queue object which be needed to handle in Queue-Task-List.
        :param queue_tasks:
        :return:
        """

        queue_tasks.init_queue_with_values()


    @dispatch(_BaseList)
    def _init_queue_process(self, queue_tasks: _BaseList) -> None:
        """
        Description:
            Initialize Queue object which be needed to handle in Queue-Task-List.
        :param queue_tasks:
        :return:
        """

        __queues_iterator = queue_tasks.iterator()
        while __queues_iterator.has_next():
            __queue_adapter = cast(_BaseQueueTask, __queues_iterator.next())
            __queue_adapter.init_queue_with_values()


    @dispatch(_BaseFeatureAdapterFactory)
    def _init_lock_or_communication_process(self, features: _BaseFeatureAdapterFactory, **kwargs) -> None:
        """
        Description:
            Initialize Lock (Lock, RLock, Semaphore, Bounded Semaphore)
            or communication object (Event, Condition) which be needed to
            handle in Feature-List.
        :param features:
        :return:
        """

        features.feature_mode = self._Strategy_Feature_Mode
        __instance = features.get_instance(**kwargs)
        features.globalize_instance(__instance)


    @dispatch(_BaseList)
    def _init_lock_or_communication_process(self, features: _BaseList, **kwargs) -> None:
        """
        Description:
            Initialize Lock (Lock, RLock, Semaphore, Bounded Semaphore)
            or communication object (Event, Condition) which be needed to
            handle in Feature-List.
        :param features:
        :return:
        """

        __features_iterator = features.iterator()
        while __features_iterator.has_next():
            __feature_adapter = cast(_BaseFeatureAdapterFactory, __features_iterator.next())
            __feature_adapter.feature_mode = self._Strategy_Feature_Mode
            __instance = __feature_adapter.get_instance(**kwargs)
            __feature_adapter.globalize_instance(__instance)



class AsyncRunnableStrategy(RunnableStrategy, ABC):

    async def initialization(self,
                             queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                             features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                             *args, **kwargs) -> None:
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
            await self._init_queue_process(queue_tasks)

        # # Lock and communication features initialization
        if features is not None:
            super()._init_lock_or_communication_process(features, **kwargs)


    @dispatch(_BaseQueueTask)
    async def _init_queue_process(self, queue_tasks: _BaseQueueTask) -> None:
        """
        Description:
            Asynchronous version of method '_init_queue_process'.
        :param queue_tasks:
        :return:
        """

        await queue_tasks.async_init_queue_with_values()


    @dispatch(_BaseList)
    async def _init_queue_process(self, queue_tasks: _BaseList) -> None:
        """
        Description:
            Asynchronous version of method '_init_queue_process'.
        :param queue_tasks:
        :return:
        """

        __queues_iterator = queue_tasks.iterator()
        while __queues_iterator.has_next():
            __queue_adapter = cast(_BaseQueueTask, __queues_iterator.next())
            await __queue_adapter.async_init_queue_with_values()


    @abstractmethod
    async def build_workers(self, function: Callable, *args, **kwargs) -> List[_OceanTasks]:
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
    async def activate_workers(self, workers_list: List[_OceanTasks]) -> None:
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


