from pyocean.framework.strategy import InitializeUtils, RunnableStrategy, Resultable, Globalize as RunningGlobalize
from pyocean.api.mode import RunningMode
from pyocean.coroutine.features import GeventQueueType, AsynchronousQueueType

from abc import ABC
from typing import List, Tuple, Dict, Iterable, Union, Callable
from multiprocessing.pool import ApplyResult
from threading import Thread
from greenlet import greenlet, getcurrent
import asyncio



class CoroutineStrategy(RunnableStrategy, ABC):

    _Running_Mode: RunningMode = None
    _Gevent_List: List[greenlet] = None
    _Gevent_Running_Result: Dict[str, Dict[str, Union[object, bool]]] = {}



class GeventStrategy(CoroutineStrategy, Resultable):

    _Running_Mode: RunningMode = RunningMode.MultiGreenlet


    def init_multi_working(self, tasks: Iterable, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # Initialize and assign task queue object.
        __init_utils.initialize_queue(tasks=tasks, qtype=GeventQueueType.Queue)
        # Initialize parameter and object with different scenario.
        __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_instances_number)


    def build_multi_workers(self, function: Callable, *args, **kwargs) -> List[Union[greenlet, Thread, ApplyResult]]:
        self._Gevent_List = [greenlet(run=function) for _ in range(self.threads_number)]
        return self._Gevent_List


    def activate_worker(self, worker: Union[greenlet, Thread, ApplyResult]) -> None:
        value = worker.switch()
        print(f"The greenlet running result: {value}")
        self._Gevent_Running_Result[getcurrent()] = value


    def end_multi_working(self) -> None:
        # if isinstance(self.__Greenlet_List, List) and isinstance(self.__Greenlet_List[0], greenlet):
        #     for threed_index in range(self.threads_number):
        #         self.__Greenlet_List[threed_index]
        # else:
        #     raise
        pass


    def get_multi_working_result(self) -> Iterable[object]:
        return self._Gevent_Running_Result



class AsynchronousStrategy(CoroutineStrategy, Resultable):

    _Running_Mode: RunningMode = RunningMode.Asynchronous
    __Async_Loop = None


    def init_multi_working(self, tasks: Iterable, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # Initialize and assign task queue object.
        __init_utils.initialize_queue(tasks=tasks, qtype=AsynchronousQueueType.Queue)
        # Initialize parameter and object with different scenario.
        __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_instances_number)

        # Initialize Event Loop object
        self.__Async_Loop = asyncio.get_event_loop()


    def build_multi_workers(self, function: Callable, *args, **kwargs) -> List[Union[greenlet, Thread, ApplyResult]]:
        self.__Async_Loop.run_until_complete(future=function(*args, **kwargs))
        return self._Greenlet_List


    def activate_worker(self, worker: Union[greenlet, Thread, ApplyResult]) -> None:
        value = worker.switch()
        print(f"The greenlet running result: {value}")
        # self._Gevent_Running_Result.append(value)


    def end_multi_working(self) -> None:
        # if isinstance(self.__Greenlet_List, List) and isinstance(self.__Greenlet_List[0], greenlet):
        #     for threed_index in range(self.threads_number):
        #         self.__Greenlet_List[threed_index]
        # else:
        #     raise
        pass


    def get_multi_working_result(self) -> Iterable[object]:
        return self._Gevent_Running_Result

