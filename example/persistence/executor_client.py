from typing import List
import logging
import time
import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_multirunnable_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_multirunnable_path)

# multirunnable package
from multirunnable import SimpleExecutor, QueueTask, RunningMode
from multirunnable.factory import LockFactory, BoundedSemaphoreFactory
from multirunnable.parallel import Queue as Process_Queue
from multirunnable.concurrent import Thread_Queue
from multirunnable.coroutine import Greenlet_Queue
from multirunnable.persistence.file import SavingStrategy

# code component
from dao import TestDao, AsyncTestDao
from fao import TestFao



class ExampleExecutorClient:

    __Worker_Number: int

    def __init__(self, worker_num: int):
        self.__Worker_Number = worker_num
        self.__logger = logging.getLogger(self.__class__.__name__)


    def main_run(self):
        test_dao = TestDao(db_driver="mysql", use_pool=False)
        # test_dao = AsyncTestDao(db_driver="mysql", use_pool=False)

        # # # # Initial and instantiate feature object: Queue Task, Lock and Bounded Semaphore
        _queue_task = self.__init_queue()
        _features = self.__init_features()

        _executor = SimpleExecutor(
            mode=RunningMode.Parallel,
            # mode=RunningMode.Concurrent,
            # mode=RunningMode.GreenThread,
            # mode=RunningMode.Asynchronous,
            executors=self.__Worker_Number)

        _executor.run(
            function=test_dao.get_test_data,
            queue_tasks=_queue_task,
            features=_features
        )
        result = _executor.result()

        for r in result:
            print(f"+============ {r.worker_ident} =============+")
            print("Result.pid: ", r.pid)
            print("Result.worker_id: ", r.worker_ident)
            print("Result.worker_name: ", r.worker_name)
            print("Result.state: ", r.state)
            print("Result.data: ", r.data)
            print("Result.exception: ", r.exception)
            print("+====================================+\n")

        self.__save_to_files(result=result)

        end_time = time.time()
        self.__logger.info(f"Total taking time: {end_time - start_time} seconds")


    def __init_queue(self):
        _queue_task = QueueTask()
        _queue_task.name = "test_sql_task"
        _queue_task.queue_instance = Process_Queue()
        # _queue_task.queue_instance = Thread_Queue
        # _queue_task.queue_instance = Greenlet_Queue
        sql_query = "select * from stock_data_2330 limit 3;"
        _queue_task.value = [sql_query for _ in range(20)]
        return _queue_task


    def __init_features(self):
        _lock = LockFactory()
        _bounded_semaphore = BoundedSemaphoreFactory(value=2)
        _features = _lock + _bounded_semaphore
        return _features


    def __save_to_files(self, result):
        __fao = TestFao(strategy=SavingStrategy.ALL_THREADS_ONE_FILE)
        self.__logger.debug(f"Start to save data to file ....")
        _final_data = ExampleExecutorClient._only_data(result=result)
        print("[FINAL] format_data: ", _final_data)
        __fao.save_as_csv(mode="a+", file="testing.csv", data=_final_data)
        __fao.save_as_excel(mode="a+", file="testing.xlsx", data=_final_data)
        __fao.save_as_json(mode="a+", file="testing.json", data=_final_data)
        self.__logger.debug(f"Saving successfully!")


    @staticmethod
    def _only_data(result: List):
        new_data = []
        for d in result:
            data_rows = d.data
            for data_row in data_rows:
                new_data.append(data_row)
        return new_data



if __name__ == '__main__':

    start_time = time.time()
    __workers_number = 3

    __executor_client = ExampleExecutorClient(worker_num=__workers_number)
    __executor_client.main_run()
