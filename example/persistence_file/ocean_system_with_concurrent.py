# Import package pyocean
from typing import List
import pathlib
import sys
import time

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean import OceanSystem, OceanTask, QueueTask
from pyocean.concurrent import MultiThreadingQueueType, ConcurrentResult
from pyocean.api import RunningMode, Feature
from pyocean.persistence import OceanPersistence, DatabaseDriver
from pyocean.persistence.database import DatabaseConfig
from pyocean.logger import ocean_logger

# code component
from connection_strategy import SingleTestConnectionStrategy, MultiTestConnectionStrategy
from dao import TestDao
from fao import ExampleFao



class ExampleOceanSystem:

    __Database_Config_Path = "Your database config path"

    __Concurrent_Number = 5

    def __init__(self):
        self.__logger = ocean_logger


    def main_run(self):
        test_dao = TestDao(connection_strategy=self.persistence_strategy())

        __task = OceanTask(mode=RunningMode.Parallel)
        __task.set_function(function=test_dao.get_test_data)

        __queue_task = QueueTask()
        __queue_task.name = "test_sql_task"
        __queue_task.queue_type = MultiThreadingQueueType.Queue
        sql_query = "select * from stock_data_2330 limit 3;"
        __queue_task.value = [sql_query for _ in range(20)]

        __system = OceanSystem(mode=RunningMode.Concurrent, worker_num=self.__Concurrent_Number)
        # result: List[ConcurrentResult] = __system.run_and_save(
        #     task=__task,
        #     queue_tasks=[__queue_task],
        #     features=[Feature.Bounded_Semaphore],
        #     persistence_strategy=self.persistence_strategy(),
        #     db_connection_num=self.__Parallel_Number
        # )
        result: List[ConcurrentResult] = __system.run_and_save(
            task=__task,
            queue_tasks=[__queue_task],
            features=[Feature.Bounded_Semaphore],
            persistence_strategy=self.persistence_strategy(),
            db_connection_num=self.__Concurrent_Number,
            saving_mode=True
        )
        print("Concurrent result: ", result)
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


    def __only_data(self, result: List[ConcurrentResult]):
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
    __process_number = 5
    __db_connection_thread_number = 5

    __example_system = ExampleOceanSystem()
    __example_system.main_run()
