from pyocean.framework.strategy import InitializeUtils, RunnableStrategy, Resultable
from pyocean.framework.worker import BaseTask
from pyocean.worker import OceanTask
# from pyocean.framework.features import BaseQueueType
from pyocean.api import FeatureMode
from pyocean.api.mode import RunningMode
# from pyocean.concurrent.features import MultiThreadingQueueType
from pyocean.concurrent.result import ConcurrentResult
from pyocean.exceptions import FunctionSignatureConflictError
from pyocean.concurrent.exceptions import ThreadsListIsEmptyError

from abc import abstractmethod, ABC
from typing import List, Dict, Union, Callable
from threading import Thread
from functools import wraps



class ConcurrentStrategy(RunnableStrategy, ABC):

    _Running_Mode: FeatureMode = FeatureMode.MultiThreading
    _Threads_List: List[Thread] = []
    _Threads_Running_Result: Dict[str, Dict[str, Union[object, bool]]] = {}
    _Threading_Running_Result: List = []

    def activate_workers(self, workers_list: List[Thread]) -> None:
        # # Method 1.
        for worker in workers_list:
            self.activate_worker(worker=worker)

        # # Method 2.
        # with workers_list as worker:
        #     self.activate_worker(worker=worker)


    @abstractmethod
    def activate_worker(self, worker: Thread) -> None:
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

        def __general_task() -> OceanTask:
            __otask = OceanTask(mode=RunningMode.Concurrent)
            __otask.set_function(function=function)
            __otask.set_func_args(args=args)
            __otask.set_func_kwargs(kwargs=kwargs)
            return __otask

        if args:
            __task = filter(lambda arg: isinstance(arg, BaseTask), args)
            if __task is None:
                __task = __general_task()
            __args = (__task,)
        else:
            __args = ()

        if kwargs:
            __task = kwargs.get("task", None)
            if __task is None:
                __task = __general_task()
            else:
                if not isinstance(__task, BaseTask):
                    raise FunctionSignatureConflictError
            __kwargs = {"task": __task}
        else:
            __kwargs = {}

        self._Threads_List = [Thread(target=self.target_task, args=__args, kwargs=__kwargs) for _ in range(self.workers_number)]
        return self._Threads_List


    def save_return_value(function: Callable) -> Callable:

        @wraps(function)
        def save_value_fun(self, task: BaseTask) -> None:
            self = self
            value = task.function(*task.func_args, **task.func_kwargs)
            __thread_result = {"result": value}
            self._Threading_Running_Result.append(__thread_result)

        return save_value_fun


    @save_return_value
    def target_task(self, task: BaseTask) -> None:
        task.function(self, *task.func_args, **task.func_kwargs)


    def activate_worker(self, worker: Thread) -> None:
        worker.start()


    def close(self) -> None:
        if self._Threads_List:
            for threed_index in range(self.workers_number):
                self._Threads_List[threed_index].join()
        else:
            raise ThreadsListIsEmptyError


    def get_result(self) -> List[ConcurrentResult]:
        __concurrent_result = self._result_handling()
        return __concurrent_result


    def _result_handling(self) -> List[ConcurrentResult]:
        __concurrent_results = []
        for __result in self._Threading_Running_Result:
            __concurrent_result = ConcurrentResult()
            __concurrent_result.data = __result.get("result")

            __concurrent_results.append(__concurrent_result)

        return __concurrent_results
