from pyocean.framework import OceanResult as _OceanResult
from pyocean.framework.task import (
    BaseQueueTask as _BaseQueueTask,
    BasePersistenceTask as _BasePersistenceTask)
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.strategy import (
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    PoolRunnableStrategy as _PoolRunnableStrategy,
    Resultable as _Resultable)
from pyocean.mode import FeatureMode as _FeatureMode
from pyocean.concurrent.result import ConcurrentResult as _ConcurrentResult

from typing import List, Dict, Callable, Iterable as IterableType, Optional, Union, Tuple, cast
from types import MethodType
from collections import Iterable
from multipledispatch import dispatch
from functools import wraps
from multiprocessing.pool import ThreadPool
from multiprocessing.pool import AsyncResult, ApplyResult
from threading import Thread

from pyocean.types import OceanTasks as _OceanTasks


class ConcurrentStrategy:

    _Strategy_Feature_Mode = _FeatureMode.Concurrent
    _Threading_Running_Result: List = []
    _Thread_Running_Result: List[Dict[str, Union[AsyncResult, bool]]] = []

    @classmethod
    def save_return_value(cls, function: Callable) -> Callable:
        __self = cls

        @wraps(function)
        def save_value_fun(*args, **kwargs) -> None:
            value = function(*args, **kwargs)
            __thread_result = {"result": value}
            __self._Threading_Running_Result.append(__thread_result)

        return save_value_fun


    def result(self) -> List[_ConcurrentResult]:
        __concurrent_result = self._result_handling()
        return __concurrent_result


    def _result_handling(self) -> List[_ConcurrentResult]:
        __concurrent_results = []
        for __result in self._Thread_Running_Result:
            __concurrent_result = _ConcurrentResult()
            __concurrent_result.data = __result.get("result")

            __concurrent_results.append(__concurrent_result)

        return __concurrent_results



class ThreadStrategy(_GeneralRunnableStrategy, ConcurrentStrategy, _Resultable):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.Concurrent
    __Thread_List: List[Thread] = None

    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(ThreadStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(db_conn_num=self.db_connection_pool_size)


    @dispatch(MethodType, tuple, dict)
    def start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> Thread:
        __worker = self.generate_worker(target=target, *args, **kwargs)
        self.activate_workers(__worker)
        return __worker


    @dispatch(Iterable, tuple, dict)
    def start_new_worker(self, target: List[Callable], args: Tuple = (), kwargs: Dict = {}) -> List[Thread]:
        __workers = [self.generate_worker(target=__function, *args, **kwargs) for __function in target]
        self.activate_workers(__workers)
        return __workers


    def generate_worker(self, target: Callable, *args, **kwargs) -> _OceanTasks:
        return Thread(target=target, args=args, kwargs=kwargs)


    @dispatch(Thread)
    def activate_workers(self, workers: Thread) -> None:
        workers.start()


    @dispatch(Iterable)
    def activate_workers(self, workers: List[Thread]) -> None:
        for worker in workers:
            self.activate_workers(worker)


    @dispatch(Thread)
    def close(self, workers: Thread) -> None:
        workers.join()


    @dispatch(Iterable)
    def close(self, workers: List[Thread]) -> None:
        for worker in workers:
            self.close(worker)


    def kill(self) -> None:
        pass


    def terminal(self) -> None:
        pass


    def get_result(self) -> List[_OceanResult]:
        pass



class ThreadPoolStrategy(_PoolRunnableStrategy, ConcurrentStrategy, _Resultable):

    _Thread_Pool: ThreadPool = None
    _Thread_List: List[Union[ApplyResult, AsyncResult]] = None

    def __init__(self, pool_size: int, tasks_size: int, persistence: _BasePersistenceTask = None):
        super().__init__(pool_size=pool_size, tasks_size=tasks_size, persistence=persistence)
        # self._init_namespace_obj()
        # if persistence is not None:
        #     namespace_persistence = cast(_BasePersistenceTask, self.namespacing_obj(obj=persistence))
        #     # super().__init__(persistence=namespace_persistence)
        #     self._persistence = namespace_persistence
        # self._Processors_Running_Result = self._Manager.list()


    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(ThreadPoolStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(db_conn_num=self.db_connection_pool_size)

        # Initialize and build the Processes Pool.
        __pool_initializer: Callable = kwargs.get("pool_initializer", None)
        __pool_initargs: IterableType = kwargs.get("pool_initargs", None)
        self._Thread_Pool = ThreadPool(processes=self.pool_size, initializer=__pool_initializer, initargs=__pool_initargs)


    def apply(self, function: Callable, *args, **kwargs) -> None:
        __process_running_result = None

        try:
            __process_running_result = [
                self._Thread_Pool.apply(func=function, args=args, kwds=kwargs)
                for _ in range(self.tasks_size)]
            __exception = None
            __process_run_successful = True
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def async_apply(self,
                    function: Callable,
                    args: Tuple = (),
                    kwargs: Dict = {},
                    callback: Callable = None,
                    error_callback: Callable = None) -> None:
        self._Thread_List = [
            self._Thread_Pool.apply_async(func=function,
                                          args=args,
                                          kwds=kwargs,
                                          callback=callback,
                                          error_callback=error_callback)
            for _ in range(self.tasks_size)]

        for process in self._Thread_List:
            __process_running_result = process.get()
            __process_run_successful = process.successful()

            # Save Running result state and Running result value as dict
            self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def map(self, function: Callable, args_iter: IterableType = (), chunksize: int = None) -> None:
        __process_running_result = None

        try:
            __process_running_result = self._Thread_Pool.map(
                func=function, iterable=args_iter, chunksize=chunksize)
            __exception = None
            __process_run_successful = True
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def async_map(self,
                  function: Callable,
                  args_iter: IterableType = (),
                  chunksize: int = None,
                  callback: Callable = None,
                  error_callback: Callable = None) -> None:
        __map_result = self._Thread_Pool.map_async(
            func=function,
            iterable=args_iter,
            chunksize=chunksize,
            callback=callback,
            error_callback=error_callback)
        __process_running_result = __map_result.get()
        __process_run_successful = __map_result.successful()

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def map_by_args(self, function: Callable, args_iter: IterableType[IterableType] = (), chunksize: int = None) -> None:
        __process_running_result = None

        try:
            __process_running_result = self._Thread_Pool.starmap(
                func=function, iterable=args_iter, chunksize=chunksize)
            __exception = None
            __process_run_successful = False
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def async_map_by_args(self,
                          function: Callable,
                          args_iter: IterableType[IterableType] = (),
                          chunksize: int = None,
                          callback: Callable = None,
                          error_callback: Callable = None) -> None:
        __map_result = self._Thread_Pool.starmap_async(
            func=function,
            iterable=args_iter,
            chunksize=chunksize,
            callback=callback,
            error_callback=error_callback)
        __process_running_result = __map_result.get()
        __process_run_successful = __map_result.successful()

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def imap_by_args(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        __process_running_result = None

        try:
            imap_running_result = self._Thread_Pool.imap(func=function, iterable=args_iter, chunksize=chunksize)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = False
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def imap_unordered_by_args(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        __process_running_result = None

        try:
            imap_running_result = self._Thread_Pool.imap_unordered(func=function, iterable=args_iter, chunksize=chunksize)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = False
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def _result_saving(self, successful: bool, result: List):
        process_result = {"successful": successful, "result": result}
        # Saving value into list
        self._Thread_Running_Result.append(process_result)


    def close(self) -> None:
        self._Thread_Pool.close()
        self._Thread_Pool.join()


    def terminal(self) -> None:
        self._Thread_Pool.terminate()


    def get_result(self) -> List[_ConcurrentResult]:
        return self.result()

