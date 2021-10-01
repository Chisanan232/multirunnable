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
from multirunnable import PersistenceExecutor, QueueTask, RunningMode
from multirunnable.adapter import Lock, BoundedSemaphore
from multirunnable.coroutine import AsynchronousQueueType, AsynchronousResult
from multirunnable.persistence import OceanPersistence, DatabaseDriver
from multirunnable.persistence.database import DatabaseConfig
from multirunnable.logger import ocean_logger

# code component
from connection_strategy import SingleTestConnectionStrategy, MultiTestConnectionStrategy
from dao import AsyncTestDao
from fao import ExampleFao



class ExampleExecutorClient:

    __Database_Config_Path = "Your database config path"

    __Async_Number: int
    __DB_CONNECTION_Number: int

    def __init__(self, worker_num: int, db_conn_num: int):
        self.__Async_Number = worker_num
        self.__DB_CONNECTION_Number = db_conn_num
        self.__logger = ocean_logger


    def main_run(self):
        test_dao = AsyncTestDao(connection_strategy=self.persistence_strategy())

        __queue_task = QueueTask()
        __queue_task.name = "test_sql_task"
        __queue_task.queue_type = AsynchronousQueueType.Queue
        sql_query = "select * from stock_data_2330 limit 3;"
        __queue_task.value = [sql_query for _ in range(20)]

        # # # # Initial and instantiate feature object: Lock and Bounded Semaphore
        __lock = Lock()
        __bounded_semaphore = BoundedSemaphore(value=2)
        __features = __lock + __bounded_semaphore

        # # # # Initial and instantiate pool object with persistence strategy
        __executor = PersistenceExecutor(
            # mode=RunningMode.Parallel,
            # mode=RunningMode.Concurrent,
            # mode=RunningMode.GreenThread,
            mode=RunningMode.Asynchronous,
            executors=self.__Async_Number,
            persistence_strategy=self.persistence_strategy(),
            db_connection_pool_size=self.__DB_CONNECTION_Number)

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

        __fao = ExampleFao()
        self.__logger.debug(f"Start to save data to file ....")
        format_data = self.__only_data(result=result)
        __fao.all_thread_one_file(data=format_data)
        __fao.all_thread_one_file_in_archiver(data=format_data)
        self.__logger.debug(f"Saving successfully!")


    def persistence_strategy(self) -> OceanPersistence:
        connection_strategy = MultiTestConnectionStrategy(
            configuration=DatabaseConfig(config_path=self.__Database_Config_Path, database_driver=DatabaseDriver.MySQL))
        # connection_strategy = SingleTestConnectionStrategy(
        #     configuration=DatabaseConfig(config_path=self.__Database_Config_Path, database_driver=DatabaseDriver.MySQL))
        return connection_strategy


    def __only_data(self, result: List[AsynchronousResult]):
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
