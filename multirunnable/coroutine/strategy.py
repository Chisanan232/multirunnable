from multipledispatch import dispatch
from gevent.threading import get_ident, getcurrent
from gevent.greenlet import Greenlet
from collections.abc import Iterable
from asyncio.tasks import Task
from gevent.pool import Pool
from typing import List, Iterable as IterableType, Callable, Optional, Union, Tuple, Dict
from types import FunctionType, MethodType
from abc import ABCMeta, ABC
from os import getpid
import functools
import asyncio
import gevent

from ..framework.runnable import (
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    PoolRunnableStrategy as _PoolRunnableStrategy,
    AsyncRunnableStrategy as _AsyncRunnableStrategy,
    Resultable as _Resultable,
    ResultState as _ResultState
)
from ..framework.factory import (
    BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory,
    BaseList as _BaseList
)
from ..framework import BaseQueueTask as _BaseQueueTask
from ..coroutine.result import (
    CoroutineResult as _CoroutineResult,
    GreenThreadPoolResult as _GreenThreadPoolResult,
    AsynchronousResult as _AsynchronousResult)
from ..mode import FeatureMode as _FeatureMode
from .. import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION



class CoroutineStrategy(metaclass=ABCMeta):

    _GreenThread_Running_Result_By_Name: Dict[str, dict] = {}
    _GreenThread_Running_Result: List = []
    _Async_Running_Result: List = []

    @classmethod
    def save_return_value(cls, function: Callable) -> Callable:
        __self = cls

        @functools.wraps(function)
        def save_value_fun(*args, **kwargs) -> None:
            _current_thread = getcurrent()

            _thread_result = {
                "pid": getpid(),
                "name": _current_thread.name,
                "ident": get_ident()
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
                    "successful": True,
                })
            finally:
                __self._GreenThread_Running_Result_By_Name[str(_current_thread.name)] = _thread_result

        return save_value_fun


    @classmethod
    def async_save_return_value(cls, function: Callable) -> Callable:
        __self = cls

        @functools.wraps(function)
        async def save_value_fun(*args, **kwargs) -> None:
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _current_task = asyncio.current_task()
            else:
                _current_task = asyncio.Task.current_task()

            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) >= (3, 8):
                _task_result = {
                    "pid": getpid(),
                    "name": _current_task.get_name(),
                    "mem_id": id(_current_task)
                }
            else:
                _task_result = {
                    "pid": getpid(),
                    "name": f"AsyncTask-{id(_current_task)}",
                    "mem_id": id(_current_task)
                }

            try:
                value = await function(*args, **kwargs)
            except Exception as e:
                _task_result.update({
                    "successful": False,
                    "exception": e
                })
            else:
                _task_result.update({
                    "result": value,
                    "successful": True,
                })
            finally:
                __self._Async_Running_Result.append(_task_result)

        return save_value_fun



class BaseGreenThreadStrategy(CoroutineStrategy, _Resultable, ABC):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.GreenThread
    # _Gevent_Running_Result: List = []
    # _GreenThread_Running_Result: List = []

    def result(self) -> List[_CoroutineResult]:
        __coroutine_results = self._saving_process()
        self.reset_result()
        return __coroutine_results


    def reset_result(self):
        self._GreenThread_Running_Result[:] = []



class GreenThreadStrategy(BaseGreenThreadStrategy, _GeneralRunnableStrategy):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.GreenThread

    def initialization(self, queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(GreenThreadStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)


    @dispatch((FunctionType, MethodType, functools.partial), args=tuple, kwargs=dict)
    def _start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> Greenlet:
        __worker = self.generate_worker(target, *args, **kwargs)
        self.activate_workers(__worker)
        return __worker


    @dispatch(Iterable, args=tuple, kwargs=dict)
    def _start_new_worker(self, target: List[Callable], args: Tuple = (), kwargs: Dict = {}) -> List[Greenlet]:
        __workers = [self.generate_worker(__function, *args, **kwargs) for __function in target]
        self.activate_workers(__workers)
        return __workers


    def generate_worker(self, target: Callable, *args, **kwargs) -> Greenlet:

        @functools.wraps(target)
        @CoroutineStrategy.save_return_value
        def _target_function(*_args, **_kwargs):
            result_value = target(*_args, **_kwargs)
            return result_value

        # return gevent.spawn(_target_function, *args, **kwargs)
        return Greenlet(_target_function, *args, **kwargs)


    @dispatch(Greenlet)
    def activate_workers(self, workers: Greenlet) -> None:
        workers.start()


    @dispatch(Iterable)
    def activate_workers(self, workers: List[Greenlet]) -> None:
        for worker in workers:
            self.activate_workers(worker)


    @dispatch(Greenlet)
    def close(self, workers: Greenlet) -> None:
        workers.join()
        result = self._format_result(worker=workers)
        self._GreenThread_Running_Result.append(result)


    @dispatch(Iterable)
    def close(self, workers: List[Greenlet]) -> None:
        gevent.joinall(workers)
        results = map(self._format_result, workers)
        self._GreenThread_Running_Result = [_r for _r in results]


    def kill(self) -> None:
        # gevent.kill(greenlet=, exception=)
        # gevent.killall(greenlets=, exception=, block=, timeout=)
        pass


    def get_result(self) -> List[_CoroutineResult]:
        return self.result()


    def _format_result(self, worker: Greenlet) -> Dict:
        assert worker.name in self._GreenThread_Running_Result_By_Name, f"It should must have the AsyncTask which be named as '{worker.name}'."
        _async_task_result = self._GreenThread_Running_Result_By_Name[worker.name]
        _async_task_result.update({
            # "loop": worker.loop,
            "parent": worker.parent,
            "args": worker.args,
            "kwargs": worker.kwargs,
        })
        return _async_task_result


    def _saving_process(self) -> List[_CoroutineResult]:
        __coroutine_results = []
        for __result in self._GreenThread_Running_Result:
            _cresult = _CoroutineResult()

            # # # # Save some basic info of Process
            _cresult.pid = __result["pid"]
            _cresult.worker_name = __result["name"]
            _cresult.worker_ident = __result["ident"]
            _cresult.parent = __result["parent"]
            _cresult.args = __result["args"]
            _cresult.kwargs = __result["kwargs"]

            # # # # Save state of process
            __coroutine_successful = __result.get("successful", None)
            if __coroutine_successful is True:
                _cresult.state = _ResultState.SUCCESS.value
            else:
                _cresult.state = _ResultState.FAIL.value

            # # # # Save running result of process
            _cresult.data = __result.get("result", None)
            _cresult.exception = __result.get("exception", None)
            __coroutine_results.append(_cresult)

        return __coroutine_results



class GreenThreadPoolStrategy(BaseGreenThreadStrategy, _PoolRunnableStrategy, _Resultable):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.GreenThread

    _GreenThread_Pool: Pool = None
    _GreenThread_List: List[Greenlet] = []
    # _GreenThread_Running_Result: List = []

    def __init__(self, pool_size: int):
        super().__init__(pool_size=pool_size)


    def initialization(self, queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:

        super(GreenThreadPoolStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # Initialize and build the Processes Pool.
        # self._GreenThread_Pool = Pool(size=self.pool_size, greenlet_class=greenlet_class)
        self._GreenThread_Pool = Pool(size=self.pool_size)


    def apply(self, tasks_size: int, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> None:
        self.reset_result()

        self._GreenThread_List = [
            self._GreenThread_Pool.apply(func=function, args=args, kwds=kwargs)
            for _ in range(tasks_size)]

        for _green_thread in self._GreenThread_List:
            __process_running_result = None
            __process_run_successful = None
            __exception = None

            try:
                __process_running_result = _green_thread
                __exception = None
                __process_run_successful = True
            except Exception as e:
                __exception = e
                __process_run_successful = False

            # Save Running result state and Running result value as dict
            self._result_saving(successful=__process_run_successful, result=__process_running_result, exception=__exception)


    def async_apply(self, tasks_size: int, function: Callable, args: Tuple = (),
                    kwargs: Dict = {}, callback: Callable = None, error_callback: Callable = None) -> None:

        self.reset_result()
        self._GreenThread_List = [
            self._GreenThread_Pool.apply_async(func=function,
                                               args=args,
                                               kwds=kwargs,
                                               callback=callback)
            for _ in range(tasks_size)]

        for process in self._GreenThread_List:
            __process_running_result = None
            __process_run_successful = None
            __exception = None

            try:
                __process_running_result = process.get()
                __process_run_successful = process.successful()
                __exception = None
            except Exception as e:
                __exception = e
                __process_running_result = None
                __process_run_successful = process.successful()

            # Save Running result state and Running result value as dict
            self._result_saving(successful=__process_run_successful, result=__process_running_result, exception=__exception)


    def apply_with_iter(self, functions_iter: List[Callable], args_iter: List[Tuple] = None, kwargs_iter: List[Dict] = None) -> None:
        self.reset_result()
        __process_running_result = None

        if args_iter is None:
            args_iter = [() for _ in functions_iter]

        if kwargs_iter is None:
            kwargs_iter = [{} for _ in functions_iter]

        self._GreenThread_List = [
            self._GreenThread_Pool.apply(func=_func, args=_args, kwds=_kwargs)
            for _func, _args, _kwargs in zip(functions_iter, args_iter, kwargs_iter)
        ]

        for _green_thread in self._GreenThread_List:
            __process_running_result = None
            __process_run_successful = None
            __exception = None

            try:
                __process_running_result = _green_thread
                __exception = None
                __process_run_successful = True
            except Exception as e:
                __exception = e
                __process_run_successful = False

            # Save Running result state and Running result value as dict
            self._result_saving(successful=__process_run_successful, result=__process_running_result, exception=__exception)


    def async_apply_with_iter(self, functions_iter: List[Callable], args_iter: List[Tuple] = None,
                              kwargs_iter: List[Dict] = None, callback_iter: List[Callable] = None,
                              error_callback_iter: List[Callable] = None) -> None:

        self.reset_result()

        if args_iter is None:
            args_iter = [() for _ in functions_iter]

        if kwargs_iter is None:
            kwargs_iter = [{} for _ in functions_iter]

        if callback_iter is None:
            callback_iter = [None for _ in functions_iter]

        if error_callback_iter is None:
            error_callback_iter = [None for _ in functions_iter]

        self._GreenThread_List = [
            self._GreenThread_Pool.apply_async(
                func=_func,
                args=_args,
                kwds=_kwargs,
                callback=_callback)
            for _func, _args, _kwargs, _callback in zip(functions_iter, args_iter, kwargs_iter, callback_iter)
        ]

        for process in self._GreenThread_List:
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
            __process_running_result = self._GreenThread_Pool.map(
                func=function, iterable=args_iter)
            __exception = None
            __process_run_successful = True
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=__exception)


    def async_map(self, function: Callable, args_iter: IterableType = (), chunksize: int = None,
                  callback: Callable = None, error_callback: Callable = None) -> None:

        self.reset_result()

        __process_running_result = None
        __process_run_successful = None
        __exception = None

        __map_result = self._GreenThread_Pool.map_async(
            func=function,
            iterable=args_iter,
            callback=callback)
        try:
            __process_running_result = __map_result.get()
            __process_run_successful = __map_result.successful()
        except Exception as e:
            __exception = e
            __process_running_result = None

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=__exception)


    def map_by_args(self, function: Callable, args_iter: IterableType[IterableType] = (), chunksize: int = None) -> None:
        """
        Note:
            For Green-Thread in Python (gevent), there isn't any methods
            could pass multiple parameters like multiprocessing.pool.starmap.
        :param function:
        :param args_iter:
        :param chunksize:
        :return:
        """
        self.reset_result()
        args_iter_set = set(args_iter)
        if len(args_iter_set) == 1:
            _arguments = args_iter[0]
            self._map_with_args(function=function, args=_arguments, size=len(args_iter), chunksize=chunksize)
        else:
            __results = []
            __process_run_successful = None

            try:
                for _args in args_iter:
                    _greenlet = self._GreenThread_Pool.spawn(function, *_args)
                    self._GreenThread_List.append(_greenlet)

                for _one_greenlet in self._GreenThread_List:
                    _one_greenlet.join()
                    _one_greenlet_value = _one_greenlet.value
                    __results.append(_one_greenlet_value)

                __process_run_successful = True
                __exception = None
            except Exception as e:
                __process_run_successful = False
                __exception = e

            # Save Running result state and Running result value as dict
            for __result in (__results or []):
                self._result_saving(successful=__process_run_successful, result=__result, exception=__exception)


    def _map_with_args(self, function: Callable, args: Iterable, size: int, chunksize: int) -> None:
        """
        Description:
            For passing multiple arguments into target function.
            That's the reason why initial a partial function first and then pass ONE parameter into it.
        :param function:
        :param args:
        :param size:
        :param chunksize:
        :return:
        """
        self.reset_result()
        _args = args[:-1]
        _last_args = args[-1:] * size
        partial_function = functools.partial(function, *_args)
        self.map(function=partial_function, args_iter=_last_args, chunksize=chunksize)


    def async_map_by_args(self, function: Callable, args_iter: IterableType[IterableType] = (),
                          chunksize: int = None, callback: Callable = None, error_callback: Callable = None) -> None:

        self.reset_result()
        args_iter_set = set(args_iter)
        if len(args_iter_set) == 1:
            _arguments = args_iter[0]
            self._async_map_with_args(function=function, args=_arguments, size=len(args_iter), chunksize=chunksize, callback=callback)
        else:
            __results = []
            __process_run_successful = None

            try:
                for _args in args_iter:
                    _greenlet = self._GreenThread_Pool.spawn(function, *_args)
                    self._GreenThread_List.append(_greenlet)

                for _one_greenlet in self._GreenThread_List:
                    _one_greenlet.join()
                    _one_greenlet_value = _one_greenlet.value
                    __results.append(_one_greenlet_value)

                __process_run_successful = True
                __exception = None
            except Exception as e:
                __process_run_successful = False
                __exception = e

            # Save Running result state and Running result value as dict
            for __result in (__results or []):
                self._result_saving(successful=__process_run_successful, result=__result, exception=__exception)


    def _async_map_with_args(self, function: Callable, args: Iterable, size: int, chunksize: int, callback: Callable) -> None:
        """
        Description:
            This is asynchronous version of function '_map_with_args'.
        :param function:
        :param args:
        :param size:
        :param chunksize:
        :param callback:
        :return:
        """
        self.reset_result()
        _args = args[:-1]
        _last_args = args[-1:] * size
        partial_function = functools.partial(function, *_args)
        self.async_map(function=partial_function, args_iter=_last_args, chunksize=chunksize, callback=callback)


    def imap(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        self.reset_result()
        __process_running_result = None

        try:
            imap_running_result = self._GreenThread_Pool.imap(function, args_iter)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = True
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=__exception)


    def imap_unordered(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        self.reset_result()
        __process_running_result = None

        try:
            imap_running_result = self._GreenThread_Pool.imap_unordered(function, args_iter)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = True
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        for __result in (__process_running_result or []):
            self._result_saving(successful=__process_run_successful, result=__result, exception=__exception)


    def _result_saving(self, successful: bool, result: List, exception: Exception) -> None:
        process_result = {"successful": successful, "result": result, "exception": exception}
        # Saving value into list
        self._GreenThread_Running_Result.append(process_result)


    def close(self) -> None:
        self._GreenThread_Pool.join()


    def terminal(self) -> None:
        pass
        # self._GreenThread_Pool.terminate()


    def get_result(self) -> List[_CoroutineResult]:
        return self.result()


    def _saving_process(self) -> List[_GreenThreadPoolResult]:
        _pool_results = []
        for __result in self._GreenThread_Running_Result:
            _pool_result = _GreenThreadPoolResult()
            _pool_result.is_successful = __result["successful"]
            _pool_result.data = __result["result"]
            _pool_result.exception = __result["exception"]
            _pool_results.append(_pool_result)
        return _pool_results



class BaseAsyncStrategy(CoroutineStrategy, _AsyncRunnableStrategy, ABC):

    _Strategy_Feature_Mode = _FeatureMode.Asynchronous

    def reset_result(self):
        self._Async_Running_Result[:] = []



class AsynchronousStrategy(BaseAsyncStrategy, _Resultable):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.Asynchronous

    @dispatch((FunctionType, MethodType, functools.partial), args=tuple, kwargs=dict)
    def _start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> None:
        self.reset_result()

        async def __start_new_async_task():
            __worker = await self.generate_worker(target, *args, **kwargs)
            await self.activate_workers(__worker)

        AsynchronousStrategy._run_async_task(__start_new_async_task)


    @dispatch(Iterable, args=tuple, kwargs=dict)
    def _start_new_worker(self, target: List[Callable], args: Tuple = (), kwargs: Dict = {}) -> None:
        self.reset_result()

        async def __start_new_async_tasks():
            __workers = [await self.generate_worker(__function, *args, **kwargs) for __function in target]
            await self.activate_workers(__workers)

        AsynchronousStrategy._run_async_task(__start_new_async_tasks)


    def run(self, function: Callable, args: Optional[Union[Tuple, Dict]] = None,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:

        self.reset_result()

        async def __run_process():
            await self.initialization(queue_tasks=queue_tasks, features=features)
            workers_list = [self._generate_worker(function, args) for _ in range(self.executors_number)]
            await self.activate_workers(workers_list)

        AsynchronousStrategy._run_async_task(__run_process)


    def map(self, function: Callable, args_iter: IterableType = [],
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:

        self.reset_result()

        async def __map_process():
            await self.initialization(queue_tasks=queue_tasks, features=features)
            __workers_list = [self._generate_worker(function, args) for args in args_iter]
            await self.activate_workers(__workers_list)

        AsynchronousStrategy._run_async_task(__map_process)


    def map_with_function(self, functions: IterableType[Callable], args_iter: IterableType = [],
                          queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                          features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:

        self.reset_result()

        async def __map_with_function_process():
            nonlocal args_iter
            if args_iter is None or args_iter == []:
                args_iter = [() for _ in range(len(list(functions)))]

            await self.initialization(queue_tasks=queue_tasks, features=features)
            __workers_list = [self._generate_worker(fun, args) for fun, args in zip(functions, args_iter)]
            await self.activate_workers(__workers_list)

        AsynchronousStrategy._run_async_task(__map_with_function_process)


    async def initialization(self, queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                             features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                             *args, **kwargs) -> None:

        if kwargs.get("event_loop") is None:
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _running_event_loop = asyncio.get_running_loop()
            else:
                # # # # Python 3.6
                # # # # It will raise an exception: AttributeError: module 'asyncio' has no attribute 'get_running_loop'
                _running_event_loop = asyncio.get_event_loop()
            kwargs["event_loop"] = _running_event_loop
        await super(AsynchronousStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)


    def generate_worker(self, target: Callable, *args, **kwargs) -> Task:

        @functools.wraps(target)
        @CoroutineStrategy.async_save_return_value
        def _target_function(*_args, **_kwargs):
            result_value = target(*_args, **_kwargs)
            return result_value

        # return asyncio.create_task(target(*args, **kwargs))
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            return asyncio.create_task(_target_function(*args, **kwargs))
        else:
            # # # # Python 3.6
            # # # # It will raise an exception: AttributeError: module 'asyncio' has no attribute 'create_task'
            _event_loop = asyncio.get_event_loop()
            return _event_loop.create_task(_target_function(*args, **kwargs))


    @dispatch(Task)
    async def activate_workers(self, workers: Task) -> None:
        value = await workers
        # self._Async_Running_Result.append({
        #     "result": value
        # })


    @dispatch(Iterable)
    async def activate_workers(self, workers: List[Task]) -> None:
        for worker in workers:
            await self.activate_workers(worker)


    @dispatch(Task)
    async def close(self, workers: Task) -> None:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) <= (3, 6):
            _event_loop = asyncio.get_event_loop()
            _event_loop.close()


    @dispatch(Iterable)
    async def close(self, workers: List[Task]) -> None:
        pass


    def get_result(self) -> List[_AsynchronousResult]:
        __async_results = self._saving_process()
        self.reset_result()
        return __async_results


    def _saving_process(self) -> List[_AsynchronousResult]:
        _async_results = []
        for __result in self._Async_Running_Result:
            _async_result = _AsynchronousResult()

            # # # # Save some basic info of Process
            _async_result.pid = __result["pid"]
            _async_result.worker_name = __result["name"]
            _async_result.worker_ident = __result["mem_id"]

            # # # # Save state of process
            __coroutine_successful = __result.get("successful", None)
            if __coroutine_successful is True:
                _async_result.state = _ResultState.SUCCESS.value
            else:
                _async_result.state = _ResultState.FAIL.value

            # # # # Save running result of process
            _async_result.data = __result.get("result", None)
            _async_result.exception = __result.get("exception", None)
            _async_results.append(_async_result)

        return _async_results


    @staticmethod
    def _run_async_task(_function):
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(_function())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(_function())

