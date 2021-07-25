from pyocean.framework.strategy import InitializeUtils, RunnableStrategy, AsyncRunnableStrategy, Resultable
# from pyocean.framework.features import BaseQueueType
from pyocean.api.mode import FeatureMode
# from pyocean.coroutine.features import GeventQueueType, AsynchronousQueueType

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Iterable, Callable
# from greenlet import greenlet, getcurrent
from gevent.greenlet import Greenlet
from asyncio.tasks import Task
import asyncio
import gevent



class CoroutineStrategy(metaclass=ABCMeta):

    pass



class BaseGreenletStrategy(CoroutineStrategy, RunnableStrategy, ABC):

    _Running_Mode: FeatureMode = FeatureMode.MultiGreenlet
    _Gevent_List: List[Greenlet] = None
    _Gevent_Running_Result: List = []



class MultiGreenletStrategy(BaseGreenletStrategy, Resultable):

    def initialization(self, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # # Initialize and assign task queue object.
        # if tasks:
        #     __init_utils.initialize_queue(tasks=tasks, qtype=queue_type)
        # Initialize persistence object.
        if self._persistence_strategy is not None:
            __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_number)


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
        return self._Gevent_Running_Result



class BaseAsyncStrategy(CoroutineStrategy, AsyncRunnableStrategy, ABC):

    _Running_Mode: FeatureMode = FeatureMode.Asynchronous
    _Async_Event_Loop = None
    _Async_Task_List: List[Task] = None
    _Async_Running_Result: List = []

    def get_event_loop(self):
        pass



class AsynchronousStrategy(BaseAsyncStrategy, Resultable):

    def get_event_loop(self):
        self._Async_Event_Loop = asyncio.get_event_loop()
        return self._Async_Event_Loop


    async def initialization(self, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # # # Initialize and assign task queue object.
        # if tasks:
        #     await __init_utils.async_initialize_queue(tasks=tasks, qtype=queue_type)
        # Initialize persistence object.
        if self._persistence_strategy is not None:
            __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_number)


    def build_workers(self, function: Callable, *args, **kwargs) -> List[Task]:
        self._Async_Task_List = [self._Async_Event_Loop.create_task(function(*args, **kwargs)) for _ in range(self.workers_number)]
        return self._Async_Task_List


    async def activate_workers(self, workers_list: List[Task]) -> None:
        finished, unfinished = await asyncio.wait(workers_list)
        for finish in finished:
            self._Async_Running_Result.append(
                {"async_id": id,
                 "event_loop": finish.get_loop(),
                 "done_flag": finish.close(),
                 "result_data": finish.result(),
                 "exceptions": finish.exception()}
            )


    def close(self) -> None:
        self._Async_Event_Loop.close()


    def get_result(self) -> Iterable[object]:
        return self._Async_Running_Result

