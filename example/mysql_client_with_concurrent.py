# Import package pyocean
import pathlib
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean.framework.factory import RunningFactory, RunningTask
from pyocean.framework import BaseBuilder, RunnableStrategy
from pyocean.concurrent import ThreadsBuilder, MultiThreadsFactory
from pyocean.persistence import OceanPersistence
from pyocean.persistence.database import BaseDao
from pyocean.persistence.database.configuration import DatabaseConfig, DatabaseDriver, HostEnvType
from pyocean.logger import LogLevel, LoggingConfig, OceanLogger, KafkaHandler

# code component
from connection_strategy import SingleTestConnectionStrategy, MultiTestConnectionStrategy
from dao import TestDao
from sql_query import SqlQuery

from multiprocessing import cpu_count
from logging import FileHandler, StreamHandler
import time

from deprecated.sphinx import deprecated



class TestThreadBuilder(ThreadsBuilder):

    def __init__(self, running_strategy: RunnableStrategy, db_connection_number: int, logger: OceanLogger):
        super().__init__(running_strategy=running_strategy)
        self.__db_connection_number = db_connection_number
        self.__logger = logger



class TestMultiThreadFactory(MultiThreadsFactory):

    def __init__(self, process_number: int, db_connection_number: int, logger):
        super().__init__(process_number, db_connection_number)
        self.__logger = logger


    def running_builder(self, running_strategy: RunnableStrategy) -> BaseBuilder:
        test_builder = TestThreadBuilder(running_strategy=running_strategy,
                                         db_connection_number=self._db_connection_num,
                                         logger=self.__logger)
        return test_builder


    def persistence_strategy(self) -> OceanPersistence:
        connection_strategy = MultiTestConnectionStrategy(
            configuration=DatabaseConfig(database_driver=DatabaseDriver.MySQL, host_type=HostEnvType.Localhost),
            logger=self.__logger)
        # connection_strategy = SingleTestConnectionStrategy(
        #     configuration=DatabaseConfig(database_driver=DatabaseDriver.MySQL, host_type=HostEnvType.Localhost),
        #     logger=self.__logger)
        return connection_strategy


    def dao(self, connection_strategy: OceanPersistence) -> BaseDao:
        # sql_query_obj = DatabaseSqlQuery(strategy=connection_strategy, logger=self.__logger)
        sql_query_obj = TestDao(connection_strategy=connection_strategy, logger=self.__logger)
        return sql_query_obj



class TestCode:

    __Strategy: MultiTestConnectionStrategy = None

    def __init__(self, process_num: int, db_connection_number: int, log_level: LogLevel = LogLevel.INFO):
        self.__process_num: int = process_num
        self.__db_connection_number: int = db_connection_number

        # # Initialize Logger configuration
        __logging_config = LoggingConfig()
        __logging_config.level = LogLevel.DEBUG
        # # Initialize Logger handler
        sys_stream_hdlr = StreamHandler()
        file_io_hdlr = FileHandler(filename="/Users/bryantliu/Downloads/test_new.log")
        __producer_config = {"bootstrap_servers": "localhost:9092"}
        __sender_config = {"topic": "logging_test", "key": "test"}
        # kafka_stream_hdlr = KafkaHandler(producer_configs=__producer_config, sender_configs=__sender_config)
        # # Initialize Logger instance
        self.__logger = OceanLogger(config=__logging_config, handlers=[sys_stream_hdlr])
        self.__logger.debug(f"first init logging, level is {log_level}")
        print("[DEBUG] new class TestCode (including  logging)")


    def run(self):
        """
        Note:
            There is a question needs to consider:
               What rule does the DAO be in here?
        :return:
        """
        # Initial running factory
        test_factory = TestMultiThreadFactory(process_number=self.__process_num,
                                              db_connection_number=self.__db_connection_number,
                                              logger=self.__logger)
        # Initial running task object
        test_task = RunningTask(process_number=self.__process_num,
                                db_connection_number=self.__db_connection_number,
                                factory=test_factory)
        # Generate a running builder to start a multi-worker program
        # (it may be a multiprocessing, multithreading or multi-greenlet, etc.)
        test_task_builder = test_task.generate()

        # Initial target tasks
        sql_tasks = [SqlQuery.GET_STOCK_DATA.value for _ in range(20)]
        test_dao = test_factory.dao(connection_strategy=test_task.persistence())
        test_task_builder.run(function=test_dao.run, tasks=sql_tasks)


    def __done(self) -> None:
        end_time = time.time()
        self.__logger.info(f"Total taking time: {end_time - start_time} seconds")


if __name__ == '__main__':

    start_time = time.time()
    __process_number = 1
    __db_connection_thread_number = 1
    print(f"Process Number: {cpu_count()}")
    test_code = TestCode(process_num=__process_number,
                         db_connection_number=__db_connection_thread_number,
                         log_level=LogLevel.DEBUG)
    test_code.run()
