from pyocean.framework.strategy import InitializeUtils, RunnableStrategy, Resultable
# from pyocean.framework.features import BaseQueueType
# from pyocean.worker import OceanTask
from pyocean.api import FeatureMode
# from pyocean.types import OceanTasks
# from pyocean.parallel.features import MultiProcessingQueueType
from pyocean.persistence import OceanPersistence

from abc import abstractmethod
from multiprocessing import Pool, Manager
from multiprocessing.managers import Namespace
from multiprocessing.pool import Pool, AsyncResult, ApplyResult
from typing import List, Dict, Iterable, Union, Callable, cast



class ParallelStrategy(RunnableStrategy):

    _Running_Mode: FeatureMode = FeatureMode.MultiProcessing
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
            namespace_persistence_strategy = cast(OceanPersistence, self.namespacing_obj(obj=persistence_strategy))
            super().__init__(persistence_strategy=namespace_persistence_strategy,
                             workers_num=workers_num,
                             db_connection_pool_size=self.db_connection_number)
        self._Processors_Running_Result = self._Manager.list()


    def __init_namespace_obj(self) -> None:
        self._Manager = Manager()
        self._Namespace_Object = self._Manager.Namespace()


    def activate_workers(self, workers_list: List[Union[ApplyResult, AsyncResult]]) -> None:
        # # Method 1.
        for worker in workers_list:
            self.activate_worker(worker=worker)

        # # Method 2.
        # with workers_list as worker:
        #     self.activate_worker(worker=worker)


    @abstractmethod
    def activate_worker(self, worker: Union[ApplyResult, AsyncResult]) -> None:
        """
        Description:
            Each one thread or process running task implementation.
        :param worker:
        :return:
        """
        pass


    def namespacing_obj(self, obj: object) -> object:
        setattr(self._Namespace_Object, repr(obj), obj)
        return getattr(self._Namespace_Object, repr(obj))



class MultiProcessingStrategy(ParallelStrategy, Resultable):

    def initialization(self, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # # Initialize and assign task queue object.
        # if tasks:
        #     __init_utils.initialize_queue(tasks=tasks, qtype=queue_type)
        # Initialize parameter and object with different scenario.
        if self._persistence_strategy is not None:
            __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_number)

        # Initialize and build the Processes Pool.
        __pool_initializer: Callable = kwargs.get("pool_initializer", None)
        __pool_initargs: Iterable = kwargs.get("pool_initargs", None)
        self._Processors_Pool = Pool(processes=self.workers_number, initializer=__pool_initializer, initargs=__pool_initargs)


    def build_workers(self,
                      function: Callable,
                      callback: Callable = None,
                      error_callback: Callable = None,
                      *args, **kwargs) -> List[Union[AsyncResult, ApplyResult]]:
        return [self._Processors_Pool.apply_async(func=function,
                                                  args=args,
                                                  kwds=kwargs,
                                                  callback=callback,
                                                  error_callback=error_callback)
                for _ in range(self.workers_number)]


    def activate_worker(self, worker: Union[AsyncResult, ApplyResult]) -> None:
        __process_running_result = worker.get()
        __process_run_successful = worker.successful()

        # Save Running result state and Running result value as dict
        process_result = {"successful": __process_run_successful, "result": __process_running_result}
        # Saving value into list
        self._Processors_Running_Result.append(process_result)


    def close(self) -> None:
        self._Processors_Pool.close()
        self._Processors_Pool.join()


    def get_result(self) -> Iterable[object]:
        return self._Processors_Running_Result

