from abc import ABC
from os import getpid, getppid
from types import FunctionType, MethodType
from typing import List, Tuple, Dict, Iterable as IterableType, Union, Callable, Optional, cast
from functools import wraps, partial as PartialFunction
from collections.abc import Iterable
from multipledispatch import dispatch
from multiprocessing import Process, current_process
from multiprocessing.pool import Pool, AsyncResult, ApplyResult

from multirunnable.mode import FeatureMode as _FeatureMode
from multirunnable.parallel.result import ParallelResult as _ParallelResult, ProcessPoolResult as _ProcessPoolResult
from multirunnable.parallel.share import Global_Manager, activate_manager_server
from multirunnable.framework import (
    BaseList as _BaseList,
    BaseQueueTask as _BaseQueueTask,
    BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory,
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    PoolRunnableStrategy as _PoolRunnableStrategy,
    Resultable as _Resultable,
    ResultState as _ResultState
)



class ParallelStrategy(_Resultable, ABC):

    _Strategy_Feature_Mode = _FeatureMode.Parallel
    _Processors_Running_Result: List[Dict] = Global_Manager.list()


    @classmethod
    def save_return_value(cls, function: Callable) -> Callable:
        __self = cls

        @wraps(function)
        def save_value_fun(*args, **kwargs) -> None:
            _current_process = current_process()

            _process_result = {
                "ppid": getppid(),
                "pid": getpid(),
                "name": _current_process.name,
                "ident": _current_process.ident
            }

            try:
                value = function(*args, **kwargs)
            except Exception as e:
                _process_result.update({
                    "successful": False,
                    "exception": e,
                    "exitcode": _current_process.exitcode
                })
            else:
                _process_result.update({
                    "result": value,
                    "successful": True,
                    "exitcode": _current_process.exitcode
                })
            finally:
                __self._Processors_Running_Result.append(_process_result)

        return save_value_fun


    def result(self) -> List[Union[_ParallelResult, _ProcessPoolResult]]:
        __parallel_result = self._saving_process()
        self.reset_result()
        return __parallel_result


    def reset_result(self) -> None:
        self._Processors_Running_Result[:] = []



class ProcessStrategy(ParallelStrategy, _GeneralRunnableStrategy):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.Parallel
    __Process_List: List[Process] = None

    def __init__(self, executors: int):
        """
        Description:
            Converting the object to multiprocessing.manager.Namespace type object at initial state.
        """
        super().__init__(executors=executors)


    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(ProcessStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # Initial sub-class of 'multiprocessing.managers.BaseManager'
        # # **** Thinking ****
        # Thinking about how to make sure that weather it needs to start
        # multiprocessing.managers.BaseManager server or not.
        # # *****************
        activate_manager_server()


    @dispatch((FunctionType, MethodType, PartialFunction), args=tuple, kwargs=dict)
    def _start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> Process:
        __worker = self.generate_worker(target, *args, **kwargs)
        self.activate_workers(__worker)
        return __worker


    @dispatch(Iterable, args=tuple, kwargs=dict)
    def _start_new_worker(self, target: List[Callable], args: Tuple = (), kwargs: Dict = {}) -> List[Process]:
        __workers = [self.generate_worker(__function, *args, **kwargs) for __function in target]
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

        from .. import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            workers.close()


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


    def get_result(self) -> IterableType[_ParallelResult]:
        return self.result()


    def _saving_process(self) -> List[_ParallelResult]:
        __parallel_results = []
        for __result in self._Processors_Running_Result:
            _presult = _ParallelResult()

            # # # # Save some basic info of Process
            _presult.ppid = __result["ppid"]
            _presult.pid = __result["pid"]
            _presult.worker_name = __result["name"]
            _presult.worker_ident = __result["ident"]

            # # # # Save state of process
            __process_successful = __result.get("successful", None)
            if __process_successful is True:
                _presult.state = _ResultState.SUCCESS.value
            else:
                _presult.state = _ResultState.FAIL.value

            # # # # Save running result of process
            __process_result = __result.get("result", None)
            _presult.data = __process_result
            _presult.exit_code = __result["exitcode"]
            _presult.exception = __result.get("exception", None)

            __parallel_results.append(_presult)

        return __parallel_results



class ProcessPoolStrategy(ParallelStrategy, _PoolRunnableStrategy, _Resultable):

    _Processors_Pool: Pool = None
    _Processors_List: List[Union[ApplyResult, AsyncResult]] = None

    def __init__(self, pool_size: int, tasks_size: int):
        super().__init__(pool_size=pool_size, tasks_size=tasks_size)


    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(ProcessPoolStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # Activate multiprocessing.managers.BaseManager server
        activate_manager_server()

        # Initialize and build the Processes Pool.
        __pool_initializer: Callable = kwargs.get("pool_initializer", None)
        __pool_initargs: IterableType = kwargs.get("pool_initargs", None)
        self._Processors_Pool = Pool(processes=self.pool_size, initializer=__pool_initializer, initargs=__pool_initargs)


    def apply(self, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> None:
        self.reset_result()
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
        self._result_saving(successful=__process_run_successful, result=__process_running_result, exception=None)


    def async_apply(self,
                    function: Callable,
                    args: Tuple = (),
                    kwargs: Dict = {},
                    callback: Callable = None,
                    error_callback: Callable = None) -> None:
        self.reset_result()
        self._Processors_List = [
            self._Processors_Pool.apply_async(func=function,
                                              args=args,
                                              kwds=kwargs,
                                              callback=callback,
                                              error_callback=error_callback)
            for _ in range(self.tasks_size)]

        for process in self._Processors_List:
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
        _process_running_result = None

        try:
            _process_running_result = self._Processors_Pool.map(
                func=function, iterable=args_iter, chunksize=chunksize)
            _exception = None
            _process_run_successful = True
        except Exception as e:
            _exception = e
            _process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (_process_running_result or []):
            self._result_saving(successful=_process_run_successful, result=__result, exception=None)


    def async_map(self,
                  function: Callable,
                  args_iter: IterableType = (),
                  chunksize: int = None,
                  callback: Callable = None,
                  error_callback: Callable = None) -> None:
        self.reset_result()
        __map_result = self._Processors_Pool.map_async(
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
            __process_running_result = self._Processors_Pool.starmap(
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
        __map_result = self._Processors_Pool.starmap_async(
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
            imap_running_result = self._Processors_Pool.imap(func=function, iterable=args_iter, chunksize=chunksize)
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
            imap_running_result = self._Processors_Pool.imap_unordered(func=function, iterable=args_iter, chunksize=chunksize)
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
        _process_result = {"successful": successful, "result": result, "exception": exception}
        self._Processors_Running_Result.append(_process_result)


    def close(self) -> None:
        self._Processors_Pool.close()
        self._Processors_Pool.join()


    def terminal(self) -> None:
        self._Processors_Pool.terminate()


    def get_result(self) -> List[_ProcessPoolResult]:
        return self.result()


    def _saving_process(self) -> List[_ProcessPoolResult]:
        _pool_results = []
        for __result in self._Processors_Running_Result:
            _pool_result = _ProcessPoolResult()
            _pool_result.is_successful = __result["successful"]
            _pool_result.data = __result["result"]
            _pool_results.append(_pool_result)
        return _pool_results

