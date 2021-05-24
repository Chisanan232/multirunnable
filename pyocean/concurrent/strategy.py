from pyocean.framework.strategy import InitializeUtils, RunnableStrategy, Resultable, Globalize as RunningGlobalize
from pyocean.framework.features import BaseQueueType
from pyocean.api import RunningMode, RunningStrategyAPI
from pyocean.concurrent.features import MultiThreadingQueueType
from pyocean.persistence.database import SingleConnection, MultiConnections
from pyocean.persistence.database.multi_connections import Globalize as DatabaseGlobalize
from pyocean.persistence.file.saver import BaseFileSaver, SingleFileSaver, MultiFileSaver

from abc import ABCMeta, abstractmethod, ABC
from typing import List, Tuple, Dict, Iterable, Union, Callable
from multiprocessing.pool import ApplyResult
from multiprocessing.queues import Queue as Process_Queue
from queue import Queue
from threading import Thread, Semaphore as ThreadingSemaphore
from greenlet import greenlet

from deprecated.sphinx import deprecated



class ConcurrentStrategy(RunnableStrategy, ABC):

    _Running_Mode: RunningMode = RunningMode.MultiThreading
    _Threads_List: List[Thread] = None
    _Threads_Running_Result: Dict[str, Dict[str, Union[object, bool]]] = {}



class MultiThreadingStrategy(ConcurrentStrategy):

    def init_multi_working(self, tasks: Iterable, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # Initialize and assign task queue object.
        __init_utils.initialize_queue(tasks=tasks, qtype=MultiThreadingQueueType.Queue)
        # Initialize parameter and object with different scenario.
        __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_instances_number)


    @deprecated(version="0.8", reason="Move the method up to super-class 'RunnableStrategy'")
    def initialize_queue(self, tasks: Iterable, qtype: BaseQueueType):
        __queue = self.init_tasks_queue(qtype=qtype)
        __tasks_queue = self.add_task_to_queue(queue=__queue, task=tasks)
        RunningGlobalize.queue(queue=__tasks_queue)


    @deprecated(version="0.8", reason="Move the method up to super-class 'RunnableStrategy'")
    def init_tasks_queue(self, qtype: BaseQueueType) -> Union[Process_Queue, Queue]:
        __running_api = RunningStrategyAPI(mode=self._Running_Mode)
        __queue = __running_api.queue(qtype=qtype)
        return __queue


    @deprecated(version="0.8", reason="Move the method up to super-class 'RunnableStrategy'")
    def add_task_to_queue(self, queue: Union[Process_Queue, Queue], task: Iterable) -> Union[Process_Queue, Queue]:
        for t in task:
            queue.put(t)
        return queue


    def build_multi_workers(self, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> List[Union[Thread, ApplyResult]]:
        print("function: ", function)
        print("args: ", args)
        print("kwargs: ", kwargs)
        self._Threads_List = [Thread(target=function, args=args, kwargs=kwargs) for _ in range(self.threads_number)]
        return self._Threads_List


    @deprecated(version="0.8", reason="Move the method up to super-class 'RunnableStrategy'")
    def initialize_persistence(self):
        pre_init_params: Dict = {}
        if isinstance(self._persistence_strategy, SingleConnection):
            pass
        elif isinstance(self._persistence_strategy, MultiConnections):
            pre_init_params["db_connection_instances_number"] = self.db_connection_instances_number
        elif isinstance(self._persistence_strategy, SingleFileSaver):
            pass
        elif isinstance(self._persistence_strategy, MultiFileSaver):
            pass
        else:
            # Unexpected scenario
            print("[DEBUG] issue ...")
            raise Exception
        print("[DEBUG] Pre-Init process start ....")
        self._persistence_strategy.initialize(mode=self._Running_Mode, **pre_init_params)


    def activate_worker(self, worker: Union[Thread, ApplyResult]) -> None:
        print("[DEBUG] start to run thread ...")
        worker.start()
        print("[DEBUG] has activate to run.")


    def end_multi_working(self) -> None:
        if isinstance(self._Threads_List, List) and isinstance(self._Threads_List[0], Thread):
            for threed_index in range(self.threads_number):
                self._Threads_List[threed_index].join()
        else:
            raise



@deprecated(version="0.8", reason="Move the class into module 'coroutine'")
class CoroutineStrategy(ConcurrentStrategy, Resultable):

    __Greenlet_List: List[greenlet] = None
    __Coroutine_Running_Result: List[object] = []

    def init_multi_working(self, tasks: Iterable, *args, **kwargs) -> None:
        # Initialize the Database Connection Instances Pool and Processes Semaphore.
        database_connections_pool = self._persistence_strategy.connect_database(pool_name="stock_crawler",
                                                                                pool_size=self.threads_number)
        DatabaseGlobalize.connection_pool(pool=database_connections_pool)

        threading_semaphore = ThreadingSemaphore(value=self.threads_number)
        RunningGlobalize.semaphore(smp=threading_semaphore)

        process_queue = self.init_tasks_queue()
        tasks_queue = self.add_task_to_queue(queue=process_queue, task=tasks)
        RunningGlobalize.tasks_queue(tasks_queue=tasks_queue)


    def init_tasks_queue(self) -> Union[Process_Queue, Queue]:
        return Queue()


    def add_task_to_queue(self, queue: Union[Process_Queue, Queue], task: Iterable) -> Union[Process_Queue, Queue]:
        for t in task:
            queue.put(t)
        return queue


    def build_multi_workers(self, function: Callable, *args, **kwargs) -> List[Union[greenlet, Thread, ApplyResult]]:
        self.__Greenlet_List = [greenlet(run=function) for _ in range(self.threads_number)]
        return self.__Greenlet_List


    def activate_worker(self, worker: Union[greenlet, Thread, ApplyResult]) -> None:
        value = worker.switch()
        self.__Coroutine_Running_Result.append(value)


    def end_multi_working(self) -> None:
        # if isinstance(self.__Greenlet_List, List) and isinstance(self.__Greenlet_List[0], greenlet):
        #     for threed_index in range(self.threads_number):
        #         self.__Greenlet_List[threed_index]
        # else:
        #     raise
        pass


    def get_multi_working_result(self) -> Iterable[object]:
        return self.__Coroutine_Running_Result

