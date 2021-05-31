from pyocean.framework.strategy import InitializeUtils, RunnableStrategy, Resultable
from pyocean.framework.features import BaseQueueType
from pyocean.api import RunningMode
from pyocean.api.types import OceanTasks
from pyocean.parallel.features import MultiProcessingQueueType
from pyocean.persistence import OceanPersistence

from abc import abstractmethod
from multiprocessing import Pool, Manager
from multiprocessing.managers import Namespace
from multiprocessing.pool import Pool, AsyncResult, ApplyResult
from typing import List, Tuple, Dict, Iterable, Union, Callable, cast
import re

from deprecated.sphinx import deprecated



class ParallelStrategy(RunnableStrategy):

    _Running_Mode: RunningMode = RunningMode.MultiProcessing
    _Manager: Manager = None
    _Namespace_Object: Namespace = None
    _Processors_Pool: Pool = None
    _Processors_Running_Result: List[Dict[str, Union[AsyncResult, bool]]] = {}

    def __init__(self, workers_num: int, persistence_strategy: OceanPersistence = None, **kwargs):
        """
        Description:
            Converting the object to multiprocessing.manager.Namespace type object at initial state.
        :param workers_num:
        :param db_connection_pool_size:
        :param persistence_strategy:
        """
        super().__init__(workers_num, persistence_strategy, **kwargs)
        self.__init_namespace_obj()
        if persistence_strategy is not None:
            namespace_persistence_strategy = cast(OceanPersistence, self.__namespacing_instance(instance=persistence_strategy))
            super().__init__(persistence_strategy=namespace_persistence_strategy,
                             workers_num=workers_num,
                             db_connection_pool_size=self.db_connection_instances_number)
        self._Processors_Running_Result = self._Manager.list()


    def __init_namespace_obj(self) -> None:
        self._Manager = Manager()
        self._Namespace_Object = self._Manager.Namespace()


    def activate_multi_workers(self, workers_list: List[OceanTasks]) -> None:
        # # Method 1.
        for worker in workers_list:
            self.activate_worker(worker=worker)

        # # Method 2.
        # with workers_list as worker:
        #     self.activate_worker(worker=worker)


    @abstractmethod
    def activate_worker(self, worker: OceanTasks) -> None:
        """
        Description:
            Each one thread or process running task implementation.
        :param worker:
        :return:
        """
        pass


    def __namespacing_instance(self, instance: object) -> object:
        setattr(self._Namespace_Object, repr(instance), instance)
        return getattr(self._Namespace_Object, repr(instance))


    @deprecated(version="0.1", reason="The code looks be useless method currently.")
    @abstractmethod
    def namespacilize_object(self, objects: Iterable[object]) -> Namespace:
        """
        Description:
              Set the object which be shared to use between multiple processes as MultiProcessing NameSpace object to
              reach shared object requirement.
        :param objects:
        :return:
        """
        pass



class MultiProcessingStrategy(ParallelStrategy, Resultable):

    def init_multi_working(self, tasks: Iterable = [], queue_type: BaseQueueType = MultiProcessingQueueType.Queue, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # Initialize and assign task queue object.
        if tasks:
            __init_utils.initialize_queue(tasks=tasks, qtype=queue_type)
        # Initialize parameter and object with different scenario.
        if self._persistence_strategy is not None:
            __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_instances_number)

        # Initialize and build the Processes Pool.
        __pool_initializer: Callable = kwargs.get("pool_initializer", None)
        __pool_initargs: Iterable = kwargs.get("pool_initargs", None)
        self._Processors_Pool = Pool(processes=self.workers_number, initializer=__pool_initializer, initargs=__pool_initargs)


    def namespacilize_object(self, objects: Iterable[Callable]) -> Namespace:
        """
        Note:
            It's possible that occur some unexpected issue if the entry value isn't class instance.
        Question:
            Should fix the issue about it cannot assign object instance correctly.
        """

        for obj in objects:
            if not isinstance(obj, Callable):
                raise TypeError("The object element of List isn't Callable.")

        __common_objects = self._Manager.Namespace()
        instance_dict = {}
        for obj in objects:
            __instance_name = self.__parse_class_name(object_char=obj)
            instance_dict[__instance_name] = obj
            # __common_objects.Common_Objects_Dict.common_objects[__instance_name] = obj

        __common_objects.Common_Objects_Dict = instance_dict
        return __common_objects


    def __parse_class_name(self, object_char: object) -> str:
        """
        Description:
            Parse the object package and class name.
        :param object_char:
        :return:
        """

        if re.search(r"<class \'\w{0,64}\.\w{0,64}\'>", str(object_char), re.IGNORECASE) is None:
            raise Exception("Cannot parse the class instance string")
        return str(object_char).split(".")[-1].split("'>")[0]


    def build_multi_workers(self,
                            function: Callable,
                            args: Tuple = (),
                            kwargs: Dict = {},
                            callback: Callable = None,
                            error_callback: Callable = None) -> List[Union[AsyncResult, ApplyResult]]:
        return [self._Processors_Pool.apply_async(func=function,
                                                  args=args,
                                                  kwds=kwargs,
                                                  callback=callback,
                                                  error_callback=error_callback)
                for _ in range(self.workers_number)]
        # elif kwargs:
        #     return [self._Processors_Pool.apply_async(func=function, kwds=kwargs, callback=callaback, error_callback=error_callback)
        #             for _ in range(self.threads_number)]


    def activate_worker(self, worker: Union[AsyncResult, ApplyResult]) -> None:
        __process_running_result = worker.get()
        __process_run_successful = worker.successful()

        # Save Running result state and Running result value as dict
        process_result = {"successful": __process_run_successful, "result": __process_running_result}
        # Saving value into list
        self._Processors_Running_Result.append(process_result)


    def end_multi_working(self) -> None:
        self._Processors_Pool.close()
        self._Processors_Pool.join()


    def get_multi_working_result(self) -> Iterable[object]:
        return self._Processors_Running_Result

