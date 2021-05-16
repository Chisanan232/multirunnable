# Import package pyocean
import pathlib
import sys
import os

# package_pyocean_path = os.path.join(str(pathlib.Path(__file__).parent.parent.absolute()), "pyocean")
package_pyocean_path = str(pathlib.Path(__file__).parent.parent.absolute())
print(package_pyocean_path)
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean.framework.factory import RunningFactory, RunningTask
from pyocean.framework.strategy import RunnableStrategy
from pyocean.framework.builder import BaseBuilder
from pyocean.persistence.interface import OceanPersistence
from pyocean.persistence.database.access_object import BaseDao
from pyocean.parallel.builder import ParallelBuilder
from pyocean.parallel.strategy import ParallelStrategy, MultiProcessingStrategy
from pyocean.parallel.factory import ParallelFactory
from pyocean.concurrent.builder import ThreadsBuilder, GreenletBuilder, ConcurrentBuilder
from pyocean.concurrent.strategy import MultiThreadingStrategy, CoroutineStrategy
from pyocean.concurrent.factory import MultiThreadsFactory, CoroutineFactory
from pyocean.persistence.database.configuration import DatabaseConfig, DatabaseDriver, HostEnvType
from pyocean.logging.level import LogLevel, Logger

# code component
from connection_strategy import SingleTestConnectionStrategy, MultiTestConnectionStrategy
from dao import DatabaseSqlQuery, TestDao
from sql_query import SqlQuery

from multiprocessing import cpu_count
import time

from deprecated.sphinx import deprecated



class TestParallelBuilder(ParallelBuilder):

    def __init__(self, running_strategy: ParallelStrategy, db_connection_number: int, logger: Logger):
        super().__init__(running_strategy=running_strategy)
        self.__db_connection_number = db_connection_number
        self.__logger = logger



@deprecated(version="0.4", reason="Unify the concurrent part like threading, greenlet and gevent. Please change to use 'ConcurrentBuilder'")
class TestThreadBuilder(ThreadsBuilder):

    def __init__(self, running_strategy: ParallelStrategy, db_connection_number: int, logger: Logger):
        super().__init__(running_strategy=running_strategy)
        self.__db_connection_number = db_connection_number
        self.__logger = logger



@deprecated(version="0.4", reason="Unify the concurrent part like threading, greenlet and gevent. Please change to use 'ConcurrentBuilder'")
class TestGreenletBuilder(GreenletBuilder):

    def __init__(self, running_strategy: ParallelStrategy, db_connection_number: int, logger: Logger):
        super().__init__(running_strategy=running_strategy)
        self.__db_connection_number = db_connection_number
        self.__logger = logger



class TestConcurrentBuilder(ConcurrentBuilder):

    def __init__(self, running_strategy: ParallelStrategy, db_connection_number: int, logger: Logger):
        super().__init__(running_strategy=running_strategy)
        self.__db_connection_number = db_connection_number
        self.__logger = logger



class TestFactory(RunningFactory):

    def __init__(self, process_number: int, db_connection_number: int, logger):
        super().__init__(process_number, db_connection_number)
        self.__logger = logger


    def running_builder(self, running_strategy: RunnableStrategy) -> BaseBuilder:
        # # Multiprocessing (Parallel)
        test_builder = TestParallelBuilder(running_strategy=running_strategy,
                                           db_connection_number=self._db_connection_num,
                                           logger=self.__logger)
        # # Multithreading
        # test_builder = TestThreadBuilder(running_strategy=running_strategy,
        #                                  db_connection_number=self.__db_connection_num,
        #                                  logger=self.__logger)
        # # Coroutine (greenlet)
        # test_builder = TestGreenletBuilder(running_strategy=running_strategy,
        #                                    db_connection_number=self.__db_connection_num,
        #                                    logger=self.__logger)
        # # Concurrent
        # test_builder = TestConcurrentBuilder(running_strategy=running_strategy,
        #                                      db_connection_number=self.__db_connection_num,
        #                                      logger=self.__logger)
        return test_builder


    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        # # Multiprocessing
        running_strategy = MultiProcessingStrategy(threads_num=self._process_num,
                                                   db_connection_pool_size=self._db_connection_num,
                                                   persistence_strategy=persistence_strategy)
        # # Multithreading
        # running_strategy = MultiThreadingStrategy(threads_num=self.__process_num,
        #                                           db_connection_pool_size=self.__db_connection_num,
        #                                           persistence_strategy=connection_strategy)
        # # Coroutine (greenlet)
        # running_strategy = CoroutineStrategy(threads_num=self.__process_num,
        #                                      db_connection_pool_size=self.__db_connection_num,
        #                                      persistence_strategy=connection_strategy)
        return running_strategy


    def persistence_strategy(self) -> OceanPersistence:
        connection_strategy = MultiTestConnectionStrategy(configuration=DatabaseConfig, logging=self.__logger)
        # connection_strategy = SingleTestConnectionStrategy(configuration=DatabaseConfig, logging=self.__logger)
        # deprecated
        # connection_strategy = MultiTestConnectionStrategy(configuration=DatabaseConfig, thread_num=self._db_connection_num, logging=self.__logger)
        return connection_strategy


    def dao(self, connection_strategy: OceanPersistence) -> BaseDao:
        # sql_query_obj = DatabaseSqlQuery(strategy=connection_strategy, logger=self.__logger)
        sql_query_obj = TestDao(connection_strategy=connection_strategy, logger=self.__logger)
        return sql_query_obj



class TestParallelFactory(ParallelFactory):

    def __init__(self, process_number: int, db_connection_number: int, logger: Logger):
        super().__init__(process_number, db_connection_number)
        self.__logger = logger


    def running_builder(self, running_strategy: RunnableStrategy) -> BaseBuilder:
        test_builder = TestParallelBuilder(running_strategy=running_strategy,
                                           db_connection_number=self._db_connection_num,
                                           logger=self.__logger)
        return test_builder


    def persistence_strategy(self) -> OceanPersistence:
        print("[DEBUG] start init connection strategy. pid - ", os.getpid())
        connection_strategy = MultiTestConnectionStrategy(
            configuration=DatabaseConfig(database_driver=DatabaseDriver.MySQL, host_type=HostEnvType.Localhost),
            logging=self.__logger)
        # connection_strategy = SingleTestConnectionStrategy(
        #     configuration=DatabaseConfig(database_driver=DatabaseDriver.MySQL, host_type=HostEnvType.Localhost),
        #     logging=self.__logger)
        print("[DEBUG] end init connection strategy. pid - ", os.getpid())
        return connection_strategy


    def dao(self, connection_strategy: OceanPersistence) -> BaseDao:
        # sql_query_obj = DatabaseSqlQuery(strategy=connection_strategy, logger=self.__logger)
        sql_query_obj = TestDao(connection_strategy=connection_strategy, logger=self.__logger)
        return sql_query_obj



class TestMultiThreadFactory(MultiThreadsFactory):

    def __init__(self, process_number: int, db_connection_number: int, logger):
        super().__init__(process_number, db_connection_number)
        self.__logger = logger


    def running_builder(self, running_strategy: RunnableStrategy) -> BaseBuilder:
        test_builder = TestConcurrentBuilder(running_strategy=running_strategy,
                                             db_connection_number=self.__db_connection_num,
                                             logger=self.__logger)
        return test_builder


    def persistence_strategy(self) -> OceanPersistence:
        connection_strategy = MultiTestConnectionStrategy(
            configuration=DatabaseConfig(database_driver=DatabaseDriver.MySQL, host_type=HostEnvType.Localhost),
            logging=self.__logger)
        # connection_strategy = SingleTestConnectionStrategy(
        #     configuration=DatabaseConfig(database_driver=DatabaseDriver.MySQL, host_type=HostEnvType.Localhost),
        #     logging=self.__logger)
        return connection_strategy


    def dao(self, connection_strategy: OceanPersistence) -> BaseDao:
        # sql_query_obj = DatabaseSqlQuery(strategy=connection_strategy, logger=self.__logger)
        sql_query_obj = TestDao(connection_strategy=connection_strategy, logger=self.__logger)
        return sql_query_obj



class TestCoroutineFactory(CoroutineFactory):

    def __init__(self, process_number: int, db_connection_number: int, logger):
        super().__init__(process_number, db_connection_number)
        self.__logger = logger


    def running_builder(self, running_strategy: RunnableStrategy) -> BaseBuilder:
        test_builder = TestConcurrentBuilder(running_strategy=running_strategy,
                                             db_connection_number=self._db_connection_num,
                                             logger=self.__logger)
        return test_builder


    def persistence_strategy(self) -> OceanPersistence:
        connection_strategy = MultiTestConnectionStrategy(
            configuration=DatabaseConfig(database_driver=DatabaseDriver.MySQL, host_type=HostEnvType.Localhost),
            logging=self.__logger)
        # connection_strategy = SingleTestConnectionStrategy(
        #     configuration=DatabaseConfig(database_driver=DatabaseDriver.MySQL, host_type=HostEnvType.Localhost),
        #     logging=self.__logger)
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
        self.__logger = Logger(level=log_level, file_path=None)


    def run(self):
        """
        Note:
            There is a question needs to consider:
               What rule does the DAO be in here?
        :return:
        """
        # Initial running factory
        # # Parallel Factory
        # test_factory = TestParallelFactory(process_number=self.__process_num,
        #                                    db_connection_number=self.__db_connection_number,
        #                                    logger=self.__logger)
        # # Coroutine Factory
        test_factory = TestCoroutineFactory(process_number=self.__process_num,
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
        self.__logger.info_level_log(f"Total taking time: {end_time - start_time} seconds")


if __name__ == '__main__':

    start_time = time.time()
    __process_number = 1
    __db_connection_thread_number = 1
    print(f"Process Number: {cpu_count()}")
    test_code = TestCode(process_num=__process_number,
                         db_connection_number=__db_connection_thread_number,
                         log_level=LogLevel.DEBUG)
    test_code.run()
