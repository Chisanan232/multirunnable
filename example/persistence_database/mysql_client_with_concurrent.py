# Import package pyocean
import pathlib
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean.framework import PersistenceRunnableTask
from pyocean.concurrent import ConcurrentSimpleFactory, ConcurrentPersistenceFactory
from pyocean.persistence import OceanPersistence
from pyocean.persistence.database import BaseDao
from pyocean.persistence.database.configuration import DatabaseConfig, DatabaseDriver
from pyocean.logger import ocean_logger

# code component
from connection_strategy import SingleTestConnectionStrategy, MultiTestConnectionStrategy
from dao import TestDao

from multiprocessing import cpu_count
import time



class TestMultiThreadFactory(ConcurrentPersistenceFactory):

    __Database_Config_Path = "Your properties file path"

    def __init__(self, workers_number: int, db_connection_number: int):
        super().__init__(workers_number, db_connection_number)
        self.__logger = ocean_logger


    def persistence_strategy(self) -> OceanPersistence:
        connection_strategy = MultiTestConnectionStrategy(
            configuration=DatabaseConfig(config_path=self.__Database_Config_Path, database_driver=DatabaseDriver.MySQL)
        )
        # connection_strategy = SingleTestConnectionStrategy(
        #     configuration=DatabaseConfig(config_path=self.__Database_Config_Path, database_driver=DatabaseDriver.MySQL),
        # )
        return connection_strategy


    def dao(self, connection_strategy: OceanPersistence) -> BaseDao:
        # sql_query_obj = DatabaseSqlQuery(strategy=connection_strategy)
        sql_query_obj = TestDao(connection_strategy=connection_strategy)
        return sql_query_obj



class TestCode:

    __Strategy: MultiTestConnectionStrategy = None

    def __init__(self, process_num: int, db_connection_number: int):
        self.__process_num: int = process_num
        self.__db_connection_number: int = db_connection_number

        self.__logger = ocean_logger


    def run(self):
        """
        Note:
            There is a question needs to consider:
               What rule does the DAO be in here?
        :return:
        """
        # Initial running factory
        test_factory = TestMultiThreadFactory(workers_number=self.__process_num,
                                              db_connection_number=self.__db_connection_number)
        # Initial running task object
        test_task = PersistenceRunnableTask(factory=test_factory)
        # Generate a running builder to start a multi-worker program
        # (it may be a multiprocessing, multithreading or multi-greenlet, etc.)
        test_task_procedure = test_task.generate()

        # Initial target tasks
        # sql_query = "select * from limited_company limit 3;"
        sql_query = "select * from stock_data_2330 limit 3;"
        sql_tasks = [sql_query for _ in range(20)]
        test_dao = test_factory.dao(connection_strategy=test_task.running_persistence())
        test_task_procedure.run(function=test_dao.get_test_data, tasks=sql_tasks)


    def __done(self) -> None:
        end_time = time.time()
        self.__logger.info(f"Total taking time: {end_time - start_time} seconds")


if __name__ == '__main__':

    start_time = time.time()
    __process_number = 5
    __db_connection_thread_number = 5
    print(f"Process Number: {cpu_count()}")
    test_code = TestCode(process_num=__process_number,
                         db_connection_number=__db_connection_thread_number)
    test_code.run()
