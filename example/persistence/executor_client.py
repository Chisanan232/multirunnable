from typing import List
import time
import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_pyocean_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_pyocean_path)

# multirunnable package
from multirunnable import SimpleExecutor, PersistenceExecutor, QueueTask, RunningMode
from multirunnable.adapter import Lock, BoundedSemaphore
from multirunnable.parallel import ProcessQueueType, ParallelResult
from multirunnable.logger import ocean_logger

# code component
from dao import TestDao
from fao import ExampleFao



class ExampleExecutorClient:

    __Database_Config_Path = "Your database config path"

    __Worker_Number: int
    __DB_CONNECTION_Number: int

    def __init__(self, worker_num: int, db_conn_num: int):
        self.__Worker_Number = worker_num
        self.__DB_CONNECTION_Number = db_conn_num
        self.__logger = ocean_logger


    def main_run(self):
        test_dao = TestDao(db_driver="mysql", use_pool=False)

        __queue_task = QueueTask()
        __queue_task.name = "test_sql_task"
        __queue_task.queue_type = ProcessQueueType.Queue
        sql_query = "select * from stock_data_2330 limit 3;"
        __queue_task.value = [sql_query for _ in range(20)]

        # # # # Initial and instantiate feature object: Lock and Bounded Semaphore
        __lock = Lock()
        __bounded_semaphore = BoundedSemaphore(value=2)
        __features = __lock + __bounded_semaphore

        # # # # Initial and instantiate pool object with persistence strategy
        # __executor = PersistenceExecutor(
        #     # mode=RunningMode.Parallel,
        #     # mode=RunningMode.Concurrent,
        #     # mode=RunningMode.GreenThread,
        #     mode=RunningMode.Asynchronous,
        #     executors=self.__Worker_Number,
        #     persistence_strategy=self.persistence_strategy(),
        #     db_connection_pool_size=self.__DB_CONNECTION_Number)

        __executor = SimpleExecutor(
            mode=RunningMode.Parallel,
            # mode=RunningMode.Concurrent,
            # mode=RunningMode.GreenThread,
            # mode=RunningMode.Asynchronous,
            executors=self.__Worker_Number)

        __executor.run(
            function=test_dao.get_test_data,
            queue_tasks=__queue_task,
            features=__features
        )
        result = __executor.result()

        for r in result:
            print(f"+============ {r.worker_id} =============+")
            print("Result.pid: ", r.pid)
            print("Result.worker_id: ", r.worker_id)
            print("Result.state: ", r.state)
            print("Result.data: ", r.data)
            print("Result.exception: ", r.exception)
            print("+====================================+\n")

        # __fao = ExampleFao()
        # self.__logger.debug(f"Start to save data to file ....")
        # format_data = self.__only_data(result=result)
        # __fao.all_thread_one_file(data=format_data)
        # __fao.all_thread_one_file_in_archiver(data=format_data)
        # self.__logger.debug(f"Saving successfully!")


    def __only_data(self, result: List[ParallelResult]):
        new_data = []
        for d in result:
            data_rows = d.data["data"]
            for data_row in data_rows:
                new_data.append(data_row)
        return new_data


    def __done(self) -> None:
        end_time = time.time()
        self.__logger.info(f"Total taking time: {end_time - start_time} seconds")



if __name__ == '__main__':

    start_time = time.time()
    __workers_number = 1
    __db_connection_number = 1

    __executor_client = ExampleExecutorClient(worker_num=__workers_number, db_conn_num=__db_connection_number)
    __executor_client.main_run()
