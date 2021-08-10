import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
gevent.monkey.patch_thread()

from abc import ABCMeta, abstractmethod
from typing import List
from enum import Enum
from multiprocessing import Pool
from multiprocessing.pool import AsyncResult
from threading import Thread, Lock
# from gevent import greenlet
import greenlet
import asyncio
import gevent



class TestKafka(metaclass=ABCMeta):

    @abstractmethod
    def kafka_process(self, **kwargs) -> None:
        pass



class MultiWorker(metaclass=ABCMeta):

    KAFKA_STRATEGY: TestKafka = None

    def __init__(self, worker_number: int, kafka_strategy: TestKafka):
        self._worker_num = worker_number
        self.KAFKA_STRATEGY = kafka_strategy


    @abstractmethod
    def run_process(self) -> None:
        pass



class ProcessingWorker(MultiWorker):

    def run_process(self) -> None:
        __pool = Pool(processes=self._worker_num)
        __process_list: List[AsyncResult] = [__pool.apply_async(func=self.KAFKA_STRATEGY.kafka_process) for _ in range(self._worker_num)]

        for process in __process_list:
            __result = process.get()
            __successful = process.successful()



class ThreadingWorker(MultiWorker):

    def run_process(self) -> None:
        __thread_list: List[Thread] = [Thread(target=self.KAFKA_STRATEGY.kafka_process) for _ in range(self._worker_num)]

        for thread in __thread_list:
            thread.start()

        for thread in __thread_list:
            thread.join()


lock = Lock()


class GreenletWorker(MultiWorker):

    def run_process(self) -> None:
        __greenlet_list: List[greenlet.greenlet] = [greenlet.greenlet(self.KAFKA_STRATEGY.kafka_process) for _ in range(self._worker_num)]
        for __one_greenlet in __greenlet_list:
            with lock:
                __one_greenlet.switch()



class GeventWorker(MultiWorker):

    def run_process(self) -> None:
        __greenlet_list: List[gevent.greenlet] = [gevent.spawn(self.KAFKA_STRATEGY.kafka_process) for _ in range(self._worker_num)]
        gevent.joinall(__greenlet_list)



class AsyncWorker(MultiWorker):

    __Even_Loop = asyncio.get_event_loop()

    def run_process(self) -> None:
        self.run_process()


    async def __run_multi_worker(self) -> None:
        tasks = [self.__Even_Loop.create_task(self.kafka_process()) for _ in range(self._worker_num)]
        finished, unfinished = await asyncio.wait(tasks)
        print(f"Finished: {finished}. \nUnfinished: {unfinished}.")
        for finish in finished:
            event_loop = finish.get_loop()
            exception = finish.exception()
            done_flag = finish.close()
            result_flag = finish.result()
            # if result_flag == "Greenlet-8":
            #     finish.set_result(result={"test": "test_1"})
            #     result_flag = finish.result()
            print(f"+----------------------------------------------------+ \n"
                  f"This is something report for the coroutine done: \n"
                  f"event loop: {event_loop} \n"
                  f"exception: {exception} \n"
                  f"done_flag: {done_flag} \n"
                  f"result_flag: {result_flag} \n"
                  f"+----------------------------------------------------+")


    # @asyncio.coroutine
    async def kafka_process(self, **kwargs) -> bool:
        try:
            self.KAFKA_STRATEGY.kafka_process(**kwargs)
        except Exception as e:
            return False
        else:
            return True



class Strategy(Enum):

    Processing = ProcessingWorker
    Threading = ThreadingWorker
    Greenlet = GreenletWorker
    Async = AsyncWorker



class EnterPoint:

    @staticmethod
    def run(running_strategy: Strategy, kafka_strategy: TestKafka, worker_number: int = 1):
        __strategy = running_strategy.value
        __thread_worker = __strategy(worker_number=worker_number, kafka_strategy=kafka_strategy)
        __thread_worker.run_process()

