from pyocean.framework.task import BaseTask as _BaseTask, BaseQueueTask as _BaseQueueTask
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.strategy import (
    RunnableStrategy as _RunnableStrategy,
    BaseMapStrategy as _BaseMapStrategy,
    Resultable as _Resultable)
from pyocean.mode import RunningMode as _RunningMode, FeatureMode as _FeatureMode
from pyocean.task import OceanTask as _OceanTask
from pyocean.concurrent.result import ConcurrentResult as _ConcurrentResult
from pyocean.exceptions import FunctionSignatureConflictError as _FunctionSignatureConflictError
from pyocean.concurrent.exceptions import ThreadsListIsEmptyError as _ThreadsListIsEmptyError

from abc import abstractmethod, ABC
from typing import List, Dict, Callable, Iterable as IterableType, Optional, Union, Tuple
from types import MethodType
from collections import Iterable
from multipledispatch import dispatch
from functools import wraps
from threading import Thread



class ConcurrentStrategy(_RunnableStrategy, ABC):

    _Strategy_Feature_Mode = _FeatureMode.Concurrent
    _Threads_List: List[Thread] = []
    _Threads_Running_Result: Dict[str, Dict[str, Union[object, bool]]] = {}
    _Threading_Running_Result: List = []

    def activate_workers(self) -> None:
        for worker in self._Threads_List:
            self.activate_worker(worker=worker)


    @abstractmethod
    def activate_worker(self, worker: Thread) -> None:
        """
        Description:
            Each one thread or process running task implementation.
        :param worker:
        :return:
        """
        pass


    @classmethod
    def save_return_value(cls, function: Callable) -> Callable:
        __self = cls

        @wraps(function)
        def save_value_fun(*args, **kwargs) -> None:
            value = function(*args, **kwargs)
            __thread_result = {"result": value}
            __self._Threading_Running_Result.append(__thread_result)

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


    def build_workers(self, function: Callable, *args, **kwargs) -> None:

        @ConcurrentStrategy.save_return_value
        def target_task(*args, **kwargs) -> None:
            value = function(*args, **kwargs)
            return value

        self._Threads_List = [Thread(target=target_task, args=args, kwargs=kwargs) for _ in range(self.workers_number)]


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



class MultiThreadingMapStrategy(_BaseMapStrategy, _Resultable):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.Concurrent

    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(MultiThreadingMapStrategy, self).initialization(
            queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        # if self._persistence_strategy is not None:
        #     self._persistence_strategy.initialize(db_conn_num=self.db_connection_number)


    def generate_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> Thread:
        return Thread(target=target, args=args, kwargs=kwargs)


    @dispatch(Thread)
    def activate_worker(self, workers: Thread) -> None:
        workers.start()


    @dispatch(Iterable)
    def activate_worker(self, workers: List[Thread]) -> None:
        for worker in workers:
            self.activate_worker(worker)


    @dispatch(Thread)
    def close_worker(self, workers: Thread) -> None:
        workers.join()


    @dispatch(Iterable)
    def close_worker(self, workers: List[Thread]) -> None:
        for worker in workers:
            self.close_worker(worker)


    @dispatch(MethodType, tuple, dict)
    def start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> Thread:
        __worker = self.generate_worker(target=target, *args, **kwargs)
        self.activate_worker(__worker)
        return __worker


    @dispatch(Iterable, tuple, dict)
    def start_new_worker(self, target: List[Callable], args: Tuple = (), kwargs: Dict = {}) -> List[Thread]:
        __workers = [self.generate_worker(target=__function, *args, **kwargs) for __function in target]
        self.activate_worker(__workers)
        return __workers


    def get_result(self) -> IterableType[object]:
        pass

