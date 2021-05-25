from pyocean.framework.strategy import InitializeUtils, RunnableStrategy
from pyocean.api import RunningMode
from pyocean.concurrent.features import MultiThreadingQueueType

from abc import ABCMeta, abstractmethod, ABC
from typing import List, Tuple, Dict, Iterable, Union, Callable
from multiprocessing.pool import ApplyResult
from threading import Thread



class ConcurrentStrategy(RunnableStrategy, ABC):

    _Running_Mode: RunningMode = RunningMode.MultiThreading
    _Threads_List: List[Thread] = None
    _Threads_Running_Result: Dict[str, Dict[str, Union[object, bool]]] = {}



class MultiThreadingStrategy(ConcurrentStrategy):

    def init_multi_working(self, tasks: Iterable, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # Initialize and assign task queue object.
        __init_utils.initialize_queue(tasks=tasks, qtype=MultiThreadingQueueType.Queue)
        # Initialize parameter and object with different scenario.
        __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_instances_number)


    def build_multi_workers(self, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> List[Union[Thread, ApplyResult]]:
        print("function: ", function)
        print("args: ", args)
        print("kwargs: ", kwargs)
        self._Threads_List = [Thread(target=function, args=args, kwargs=kwargs) for _ in range(self.threads_number)]
        return self._Threads_List


    def activate_worker(self, worker: Union[Thread, ApplyResult]) -> None:
        print("[DEBUG] start to run thread ...")
        worker.start()
        print("[DEBUG] has activate to run.")


    def end_multi_working(self) -> None:
        if isinstance(self._Threads_List, List) and isinstance(self._Threads_List[0], Thread):
            for threed_index in range(self.threads_number):
                self._Threads_List[threed_index].join()
        else:
            raise
