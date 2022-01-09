from abc import ABC
from os import getpid
from types import FunctionType, MethodType
from typing import List, Dict, Callable, Iterable as IterableType, Optional, Union, Tuple, cast
from functools import wraps, partial as PartialFunction
from collections.abc import Iterable
from multipledispatch import dispatch
from threading import Thread, current_thread
from multiprocessing.pool import ThreadPool
from multiprocessing.pool import AsyncResult, ApplyResult

from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from multirunnable.mode import FeatureMode as _FeatureMode
from multirunnable.types import MRTasks as _MRTasks
from multirunnable.concurrent.result import ConcurrentResult as _ConcurrentResult, ThreadPoolResult as _ThreadPoolResult
from multirunnable.framework import (
    MRResult as _MRResult,
    BaseQueueTask as _BaseQueueTask,
    BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory,
    BaseList as _BaseList,
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    PoolRunnableStrategy as _PoolRunnableStrategy,
    Resultable as _Resultable,
    ResultState as _ResultState
)



class ConcurrentStrategy(_Resultable, ABC):

    _Strategy_Feature_Mode = _FeatureMode.Concurrent
    _Thread_Running_Result: List[Dict[str, Union[AsyncResult, bool]]] = []

    @classmethod
    def save_return_value(cls, function: Callable) -> Callable:
        __self = cls

        @wraps(function)
        def save_value_fun(*args, **kwargs) -> None:
            _current_thread = current_thread()

            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) >= (3, 8):
                _thread_result = {
                    "pid": getpid(),
                    "name": _current_thread.name,
                    "ident": _current_thread.ident,
                    "native_id": _current_thread.native_id
                }
            else:
                _thread_result = {
                    "pid": getpid(),
                    "name": _current_thread.name,
                    "ident": _current_thread.ident
                }

            try:
                value = function(*args, **kwargs)
            except Exception as e:
                _thread_result.update({
                    "successful": False,
                    "exception": e
                })
            else:
                _thread_result.update({
                    "result": value,
                    "successful": True
                })
            finally:
                __self._Thread_Running_Result.append(_thread_result)

        return save_value_fun


    def result(self) -> List[_ConcurrentResult]:
        __concurrent_result = self._saving_process()
        self.reset_result()
        return __concurrent_result


    def reset_result(self):
        self._Thread_Running_Result[:] = []



class ThreadStrategy(ConcurrentStrategy, _GeneralRunnableStrategy):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.Concurrent
    __Thread_List: List[Thread] = None

    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(ThreadStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)


    @dispatch((FunctionType, MethodType, PartialFunction), args=tuple, kwargs=dict)
    def _start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> Thread:
        __worker = self.generate_worker(target, *args, **kwargs)
        self.activate_workers(__worker)
        return __worker


    @dispatch(Iterable, args=tuple, kwargs=dict)
    def _start_new_worker(self, target: List[Callable], args: Tuple = (), kwargs: Dict = {}) -> List[Thread]:
        __workers = [self.generate_worker(__function, *args, **kwargs) for __function in target]
        self.activate_workers(__workers)
        return __workers


    def generate_worker(self, target: Callable, *args, **kwargs) -> _MRTasks:

        @wraps(target)
        @ConcurrentStrategy.save_return_value
        def _target_function(*_args, **_kwargs):
            result_value = target(*_args, **_kwargs)
            return result_value

        return Thread(target=_target_function, args=args, kwargs=kwargs)


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


    def get_result(self) -> List[_MRResult]:
        return self.result()


    def _saving_process(self) -> List[_ConcurrentResult]:
        __concurrent_results = []
        for __result in self._Thread_Running_Result:
            _cresult = _ConcurrentResult()

            # # # # Save some basic info of Process
            _cresult.pid = __result["pid"]
            _cresult.worker_name = __result["name"]
            _cresult.worker_ident = __result["ident"]
            if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION >= 8:
                _cresult.native_id = __result["native_id"]

            # # # # Save state of process
            __concurrent_successful = __result.get("successful", None)
            if __concurrent_successful is True:
                _cresult.state = _ResultState.SUCCESS.value
            else:
                _cresult.state = _ResultState.FAIL.value

            # # # # Save running result of process
            _cresult.data = __result.get("result", None)
            _cresult.exception = __result.get("exception", None)

            __concurrent_results.append(_cresult)

        return __concurrent_results



class ThreadPoolStrategy(ConcurrentStrategy, _PoolRunnableStrategy, _Resultable):

    _Thread_Pool: ThreadPool = None
    _Thread_List: List[Union[ApplyResult, AsyncResult]] = None

    def __init__(self, pool_size: int, tasks_size: int):
        super().__init__(pool_size=pool_size, tasks_size=tasks_size)


    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(ThreadPoolStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # Initialize and build the Processes Pool.
        __pool_initializer: Callable = kwargs.get("pool_initializer", None)
        __pool_initargs: IterableType = kwargs.get("pool_initargs", None)
        self._Thread_Pool = ThreadPool(processes=self.pool_size, initializer=__pool_initializer, initargs=__pool_initargs)


    def apply(self, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> None:
        self.reset_result()
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
        self._result_saving(successful=__process_run_successful, result=__process_running_result, exception=None)


    def async_apply(self,
                    function: Callable,
                    args: Tuple = (),
                    kwargs: Dict = {},
                    callback: Callable = None,
                    error_callback: Callable = None) -> None:
        self.reset_result()
        self._Thread_List = [
            self._Thread_Pool.apply_async(func=function,
                                          args=args,
                                          kwds=kwargs,
                                          callback=callback,
                                          error_callback=error_callback)
            for _ in range(self.tasks_size)]

        for process in self._Thread_List:
            _process_running_result = None
            _process_run_successful = None
            _exception = None

            try:
                _process_running_result = process.get()
                _process_run_successful = process.successful()
            except Exception as e:
                _exception = e
                _process_run_successful = False

            # Save Running result state and Running result value as dict
            self._result_saving(successful=_process_run_successful, result=_process_running_result, exception=_exception)


    def map(self, function: Callable, args_iter: IterableType = (), chunksize: int = None) -> None:
        self.reset_result()
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
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=None)


    def async_map(self,
                  function: Callable,
                  args_iter: IterableType = (),
                  chunksize: int = None,
                  callback: Callable = None,
                  error_callback: Callable = None) -> None:
        self.reset_result()
        __map_result = self._Thread_Pool.map_async(
            func=function,
            iterable=args_iter,
            chunksize=chunksize,
            callback=callback,
            error_callback=error_callback)
        __process_running_result = __map_result.get()
        __process_run_successful = __map_result.successful()

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=None)


    def map_by_args(self, function: Callable, args_iter: IterableType[IterableType] = (), chunksize: int = None) -> None:
        self.reset_result()
        __process_running_result = None

        try:
            __process_running_result = self._Thread_Pool.starmap(
                func=function, iterable=args_iter, chunksize=chunksize)
            __exception = None
            __process_run_successful = True
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=None)


    def async_map_by_args(self,
                          function: Callable,
                          args_iter: IterableType[IterableType] = (),
                          chunksize: int = None,
                          callback: Callable = None,
                          error_callback: Callable = None) -> None:
        self.reset_result()
        __map_result = self._Thread_Pool.starmap_async(
            func=function,
            iterable=args_iter,
            chunksize=chunksize,
            callback=callback,
            error_callback=error_callback)
        __process_running_result = __map_result.get()
        __process_run_successful = __map_result.successful()

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=None)


    def imap(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        self.reset_result()
        __process_running_result = None

        try:
            imap_running_result = self._Thread_Pool.imap(func=function, iterable=args_iter, chunksize=chunksize)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = True
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=None)


    def imap_unordered(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        self.reset_result()
        __process_running_result = None

        try:
            imap_running_result = self._Thread_Pool.imap_unordered(func=function, iterable=args_iter, chunksize=chunksize)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = True
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=None)


    def _result_saving(self, successful: bool, result: List, exception: Exception) -> None:
        _thread_result = {"successful": successful, "result": result, "exception": exception}
        # Saving value into list
        self._Thread_Running_Result.append(_thread_result)


    def close(self) -> None:
        self._Thread_Pool.close()
        self._Thread_Pool.join()


    def terminal(self) -> None:
        self._Thread_Pool.terminate()


    def get_result(self) -> List[_ConcurrentResult]:
        return self.result()


    def _saving_process(self) -> List[_ThreadPoolResult]:
        _pool_results = []
        for __result in self._Thread_Running_Result:
            _pool_result = _ThreadPoolResult()
            _pool_result.is_successful = __result["successful"]
            _pool_result.data = __result["result"]
            _pool_results.append(_pool_result)
        return _pool_results

