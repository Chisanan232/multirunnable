from multirunnable.framework.adapter.collection import BaseList as _BaseList
from multirunnable.framework.task import (
    BaseQueueTask as _BaseQueueTask,
    BasePersistenceTask as _BasePersistenceTask)
from multirunnable.framework.features import BaseFeatureAdapterFactory as  _BaseFeatureAdapterFactory
from multirunnable.framework.result import OceanResult as _OceanResult
from multirunnable.mode import FeatureMode as _FeatureMode
from multirunnable.types import OceanTasks as _OceanTasks
import multirunnable._utils as _utils

from abc import ABCMeta, ABC, abstractmethod
from types import MethodType, FunctionType
from typing import cast, List, Tuple, Dict, Iterable, Callable, Optional, Union
from functools import partial as PartialFunctionType
from multipledispatch import dispatch
import logging



class BaseRunnableStrategy(metaclass=ABCMeta):

    def __init__(self, persistence: _BasePersistenceTask = None):
        self._persistence_strategy = None
        self._db_conn_num = None
        if persistence is not None:
            self.__persistence = persistence
            self._persistence_strategy = persistence.strategy
            self._db_conn_num = persistence.connection_pool_size


    def __str__(self):
        """
        Description:
            Just a clear and pointed info about this "instance".
        :return:
        """
        return f"{self.__str__()} at {id(self.__class__)}"


    def __repr__(self):
        """
        Description:
            More information (like brief, not detail) about class.

        Example:
            BaseRunnableStrategy(persistence=X)
        :return:
        """
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(persistence={self.__persistence}) "
        else:
            __instance_brief = __cls_str
        return __instance_brief


    @property
    @abstractmethod
    def db_connection_pool_size(self) -> int:
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
    def close(self, *args, **kwargs) -> None:
        """
        Description:
            Close and join executor or pool.
        :return:
        """
        pass


    @abstractmethod
    def terminal(self) -> None:
        """
        Description:
            Terminate executor or pool.
        :return:
        """
        pass



class RunnableInitialization:

    _Strategy_Feature_Mode: _FeatureMode = None

    def __init__(self, mode: _FeatureMode):
        self._Strategy_Feature_Mode = mode


    @dispatch(_BaseQueueTask)
    def init_queue_process(self, queue_tasks: _BaseQueueTask) -> None:
        """
        Description:
            Initialize Queue object which be needed to handle in Queue-Task-List.
        :param queue_tasks:
        :return:
        """

        queue_tasks.init_queue_with_values()


    @dispatch(_BaseList)
    def init_queue_process(self, queue_tasks: _BaseList) -> None:
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
    def init_lock_or_communication_process(self, features: _BaseFeatureAdapterFactory, **kwargs) -> None:
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
    def init_lock_or_communication_process(self, features: _BaseList, **kwargs) -> None:
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



class RunnableStrategy(BaseRunnableStrategy, ABC):

    _Strategy_Feature_Mode: _FeatureMode = None
    __Initialization = None

    def __init__(self, persistence: _BasePersistenceTask = None):
        super().__init__(persistence=persistence)
        self.__Initialization = RunnableInitialization(mode=self._Strategy_Feature_Mode)


    @property
    def db_connection_pool_size(self) -> int:
        """
        Description:
            The number of the connection instances which target to do something operators with database.
        Note:
            The number be suggested to be roughly equal to the CPUs amount of host which the program be run.
        :return:
        """
        from multiprocessing import cpu_count

        if self._db_conn_num < 0:
            raise ValueError("The database connection pool size cannot less than 0.")

        if self._db_conn_num is None or self._db_conn_num == 0:
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


    def _init_queue_process(self, queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]]) -> None:
        self.__Initialization.init_queue_process(queue_tasks)


    def _init_lock_or_communication_process(self, features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]], **kwargs) -> None:
        self.__Initialization.init_lock_or_communication_process(features, **kwargs)



class GeneralRunnableStrategy(RunnableStrategy):
    
    def __init__(self, executors: int, persistence: _BasePersistenceTask = None):
        super(GeneralRunnableStrategy, self).__init__(persistence=persistence)
        self._executors_num = executors


    @property
    def executors_number(self) -> int:
        """
        Description:
            The number of executors (processes, threads, etc) be created and activated to do something.
        :return:
        """
        return self._executors_num


    def run(self,
            function: Callable,
            args: Optional[Union[Tuple, Dict]] = None,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        """
        Description:
            Generally running multiple target tasks.
        :param function:
        :param args:
        :param queue_tasks:
        :param features:
        :return:
        """
        self.initialization(queue_tasks=queue_tasks, features=features)
        __workers_list = [self._generate_worker(function, args) for _ in range(self.executors_number)]
        self.activate_workers(__workers_list)
        self.close(__workers_list)


    def map(self,
            function: Callable,
            args_iter: Iterable = [],
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        """
        Description:
            Map version of running target function by the iterator of arguments.
        :param function:
        :param args_iter:
        :param queue_tasks:
        :param features:
        :return:
        """
        self.initialization(queue_tasks=queue_tasks, features=features)
        # __workers_list = map(self._generate_worker, args_iter)
        __workers_list = [self._generate_worker(function, args) for args in args_iter]
        self.activate_workers(list(__workers_list))
        self.close(__workers_list)


    def map_with_function(self,
                          functions: Iterable[Callable],
                          args_iter: Iterable = [],
                          queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                          features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        """
        Description:
            Map by (functions, arguments).
        :param functions:
        :param args_iter:
        :param queue_tasks:
        :param features:
        :return:
        """
        # self.__chk_function_and_args(functions=functions, args_iter=args_iter)
        if args_iter is None or args_iter == []:
            args_iter = [() for _ in range(len(list(functions)))]

        self.initialization(queue_tasks=queue_tasks, features=features)
        __workers_list = [self._generate_worker(fun, args) for fun, args in zip(functions, args_iter)]
        self.activate_workers(__workers_list)
        self.close(__workers_list)


    @dispatch((FunctionType, MethodType, PartialFunctionType), type(None))
    def _generate_worker(self, function: Callable, args) -> _OceanTasks:
        __worker = self.generate_worker(function)
        return __worker


    @dispatch((FunctionType, MethodType, PartialFunctionType), tuple)
    def _generate_worker(self, function: Callable, args) -> _OceanTasks:
        __worker = self.generate_worker(function, *args)
        return __worker


    @dispatch((FunctionType, MethodType, PartialFunctionType), dict)
    def _generate_worker(self, function: Callable, args) -> _OceanTasks:
        __worker = self.generate_worker(function, **args)
        return __worker


    @abstractmethod
    def generate_worker(self, target: Callable, *args, **kwargs) -> _OceanTasks:
        """
        Description:
            Initial and instantiate multiple executors (processes, threads, etc).
        :return:
        """
        pass


    @abstractmethod
    def activate_workers(self, workers: Union[_OceanTasks, List[_OceanTasks]]) -> None:
        """
        Description:
            Activate multiple executors (processes, threads, etc) to run target task(s).
        :return:
        """
        pass


    @abstractmethod
    def start_new_worker(self, target: Callable, *args, **kwargs) -> None:
        """
        Description:
            Initial and activate an executor (process, thread, etc).
        :return:
        """
        pass


    @abstractmethod
    def close(self, workers: Union[_OceanTasks, List[_OceanTasks]]) -> None:
        """
        Description:
            Close and join executor.
        :return:
        """
        pass


    @abstractmethod
    def kill(self) -> None:
        """
        Description:
            Kill executor.
        :return:
        """
        pass



class PoolRunnableStrategy(RunnableStrategy):

    def __init__(self, pool_size: int, tasks_size: int, persistence: _BasePersistenceTask = None):
        super(PoolRunnableStrategy, self).__init__(persistence=persistence)
        self._pool_size = pool_size
        self._tasks_size = tasks_size


    @property
    def pool_size(self) -> int:
        """
        Description:
            The number of executors (process, thread, etc) which been
            instantiated and temporally saving in Pool.
        :return:
        """
        return self._pool_size


    @property
    def tasks_size(self) -> int:
        """
        Description:
            The number of threads or processes be create and activate to do something.
        :return:
        """
        return self._tasks_size


    @abstractmethod
    def apply(self, function: Callable, *args, **kwargs) -> None:
        """
        Description:
            Refer to multiprocessing.pool.apply.
        :return:
        """
        pass


    @abstractmethod
    def async_apply(self,
                    function: Callable,
                    args: Tuple = (),
                    kwargs: Dict = {},
                    callback: Callable = None,
                    error_callback: Callable = None) -> None:
        """
        Description:
            Refer to multiprocessing.pool.apply_async.
        :return:
        """
        pass


    @abstractmethod
    def map(self, function: Callable, args_iter: Iterable = (), chunksize: int = None) -> None:
        """
        Description:
            Refer to multiprocessing.pool.map.
        :return:
        """
        pass


    @abstractmethod
    def async_map(self,
                  function: Callable,
                  args_iter: Iterable = (),
                  chunksize: int = None,
                  callback: Callable = None,
                  error_callback: Callable = None) -> None:
        """
        Description:
            Refer to multiprocessing.pool.map_async.
        :return:
        """
        pass


    @abstractmethod
    def map_by_args(self, function: Callable, args_iter: Iterable[Iterable] = (), chunksize: int = None) -> None:
        """
        Description:
            Refer to multiprocessing.pool.starmap.
        :return:
        """
        pass


    @abstractmethod
    def async_map_by_args(self,
                          function: Callable,
                          args_iter: Iterable[Iterable] = (),
                          chunksize: int = None,
                          callback: Callable = None,
                          error_callback: Callable = None) -> None:
        """
        Description:
            Refer to multiprocessing.pool.starmap_async.
        :return:
        """
        pass


    @abstractmethod
    def imap(self, function: Callable, args_iter: Iterable[Iterable] = (), chunksize: int = 1) -> None:
        """
        Description:
            Refer to multiprocessing.pool.imap.
        :return:
        """
        pass


    @abstractmethod
    def imap_unordered(self, function: Callable, args_iter: Iterable[Iterable] = (), chunksize: int = 1) -> None:
        """
        Description:
            Refer to multiprocessing.pool.imap_unordered.
        :return:
        """
        pass


    @abstractmethod
    def close(self) -> None:
        """
        Description:
            Close and join pool.
        :return:
        """
        pass



class AsyncRunnableStrategy(GeneralRunnableStrategy, ABC):

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
    async def activate_workers(self, workers: Union[_OceanTasks, List[_OceanTasks]]) -> None:
        """
        Description:
            Activate multiple executors (processes, threads, etc) to run target task(s).
        :return:
        """
        pass


    @abstractmethod
    async def start_new_worker(self, target: Callable, *args, **kwargs) -> None:
        """
        Description:
            Initial and activate an executor (process, thread, etc).
        :return:
        """
        pass


    @abstractmethod
    async def close(self, workers: Union[_OceanTasks, List[_OceanTasks]]) -> None:
        """
        Description:
            Asynchronous version of method 'close'.
        :return:
        """
        pass



class Resultable(metaclass=ABCMeta):

    @abstractmethod
    def get_result(self) -> List[_OceanResult]:
        """
        Description:
            Return the result of every tasks done.
        :return:
        """
        pass


