from multirunnable.api import RunWith, AsyncRunWith, QueueOperator
from multirunnable.persistence.database.strategy import BaseDatabaseConnection
from multirunnable.persistence.database.operator import DatabaseOperator
from multirunnable.persistence.database.layer import BaseDao

from db_mysql import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator

import logging



class TestingDao(BaseDao):

    def __init__(self, db_driver=None, use_pool=False):
        self.db_driver = db_driver
        self.use_pool = use_pool

        # Initial and connect to database and get connection, cursor (or session) instance
        self._database_config = {
            "host": "127.0.0.1",
            # "host": "172.17.0.6",
            "port": "3306",
            "user": "root",
            "password": "password",
            "database": "tw_stock"
        }
        """
        Note:
            Target variable:
                self._database_opts

            Something note about parallel: 
                * Question 1: 
                Is it possible that the current instance instantiates the 
                class object which is 'Singleton Pattern' whose IDs are different? 
                Just think it as a hardware level concept, each instance will be save at 
                a memory place for temporary after it has been instantiated by others objects.
                However, right now it has a general object and more than 2 object with 'Singleton Pattern' 
                and the general object instantiates others 2 Singleton object. 

                * Possible Answer: 
                1.  Because singleton, no matter how many it be instantiated, it ONLY return one and the same instance back to outside.
                2. For many process, it still instantiate them so many times and gets so many different instances.
        """

        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)


    def _instantiate_strategy(self) -> BaseDatabaseConnection:
        if self.db_driver == "mysql":
            # from db_mysql import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator
            if self.use_pool is True:
                db_conn_strategy = MySQLDriverConnectionPool(**self._database_config)
            else:
                db_conn_strategy = MySQLSingleConnection(**self._database_config)
            return db_conn_strategy
        else:
            raise ValueError


    def _instantiate_database_opts(self, strategy: BaseDatabaseConnection) -> DatabaseOperator:
        _database_opts = MySQLOperator(conn_strategy=strategy)
        return _database_opts



class TestDao(TestingDao):

    def get_test_data(self) -> object:
        """
        Note (?) need to consider:
            How to abstractilize the logic or how to be more clear ?
        :return:
        """
        data = self.sql_process_with_lock()
        # data = self.sql_process_with_semaphore()
        self._logger.debug(f"at fun 'run': {data}")
        return data


    @RunWith.Lock
    def sql_process_with_lock(self):
        import multiprocessing as mp

        self._logger.debug("Running all things with Lock.")
        # sql_tasks = self.get_all_sql_tasks()
        sql_tasks = QueueOperator.get_queue_with_name(name="test_sql_task")
        self._logger.debug(f"SQL tasks: {sql_tasks} - {mp.current_process()}")
        one_sql_query = sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {one_sql_query} - {mp.current_process()}")
        self.execute(one_sql_query)
        data = self.fetch_all()
        return data


    @RunWith.Bounded_Semaphore
    def sql_process_with_semaphore(self):
        import multiprocessing as mp

        self._logger.debug("Running all things with Bounded Semaphore.")
        # sql_tasks = self.get_all_sql_tasks()
        sql_tasks = QueueOperator.get_queue_with_name(name="test_sql_task")
        self._logger.debug(f"SQL tasks: {sql_tasks} - {mp.current_process()}")
        one_sql_query = sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {one_sql_query} - {mp.current_process()}")
        self.execute(one_sql_query)
        data = self.fetch_all()
        return data



class AsyncTestDao(TestingDao):

    async def get_test_data(self) -> object:
        """
        Note (?) need to consider:
            How to abstractilize the logic or how to be more clear ?
        :return:
        """
        data = await self.sql_process_with_lock()
        # data = self.sql_process_with_semaphore()
        self._logger.debug(f"at fun 'run': {data}")
        return data


    @AsyncRunWith.Lock
    async def sql_process_with_lock(self):
        import multiprocessing as mp

        self._logger.debug("Running all things with Lock.")
        # sql_tasks = self.get_all_sql_tasks()
        sql_tasks = QueueOperator.get_queue_with_name(name="test_sql_task")
        self._logger.debug(f"SQL tasks: {sql_tasks} - {mp.current_process()}")
        one_sql_query = await sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {one_sql_query} - {mp.current_process()}")
        self.execute(one_sql_query)
        data = self.fetch_all()
        return data


    @AsyncRunWith.Bounded_Semaphore
    async def sql_process_with_semaphore(self):
        import multiprocessing as mp

        self._logger.debug("Running all things with Bounded Semaphore.")
        # sql_tasks = self.get_all_sql_tasks()
        sql_tasks = QueueOperator.get_queue_with_name(name="test_sql_task")
        self._logger.debug(f"SQL tasks: {sql_tasks} - {mp.current_process()}")
        one_sql_query = await sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {one_sql_query} - {mp.current_process()}")
        self.execute(one_sql_query)
        data = self.fetch_all()
        return data
