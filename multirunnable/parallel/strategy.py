from multirunnable.mode import FeatureMode as _FeatureMode
from multirunnable.parallel.result import ParallelResult as _ParallelResult
from multirunnable.framework.task import (
    BaseQueueTask as _BaseQueueTask,
    BasePersistenceTask as _BasePersistenceTask)
from multirunnable.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from multirunnable.framework.adapter.collection import BaseList as _BaseList
from multirunnable.framework.strategy import (
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    PoolRunnableStrategy as _PoolRunnableStrategy,
    Resultable as _Resultable)
from multirunnable.framework.result import ResultState as _ResultState

from types import FunctionType, MethodType
from typing import List, Tuple, Dict, Iterable as IterableType, Union, Callable, Optional, cast
from functools import wraps, partial as PartialFunction
from collections import Iterable
from multipledispatch import dispatch
from multiprocessing import Process, Manager
from multiprocessing.pool import Pool, AsyncResult, ApplyResult
from multiprocessing.managers import Namespace



class ParallelStrategy:

    _Strategy_Feature_Mode = _FeatureMode.Parallel
    _Manager: Manager = Manager()
    _Namespace_Object: Namespace = _Manager.Namespace()
    _Processors_Running_Result: List[Dict] = _Manager.list()
    # _Manager: Manager = None
    # _Namespace_Object: Namespace = None
    # _Processors_Running_Result: List[Dict] = None

    # def _init_namespace_obj(self) -> None:
    #     self._Manager = Manager()
    #     self._Namespace_Object = self._Manager.Namespace()


    def namespacing_obj(self, obj: object) -> object:
        setattr(self._Namespace_Object, repr(obj), obj)
        return getattr(self._Namespace_Object, repr(obj))


    @classmethod
    def save_return_value(cls, function: Callable) -> Callable:
        __self = cls

        @wraps(function)
        def save_value_fun(*args, **kwargs) -> None:
            value = function(*args, **kwargs)
            __thread_result = {"result": value}
            __self._Processors_Running_Result.append(__thread_result)

        return save_value_fun


    def result(self) -> List[_ParallelResult]:
        __parallel_result = self._result_handling()
        self._Processors_Running_Result = []
        return __parallel_result


    def _result_handling(self) -> List[_ParallelResult]:
        __parallel_results = []
        for __result in self._Processors_Running_Result:
            __parallel_result = _ParallelResult()

            __process_successful = __result.get("successful", None)
            if __process_successful is True:
                __parallel_result.state = _ResultState.SUCCESS.value
            else:
                __parallel_result.state = _ResultState.FAIL.value

            __process_result = __result.get("result", None)
            __parallel_result.data = __process_result

            __parallel_results.append(__parallel_result)

        return __parallel_results



class ProcessStrategy(ParallelStrategy, _GeneralRunnableStrategy, _Resultable):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.Parallel
    __Process_List: List[Process] = None

    def __init__(self, executors: int, persistence: _BasePersistenceTask = None):
        """
        Description:
            Converting the object to multiprocessing.manager.Namespace type object at initial state.
        :param persistence:
        """
        super().__init__(executors=executors, persistence=persistence)
        # self._init_namespace_obj()
        if persistence is not None:
            namespace_persistence = cast(_BasePersistenceTask, self.namespacing_obj(obj=persistence))
            # super().__init__(persistence=namespace_persistence)
            self._persistence = namespace_persistence
        # self._Processors_Running_Result = self._Manager.list()


    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(ProcessStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(db_conn_num=self.db_connection_pool_size)


    @dispatch((FunctionType, MethodType, PartialFunction), tuple, dict)
    def start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> Process:
        __worker = self.generate_worker(target=target, *args, **kwargs)
        self.activate_workers(__worker)
        return __worker


    @dispatch(Iterable, tuple, dict)
    def start_new_worker(self, target: List[Callable], args: Tuple = (), kwargs: Dict = {}) -> List[Process]:
        __workers = [self.generate_worker(target=__function, *args, **kwargs) for __function in target]
        self.activate_workers(__workers)
        return __workers


    def generate_worker(self, target: Callable, *args, **kwargs) -> Process:

        @wraps(target)
        @ParallelStrategy.save_return_value
        def _target_function(*_args, **_kwargs):
            result_value = target(*_args, **_kwargs)
            return result_value

        return Process(target=_target_function, args=args, kwargs=kwargs)


    @dispatch(Process)
    def activate_workers(self, workers: Process) -> None:
        workers.start()


    @dispatch(Iterable)
    def activate_workers(self, workers: List[Process]) -> None:
        for worker in workers:
            self.activate_workers(worker)


    @dispatch(Process)
    def close(self, workers: Process) -> None:
        workers.join()


    @dispatch(Iterable)
    def close(self, workers: List[Process]) -> None:
        for worker in workers:
            self.close(worker)


    def terminal(self):
        for __process in self.__Process_List:
            __process.terminate()


    def kill(self):
        for __process in self.__Process_List:
            __process.kill()


    def get_result(self) -> IterableType[object]:
        return self.result()



class ProcessPoolStrategy(ParallelStrategy, _PoolRunnableStrategy, _Resultable):

    _Processors_Pool: Pool = None
    _Processors_List: List[Union[ApplyResult, AsyncResult]] = None

    def __init__(self, pool_size: int, tasks_size: int, persistence: _BasePersistenceTask = None):
        super().__init__(pool_size=pool_size, tasks_size=tasks_size, persistence=persistence)
        # self._init_namespace_obj()
        if persistence is not None:
            namespace_persistence = cast(_BasePersistenceTask, self.namespacing_obj(obj=persistence))
            # super().__init__(persistence=namespace_persistence)
            self._persistence = namespace_persistence
        # self._Processors_Running_Result = self._Manager.list()


    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(ProcessPoolStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(db_conn_num=self.db_connection_pool_size)

        # Initialize and build the Processes Pool.
        __pool_initializer: Callable = kwargs.get("pool_initializer", None)
        __pool_initargs: IterableType = kwargs.get("pool_initargs", None)
        self._Processors_Pool = Pool(processes=self.pool_size, initializer=__pool_initializer, initargs=__pool_initargs)


    def apply(self, function: Callable, *args, **kwargs) -> None:
        __process_running_result = None

        try:
            __process_running_result = [
                self._Processors_Pool.apply(func=function, args=args, kwds=kwargs)
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
        self._Processors_List = [
            self._Processors_Pool.apply_async(func=function,
                                              args=args,
                                              kwds=kwargs,
                                              callback=callback,
                                              error_callback=error_callback)
            for _ in range(self.tasks_size)]

        for process in self._Processors_List:
            __process_running_result = process.get()
            __process_run_successful = process.successful()

            # Save Running result state and Running result value as dict
            self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def map(self, function: Callable, args_iter: IterableType = (), chunksize: int = None) -> None:
        __process_running_result = None

        try:
            __process_running_result = self._Processors_Pool.map(
                func=function, iterable=args_iter, chunksize=chunksize)
            __exception = None
            __process_run_successful = True
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result, []):
            self._result_saving(successful=__process_run_successful, result=__result)


    def async_map(self,
                  function: Callable,
                  args_iter: IterableType = (),
                  chunksize: int = None,
                  callback: Callable = None,
                  error_callback: Callable = None) -> None:
        __map_result = self._Processors_Pool.map_async(
            func=function,
            iterable=args_iter,
            chunksize=chunksize,
            callback=callback,
            error_callback=error_callback)
        __process_running_result = __map_result.get()
        __process_run_successful = __map_result.successful()

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result, []):
            self._result_saving(successful=__process_run_successful, result=__result)


    def map_by_args(self, function: Callable, args_iter: IterableType[IterableType] = (), chunksize: int = None) -> None:
        __process_running_result = None

        try:
            __process_running_result = self._Processors_Pool.starmap(
                func=function, iterable=args_iter, chunksize=chunksize)
            __exception = None
            __process_run_successful = False
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result, []):
            self._result_saving(successful=__process_run_successful, result=__result)


    def async_map_by_args(self,
                          function: Callable,
                          args_iter: IterableType[IterableType] = (),
                          chunksize: int = None,
                          callback: Callable = None,
                          error_callback: Callable = None) -> None:
        __map_result = self._Processors_Pool.starmap_async(
            func=function,
            iterable=args_iter,
            chunksize=chunksize,
            callback=callback,
            error_callback=error_callback)
        __process_running_result = __map_result.get()
        __process_run_successful = __map_result.successful()

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result, []):
            self._result_saving(successful=__process_run_successful, result=__result)


    def imap(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        __process_running_result = None

        try:
            imap_running_result = self._Processors_Pool.imap(func=function, iterable=args_iter, chunksize=chunksize)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = False
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result, []):
            self._result_saving(successful=__process_run_successful, result=__result)


    def imap_unordered(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        __process_running_result = None

        try:
            imap_running_result = self._Processors_Pool.imap_unordered(func=function,iterable=args_iter, chunksize=chunksize)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = False
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result, []):
            self._result_saving(successful=__process_run_successful, result=__result)


    def _result_saving(self, successful: bool, result: List) -> None:
        process_result = {"successful": successful, "result": result}
        # Saving value into list
        self._Processors_Running_Result.append(process_result)


    def close(self) -> None:
        self._Processors_Pool.close()
        self._Processors_Pool.join()


    def terminal(self) -> None:
        self._Processors_Pool.terminate()


    def get_result(self) -> List[_ParallelResult]:
        return self.result()


