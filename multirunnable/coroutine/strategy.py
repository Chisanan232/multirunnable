from multirunnable.mode import FeatureMode as _FeatureMode
from multirunnable.coroutine.result import (
    CoroutineResult as _CoroutineResult,
    AsynchronousResult as _AsynchronousResult)
from multirunnable.framework.task import (
    BaseQueueTask as _BaseQueueTask,
    BasePersistenceTask as _BasePersistenceTask)
from multirunnable.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from multirunnable.framework.adapter.collection import BaseList as _BaseList
from multirunnable.framework.strategy import (
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    PoolRunnableStrategy as _PoolRunnableStrategy,
    AsyncRunnableStrategy as _AsyncRunnableStrategy,
    Resultable as _Resultable)

from abc import ABCMeta, ABC
from types import FunctionType, MethodType
from typing import List, Iterable as IterableType, Callable, Optional, Union, Tuple, Dict
from collections import Iterable
from multipledispatch import dispatch
from gevent.greenlet import Greenlet
from gevent.pool import Pool
from asyncio.tasks import Task
import functools
import itertools
import asyncio
import gevent



def starmapstar(args):
    return list(itertools.starmap(args[0], args[1]))



class CoroutineStrategy(metaclass=ABCMeta):

    pass



class BaseGreenThreadStrategy(CoroutineStrategy):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.GreenThread
    # _Gevent_Running_Result: List = []
    _GreenThread_Running_Result: List = []

    def result(self) -> List[_CoroutineResult]:
        __coroutine_results = self._result_handling()
        return __coroutine_results


    def _result_handling(self) -> List[_CoroutineResult]:
        __coroutine_results = []
        for __result in self._GreenThread_Running_Result:
            __coroutine_result = _CoroutineResult()
            __coroutine_result.data = __result
            __coroutine_results.append(__coroutine_result)

        return __coroutine_results



class GreenThreadStrategy(BaseGreenThreadStrategy, _GeneralRunnableStrategy, _Resultable):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.GreenThread

    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(GreenThreadStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(db_conn_num=self.db_connection_pool_size)


    @dispatch(MethodType, tuple, dict)
    def start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> Greenlet:
        __worker = self.generate_worker(target=target, *args, **kwargs)
        self.activate_workers(__worker)
        return __worker


    @dispatch(Iterable, tuple, dict)
    def start_new_worker(self, target: List[Callable], args: Tuple = (), kwargs: Dict = {}) -> List[Greenlet]:
        __workers = [self.generate_worker(target=__function, *args, **kwargs) for __function in target]
        self.activate_workers(__workers)
        return __workers


    def generate_worker(self, target: Callable, *args, **kwargs) -> Greenlet:
        # return gevent.spawn(target, *args, **kwargs)
        return Greenlet(target, *args, **kwargs)


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
        result = GreenThreadStrategy._format_result(worker=workers)
        self._GreenThread_Running_Result.append(result)


    @dispatch(Iterable)
    def close(self, workers: List[Greenlet]) -> None:
        gevent.joinall(workers)
        results = map(GreenThreadStrategy._format_result, workers)
        self._GreenThread_Running_Result = list(results)


    def kill(self) -> None:
        pass


    def terminal(self) -> None:
        pass


    def get_result(self) -> List[_CoroutineResult]:
        return self.result()


    @staticmethod
    def _format_result(worker: Greenlet) -> Dict:
        return {
            "loop": worker.loop,
            "parent": worker.parent,
            "name": worker.name,
            "args": worker.args,
            "kwargs": worker.kwargs,
            "value": worker.value,
            "exception": worker.exception,
            "successfully": worker.successful()
        }



class GreenThreadPoolStrategy(BaseGreenThreadStrategy, _PoolRunnableStrategy, _Resultable):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.GreenThread

    _GreenThread_Pool: Pool = None
    _GreenThread_List: List[Greenlet] = []
    # _GreenThread_Running_Result: List = []

    def __init__(self, pool_size: int, tasks_size: int, persistence: _BasePersistenceTask = None):
        super().__init__(pool_size=pool_size, tasks_size=tasks_size, persistence=persistence)


    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(GreenThreadPoolStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(db_conn_num=self.db_connection_pool_size)

        # Initialize and build the Processes Pool.
        # self._GreenThread_Pool = Pool(size=self.pool_size, greenlet_class=greenlet_class)
        self._GreenThread_Pool = Pool(size=self.pool_size)


    def apply(self, function: Callable, *args, **kwargs) -> None:
        __process_running_result = None

        try:
            __process_running_result = [
                self._GreenThread_Pool.apply(func=function, args=args, kwds=kwargs)
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
        self._GreenThread_List = [
            self._GreenThread_Pool.apply_async(func=function,
                                               args=args,
                                               kwds=kwargs,
                                               callback=callback)
            for _ in range(self.tasks_size)]

        for process in self._GreenThread_List:
            __process_running_result = process.get()
            __process_run_successful = process.successful()

            # Save Running result state and Running result value as dict
            self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def map(self, function: Callable, args_iter: IterableType = (), chunksize: int = None) -> None:
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
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def async_map(self,
                  function: Callable,
                  args_iter: IterableType = (),
                  chunksize: int = None,
                  callback: Callable = None,
                  error_callback: Callable = None) -> None:
        __map_result = self._GreenThread_Pool.map_async(
            func=function,
            iterable=args_iter,
            callback=callback)
        __process_running_result = __map_result.get()
        __process_run_successful = __map_result.successful()

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


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
        args_iter_set = set(args_iter)
        if len(args_iter_set) == 1:
            _arguments = tuple(args_iter_set)[0]
            self._map_with_args(function=function, args=_arguments)
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
            self._result_saving(successful=__process_run_successful, result=__results)


    def _map_with_args(self, function: Callable, args: Iterable) -> None:
        _args = args[:-1]
        _last_args = args[-1:] * len(_args)
        partial_function = functools.partial(func=function, *_args)
        self.map(function=partial_function, args_iter=_last_args)


    def async_map_by_args(self,
                          function: Callable,
                          args_iter: IterableType[IterableType] = (),
                          chunksize: int = None,
                          callback: Callable = None,
                          error_callback: Callable = None) -> None:
        self.async_map(function=function, args_iter=args_iter, callback=callback)


    def imap(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        __process_running_result = None

        try:
            imap_running_result = self._GreenThread_Pool.imap(function, args_iter)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = False
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def imap_unordered(self, function: Callable, args_iter: IterableType = (), chunksize: int = 1) -> None:
        __process_running_result = None

        try:
            imap_running_result = self._GreenThread_Pool.imap_unordered(function, args_iter)
            __process_running_result = [result for result in imap_running_result]
            __exception = None
            __process_run_successful = False
        except Exception as e:
            __exception = e
            __process_run_successful = False

        # Save Running result state and Running result value as dict
        self._result_saving(successful=__process_run_successful, result=__process_running_result)


    def _result_saving(self, successful: bool, result: List) -> None:
        process_result = {"successful": successful, "result": result}
        # Saving value into list
        self._GreenThread_Running_Result.append(process_result)


    def close(self) -> None:
        self._GreenThread_Pool.join()


    def terminal(self) -> None:
        pass
        # self._GreenThread_Pool.terminate()


    def get_result(self) -> List[_CoroutineResult]:
        return self.result()



class BaseAsyncStrategy(CoroutineStrategy, _AsyncRunnableStrategy, ABC):

    _Strategy_Feature_Mode = _FeatureMode.Asynchronous
    _Async_Event_Loop = None
    _Async_Task_List: List[Task] = None
    _Async_Running_Result: List = []

    def get_event_loop(self):
        pass



class AsynchronousStrategy(BaseAsyncStrategy, _Resultable):

    _Strategy_Feature_Mode: _FeatureMode = _FeatureMode.Asynchronous

    @dispatch(MethodType, tuple, dict)
    def start_new_worker(self, target: Callable, args: Tuple = (), kwargs: Dict = {}) -> None:

        async def __start_new_async_task():
            __worker = await self.generate_worker(target=target, *args, **kwargs)
            await self.activate_workers(__worker)

        asyncio.run(__start_new_async_task())


    @dispatch(Iterable, tuple, dict)
    def start_new_worker(self, target: List[Callable], args: Tuple = (), kwargs: Dict = {}) -> None:

        async def __start_new_async_tasks():
            __workers = [await self.generate_worker(target=__function, *args, **kwargs) for __function in target]
            await self.activate_workers(__workers)

        asyncio.run(__start_new_async_tasks())


    def run(self,
            function: Callable,
            args: Optional[Union[Tuple, Dict]] = None,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:

        async def __run_process():
            await self.initialization(queue_tasks=queue_tasks, features=features)
            workers_list = [self._generate_worker(function, args) for _ in range(self.executors_number)]
            await self.activate_workers(workers_list)

        asyncio.run(__run_process())


    def map(self,
            function: Callable,
            args_iter: IterableType = [],
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:

        async def __map_process():
            await self.initialization(queue_tasks=queue_tasks, features=features)
            __workers_list = [self._generate_worker(function, args) for args in args_iter]
            await self.activate_workers(__workers_list)

        asyncio.run(__map_process())


    def map_with_function(self,
                          functions: IterableType[Callable],
                          args_iter: IterableType = [],
                          queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                          features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:

        async def __map_with_function_process():
            nonlocal args_iter
            if args_iter is None or args_iter == []:
                args_iter = [() for _ in range(len(list(functions)))]

            await self.initialization(queue_tasks=queue_tasks, features=features)
            __workers_list = [self._generate_worker(fun, args) for fun, args in zip(functions, args_iter)]
            await self.activate_workers(__workers_list)

        asyncio.run(__map_with_function_process())


    async def initialization(self,
                             queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                             features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                             *args, **kwargs) -> None:
        _running_event_loop = asyncio.get_running_loop()
        kwargs["event_loop"] = _running_event_loop
        await super(AsynchronousStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(
                db_conn_num=self.db_connection_pool_size,
                event_loop=kwargs.get("event_loop"))


    def generate_worker(self, target: Callable, *args, **kwargs) -> Task:
        return asyncio.create_task(target(*args, **kwargs))


    @dispatch(Task)
    async def activate_workers(self, workers: Task) -> None:
        value = await workers
        self._Async_Running_Result.append({
            "result": value
        })


    @dispatch(Iterable)
    async def activate_workers(self, workers: List[Task]) -> None:
        for worker in workers:
            await self.activate_workers(worker)


    @dispatch(Task)
    async def close(self, workers: Task) -> None:
        pass


    @dispatch(Iterable)
    async def close(self, workers: List[Task]) -> None:
        pass


    def terminal(self) -> None:
        pass


    def kill(self) -> None:
        pass


    def get_result(self) -> List[_AsynchronousResult]:
        __async_results = self._result_handling()
        return __async_results


    def _result_handling(self) -> List[_AsynchronousResult]:
        __async_results = []
        for __result in self._Async_Running_Result:
            __async_result = _AsynchronousResult()

            # __async_result.worker_id = __result.get("async_id")
            # __async_result.event_loop = __result.get("event_loop")
            # __async_result.data = __result.get("result_data")
            # __async_result.exception = __result.get("exceptions")

            __async_result.data = __result.get("result")

            __async_results.append(__async_result)

        return __async_results

