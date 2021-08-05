from pyocean.framework.task import BaseQueueTask
from pyocean.framework.strategy import RunnableStrategy, AsyncRunnableStrategy, Resultable
from pyocean.api.mode import FeatureMode
from pyocean.api.tool import Feature
from pyocean.coroutine.result import CoroutineResult, AsynchronousResult

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Iterable, Callable, Optional
from gevent.greenlet import Greenlet
from asyncio.tasks import Task
import asyncio
import gevent



class CoroutineStrategy(metaclass=ABCMeta):

    pass



class BaseGreenletStrategy(CoroutineStrategy, RunnableStrategy, ABC):

    _Running_Feature_Mode: FeatureMode = FeatureMode.MultiGreenlet
    _Gevent_List: List[Greenlet] = None
    _Gevent_Running_Result: List = []



class MultiGreenletStrategy(BaseGreenletStrategy, Resultable):

    def initialization(self, queue_tasks: Optional[List[BaseQueueTask]] = None,
                       features: Optional[List[Feature]] = None, *args, **kwargs) -> None:
        super(MultiGreenletStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(mode=self._Running_Feature_Mode, db_conn_num=self.db_connection_number)


    def build_workers(self, function: Callable, *args, **kwargs) -> List[Greenlet]:
        # # General Greenlet
        # self._Gevent_List = [greenlet(run=function) for _ in range(self.threads_number)]
        # # Greenlet framework -- Gevent
        self._Gevent_List = [gevent.spawn(function, *args, **kwargs) for _ in range(self.workers_number)]
        return self._Gevent_List


    def activate_workers(self, workers_list: List[Greenlet]) -> None:
        # # General Greenlet
        # value = worker.switch()
        # # Greenlet framework -- Gevent
        greenlets_list = gevent.joinall(workers_list)
        for one_greenlet in greenlets_list:
            self._Gevent_Running_Result.append(one_greenlet.value)


    def close(self) -> None:
        for one_greenlet in self._Gevent_List:
            one_greenlet.join()


    def get_result(self) -> Iterable[object]:
        __coroutine_results = self._result_handling()
        return __coroutine_results


    def _result_handling(self) -> List[CoroutineResult]:
        __coroutine_results = []
        for __result in self._Gevent_Running_Result:
            __coroutine_result = CoroutineResult()
            __coroutine_result.data = __result
            __coroutine_results.append(__coroutine_result)

        return __coroutine_results



class BaseAsyncStrategy(CoroutineStrategy, AsyncRunnableStrategy, ABC):

    _Running_Feature_Mode: FeatureMode = FeatureMode.Asynchronous
    _Async_Event_Loop = None
    _Async_Task_List: List[Task] = None
    _Async_Running_Result: List = []

    def get_event_loop(self):
        pass



class AsynchronousStrategy(BaseAsyncStrategy, Resultable):

    def get_event_loop(self):
        self._Async_Event_Loop = asyncio.get_event_loop()
        return self._Async_Event_Loop


    async def initialization(self, queue_tasks: Optional[List[BaseQueueTask]] = None,
                             features: Optional[List[Feature]] = None, *args, **kwargs) -> None:
        await super(AsynchronousStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(
                mode=self._Running_Feature_Mode,
                db_conn_num=self.db_connection_number,
                event_loop=kwargs.get("event_loop"))


    def build_workers(self, function: Callable, *args, **kwargs) -> List[Task]:
        self._Async_Task_List = [self._Async_Event_Loop.create_task(function(*args, **kwargs)) for _ in range(self.workers_number)]
        return self._Async_Task_List


    async def activate_workers(self, workers_list: List[Task]) -> None:
        finished, unfinished = await asyncio.wait(workers_list)
        for finish in finished:
            self._Async_Running_Result.append(
                {"async_id": id,
                 "event_loop": finish.get_loop(),
                 # "done_flag": finish.close(),
                 "result_data": finish.result(),
                 "exceptions": finish.exception()}
            )


    def close(self) -> None:
        self._Async_Event_Loop.close()


    def get_result(self) -> Iterable[object]:
        __async_results = self._result_handling()
        return __async_results


    def _result_handling(self) -> List[AsynchronousResult]:
        __async_results = []
        for __result in self._Async_Running_Result:
            __async_result = AsynchronousResult()

            __async_result.worker_id = __result.get("async_id")
            __async_result.event_loop = __result.get("event_loop")
            __async_result.data = __result.get("result_data")
            __async_result.exception = __result.get("exceptions")

            __async_results.append(__async_result)

        return __async_results

