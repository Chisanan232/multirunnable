from pyocean.framework.strategy import InitializeUtils, RunnableStrategy, Resultable
from pyocean.framework.features import BaseQueueType
from pyocean.api import FeatureMode
from pyocean.types import OceanTasks
from pyocean.concurrent.features import MultiThreadingQueueType
from pyocean.concurrent.exceptions import ThreadsListIsEmptyError

from abc import abstractmethod, ABC
from typing import List, Tuple, Dict, Iterable, Union, Callable, Any
from threading import Thread



class ConcurrentStrategy(RunnableStrategy, ABC):

    _Running_Mode: FeatureMode = FeatureMode.MultiThreading
    _Threads_List: List[Thread] = []
    _Threads_Running_Result: Dict[str, Dict[str, Union[object, bool]]] = {}
    _Threading_Running_Result: List = []

    def activate_workers(self, workers_list: List[OceanTasks]) -> None:
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



class MultiThreadingStrategy(ConcurrentStrategy, Resultable):

    def initialization(self, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # # Initialize and assign task queue object.
        # if tasks:
        #     __init_utils.initialize_queue(tasks=tasks, qtype=queue_type)
        # Initialize parameter and object with different scenario.
        if self._persistence_strategy is not None:
            __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_number)


    def build_workers(self, function: Callable, *args, **kwargs) -> List[Thread]:
        self._Threads_List = [Thread(target=function, args=args, kwargs=kwargs) for _ in range(self.workers_number)]
        return self._Threads_List


    def build_workers_test(self, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> List[Thread]:
        if args:
            args = (function,) + args
        if kwargs:
            kwargs["function"] = function
        self._Threads_List = [Thread(target=self.target_function, args=args, kwargs=kwargs) for _ in range(self.workers_number)]
        return self._Threads_List


    def record_result(function: Callable) -> Callable:

        def decorator(self, *args, **kwargs) -> None:
            print(f"record_result.args: {args}")
            print(f"record_result.kwargs: {kwargs}")
            value = function(self, *args, **kwargs)
            self._Threading_Running_Result.append(value)

        return decorator


    @record_result
    def target_function(self, function: Callable, *args, **kwargs) -> Union[None, Any]:
        value = function(*args, **kwargs)
        return value


    def activate_worker(self, worker: OceanTasks) -> None:
        worker.start()


    def close(self) -> None:
        if self._Threads_List:
            for threed_index in range(self.workers_number):
                self._Threads_List[threed_index].join()
        else:
            raise ThreadsListIsEmptyError


    def get_result(self) -> Iterable[object]:
        return self._Threading_Running_Result
