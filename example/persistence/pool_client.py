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
from multirunnable import SimplePool, QueueTask, RunningMode
from multirunnable.factory import LockFactory, BoundedSemaphoreFactory
from multirunnable.parallel import Queue
from multirunnable.persistence.file import SavingStrategy

# code component
from dao import TestDao
from fao import TestFao



class ExamplePoolClient:

    __Pool_Size: int

    def __init__(self, worker_num: int):
        self.__Pool_Size = worker_num
        self.__logger = logging.getLogger(self.__class__.__name__)


    def main_run(self):
        # test_dao = TestDao(connection_strategy=self.persistence_strategy())
        test_dao = TestDao(db_driver="mysql", use_pool=False)

        # # # # Initial and instantiate feature object: Queue Task, Lock and Bounded Semaphore
        _queue_task = self.__init_queue()
        _features = self.__init_features()

        _pool = SimplePool(
            mode=RunningMode.Parallel,
            # mode=RunningMode.Concurrent,
            # mode=RunningMode.GreenThread,
            pool_size=self.__Pool_Size)

        _pool.initial(queue_tasks=_queue_task, features=_features)
        _pool.async_apply(function=test_dao.get_test_data, tasks_size=self.__Pool_Size)
        result = _pool.get_result()

        print("Result: ", result)
        for r in result:
            print(f"+====================================+")
            print("Result.data: ", r.data)
            print("Result.is_successful: ", r.is_successful)
            print("+====================================+\n")

        self.__save_to_files(result=result)

        end_time = time.time()
        self.__logger.info(f"Total taking time: {end_time - start_time} seconds")


    def __init_queue(self):
        _queue_task = QueueTask()
        _queue_task.name = "test_sql_task"
        _queue_task.queue_type = Queue()
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
        _final_data = ExamplePoolClient._only_data(result=result)
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
            for data_row in (data_rows or []):
                new_data.append(data_row)
        return new_data



if __name__ == '__main__':

    start_time = time.time()
    __workers_number = 3

    __pool_client = ExamplePoolClient(worker_num=__workers_number)
    __pool_client.main_run()
