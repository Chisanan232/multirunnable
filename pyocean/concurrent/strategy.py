from ..framework.strategy import RunnableStrategy, Resultable, Globalize as RunningGlobalize
from ..framework.features import BaseQueueType
from ..persistence.database.multi_connections import Globalize as DatabaseGlobalize

from multiprocessing.pool import ApplyResult
from multiprocessing.queues import Queue as Process_Queue
from queue import Queue
from threading import Thread, Semaphore as ThreadingSemaphore
from greenlet import greenlet

from abc import ABCMeta, abstractmethod, ABC
from typing import List, Tuple, Dict, Iterable, Union, Callable



class ConcurrentStrategy(RunnableStrategy, ABC):

    pass



class MultiThreadingStrategy(ConcurrentStrategy):

    __Threads_List: List[Thread] = None

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


    def init_tasks_queue(self, qtype: BaseQueueType) -> Union[Process_Queue, Queue]:
        return Queue()


    def add_task_to_queue(self, queue: Union[Process_Queue, Queue], task: Iterable) -> Union[Process_Queue, Queue]:
        for t in task:
            queue.put(t)
        return queue


    def build_multi_workers(self, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> List[Union[Thread, ApplyResult]]:
        print("function: ", function)
        print("args: ", args)
        print("kwargs: ", kwargs)
        self.__Threads_List = [Thread(target=function, args=args, kwargs=kwargs) for _ in range(self.threads_number)]
        return self.__Threads_List


    def activate_worker(self, worker: Union[Thread, ApplyResult]) -> None:
        print("[DEBUG] start to run thread ...")
        worker.start()
        print("[DEBUG] has activate to run.")


    def end_multi_working(self) -> None:
        if isinstance(self.__Threads_List, List) and isinstance(self.__Threads_List[0], Thread):
            for threed_index in range(self.threads_number):
                self.__Threads_List[threed_index].join()
        else:
            raise



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

