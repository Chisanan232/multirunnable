from pyocean.framework.task import BaseTask as _BaseTask, BaseQueueTask as _BaseQueueTask
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.collection import BaseList as _BaseList
from pyocean.framework.strategy import RunnableStrategy as _RunnableStrategy, Resultable as _Resultable
from pyocean.mode import RunningMode as _RunningMode, FeatureMode as _FeatureMode
from pyocean.task import OceanTask as _OceanTask
from pyocean.concurrent.result import ConcurrentResult as _ConcurrentResult
from pyocean.exceptions import FunctionSignatureConflictError as _FunctionSignatureConflictError
from pyocean.concurrent.exceptions import ThreadsListIsEmptyError as _ThreadsListIsEmptyError

from abc import abstractmethod, ABC
from typing import List, Dict, Callable, Optional, Union
from functools import wraps
from threading import Thread



class ConcurrentStrategy(_RunnableStrategy, ABC):

    _Strategy_Feature_Mode = _FeatureMode.Parallel
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


    @staticmethod
    def save_return_value(function: Callable) -> Callable:

        @wraps(function)
        def save_value_fun(self, task: _BaseTask) -> None:
            self = self
            value = task.function(*task.func_args, **task.func_kwargs)
            __thread_result = {"result": value}
            self._Threading_Running_Result.append(__thread_result)

        return save_value_fun



class MultiThreadingStrategy(ConcurrentStrategy, _Resultable):

    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(MultiThreadingStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(db_conn_num=self.db_connection_number)


    def build_workers(self, function: Callable, *args, **kwargs) -> List[Thread]:

        def __general_task() -> _OceanTask:
            __otask = _OceanTask(mode=_RunningMode.Concurrent)
            __otask.set_function(function=function)
            __otask.set_func_args(args=args)
            __otask.set_func_kwargs(kwargs=kwargs)
            return __otask

        if args:
            __task = filter(lambda arg: isinstance(arg, _BaseTask), args)
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
                if not isinstance(__task, _BaseTask):
                    raise _FunctionSignatureConflictError
            __kwargs = {"task": __task}
        else:
            __kwargs = {}

        self._Threads_List = [Thread(target=self.target_task, args=__args, kwargs=__kwargs) for _ in range(self.workers_number)]
        return self._Threads_List


    @ConcurrentStrategy.save_return_value
    def target_task(self, task: _BaseTask) -> None:
        task.function(self, *task.func_args, **task.func_kwargs)


    def activate_worker(self, worker: Thread) -> None:
        worker.start()


    def close(self) -> None:
        if self._Threads_List:
            for threed_index in range(self.workers_number):
                self._Threads_List[threed_index].join()
        else:
            raise _ThreadsListIsEmptyError


    def get_result(self) -> List[_ConcurrentResult]:
        __concurrent_result = self._result_handling()
        return __concurrent_result


    def _result_handling(self) -> List[_ConcurrentResult]:
        __concurrent_results = []
        for __result in self._Threading_Running_Result:
            __concurrent_result = _ConcurrentResult()
            __concurrent_result.data = __result.get("result")

            __concurrent_results.append(__concurrent_result)

        return __concurrent_results
