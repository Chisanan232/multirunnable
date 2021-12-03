import time

from multirunnable.api import RunWith, AsyncRunWith, QueueOperator, RLockOperator
from multirunnable.persistence import BasePersistence
from multirunnable.persistence.database.operator import DatabaseOperator
from multirunnable.persistence.database.strategy import BaseSingleConnection, BaseConnectionPool
from multirunnable.persistence.database.layer import BaseDao
from multirunnable.logger import ocean_logger

from mysql.connector import Error
from mysql.connector.cursor import MySQLCursor
from typing import Dict, Tuple, Iterable, Callable, Union, Type, Generic
import threading
import datetime
import decimal
import os

from db_mysql import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator



class TestDao(BaseDao):

    # _database_opts = None

    def __init__(self, db_driver=None, use_pool=False, **kwargs):
        # super().__init__(connection_strategy=connection_strategy)
        super().__init__(**kwargs)
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
        self._database_opts = None
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

        self._logger = ocean_logger


    @property
    def database_opt(self) -> DatabaseOperator:
        import multiprocessing as mp
        print(f"TestDao:: Start to initial database operator instance. - {mp.current_process} - {datetime.datetime.now()}")

        if self._database_opts is None:
            print(f"TestDao:: It doesn't have the instance right now. - {mp.current_process} - {datetime.datetime.now()}")
            if self.db_driver == "mysql":
                # from db_mysql import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator
                if self.use_pool is True:
                    db_conn_strategy = MySQLDriverConnectionPool(**self._database_config)
                else:
                    db_conn_strategy = MySQLSingleConnection(**self._database_config)
                print(f"TestDao:: It gets the strategy instance. strategy: {db_conn_strategy} - {mp.current_process}")
                print(f"TestDao:: It gets the strategy instance. repr(strategy): {repr(db_conn_strategy)} - {mp.current_process}")
                print(f"TestDao:: ID of strategy instance: {id(db_conn_strategy)} - {mp.current_process}")
                self._database_opts = MySQLOperator(conn_strategy=db_conn_strategy)
                print(f"TestDao:: It gets the operator instance. operator: {self._database_opts} - {mp.current_process}")
                print(f"TestDao:: ID of operator instance: {id(self._database_opts)} - {mp.current_process}")

            elif self.db_driver == "postgre":
                from db_postgresql import PostgreSQLSingleConnection, PostgreSQLDriverConnectionPool, PostgreSQLOperator
                if self.use_pool is True:
                    db_conn_strategy = PostgreSQLDriverConnectionPool(**self._database_config)
                else:
                    db_conn_strategy = PostgreSQLSingleConnection(**self._database_config)
                self._database_opts = PostgreSQLOperator(conn_strategy=db_conn_strategy)

            elif self.db_driver == "cassandra":
                from db_cassandra import CassandraSingleConnection, CassandraDriverConnectionPool, CassandraOperator
                if self.use_pool is True:
                    db_conn_strategy = CassandraDriverConnectionPool(**self._database_config)
                else:
                    db_conn_strategy = CassandraSingleConnection(**self._database_config)
                self._database_opts = CassandraOperator(conn_strategy=db_conn_strategy)

            elif self.db_driver == "clickhouse":
                from db_clickhouse import ClickHouseSingleConnection, ClickHouseDriverConnectionPool, ClickHouseOperator
                if self.use_pool is True:
                    db_conn_strategy = ClickHouseDriverConnectionPool(**self._database_config)
                else:
                    db_conn_strategy = ClickHouseSingleConnection(**self._database_config)
                self._database_opts = ClickHouseOperator(conn_strategy=db_conn_strategy)

            else:
                raise ValueError("")
        else:
            print(f"TestDao:: Return instance directly because it already has it.")

        print(f"[DEBUG] ID of TestDao._database_opts: {id(self._database_opts)} - {mp.current_process()}")
        return self._database_opts


    def get_test_data(self) -> object:
        """
        Note (?) need to consider:
            How to abstractilize the logic or how to be more clear ?
        :return:
        """
        # self._logger.debug("Running all things with Lock.")
        self._logger.debug("Running all things with Bounded Semaphore.")
        data = self.sql_process()
        self._logger.debug(f"at fun 'run': {data}")
        return data


    @RunWith.Lock
    # @RunWith.Bounded_Semaphore
    def sql_process(self):
        import multiprocessing as mp
        # sql_tasks = self.get_all_sql_tasks()
        sql_tasks = QueueOperator.get_queue_with_name(name="test_sql_task")
        self._logger.debug(f"SQL tasks: {sql_tasks} - {mp.current_process()}")
        one_sql_query = sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {one_sql_query} - {mp.current_process()}")
        self.database_opt.execute(one_sql_query)
        data = self.database_opt.fetch_all()
        return data



class AsyncTestDao(BaseDao):

    def __init__(self, connection_strategy: BasePersistence):
        super().__init__(connection_strategy=connection_strategy)
        self._logger = ocean_logger


    @property
    def database_opt(self) -> Type[DatabaseOperator]:
        pass


    async def get_test_data(self) -> object:
        """
        Note (?) need to consider:
            How to abstractilize the logic or how to be more clear ?
        :return:
        """
        pass
        # Running directly
        # if isinstance(self._Connection_Strategy, MultiConnections):
        #     self._logger.debug("Running all things with Bounded Semaphore.")
        #     # data = await AsyncRunnableOperator.run_with_semaphore(function=self.sql_process_new)
        #     # data = await AsyncRunnableOperator.run_with_bounded_semaphore(function=self.sql_process_new)
        #     data = await self.sql_process_many()
        #     self._logger.debug(f"at fun 'run': {data}")
        #     return data
        # elif isinstance(self._Connection_Strategy, SingleConnection):
        #     self._logger.debug("Running all things with Lock.")
        #     # return AsyncRunnableOperator.run_with_lock(function=self.sql_process_new)
        #     return self.sql_process_one()
        # else:
        #     pass


    @AsyncRunWith.Lock
    async def sql_process_one(self):
        # sql_tasks = self.get_all_sql_tasks()
        sql_tasks = QueueOperator.get_queue_with_name(name="test_sql_task")
        self._logger.debug(f"SQL tasks: {sql_tasks}")
        sql_query = await sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {sql_query}")
        data = self.running_sql_query_process(sql_query=sql_query)
        return data


    @AsyncRunWith.Bounded_Semaphore
    async def sql_process_many(self):
        # sql_tasks = self.get_all_sql_tasks()
        sql_tasks = QueueOperator.get_queue_with_name(name="test_sql_task")
        self._logger.debug(f"SQL tasks: {sql_tasks}")
        sql_query = await sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {sql_query}")
        data = self.running_sql_query_process(sql_query=sql_query)
        return data


    def execute_sql(self, cursor: MySQLCursor, query: str) -> object:
        cursor.execute(query)
        return cursor


    def fetch_all(self, cursor: MySQLCursor) -> Union[object, None]:
        return cursor.fetchall()


    def error_handling(self, error: Error) -> Union[object, None]:
        # Print error message
        self._logger.error(f"Got an error! ")
        self._logger.error(f"error: {error}")
        self._logger.error(f"e.sqlstate: {error.sqlstate}")
        self._logger.error(f"e.errno: {error.errno}")
        self._logger.error(f"e.msg: {error.msg}")
        return None


    def executing_result(self, running_state, data, exception_info) -> Dict[str, object]:
        self._logger.debug(f"SQL result data: {data}")
        __handled_data = data
        if __handled_data is not None:
            __handled_data = self.iterate_data_rows(data=data)
        self._logger.debug(f"Handling finish and final data is: {__handled_data}")
        return {
            "pid": os.getpid(),
            "state": running_state,
            "data": __handled_data,
            "exception_info": exception_info
        }
        # return {"pid": os.getpid(), "state": running_state, "data": data, "exception_info": exception_info}


    def iterate_data_rows(self, data: Tuple[Tuple]):
        new_data = map(self.__data_type_handling, data)
        return list(new_data)


    def __data_type_handling(self, data: Iterable):
        new_data = []
        for d in data:
            if isinstance(d, datetime.datetime):
                f = '%Y-%m-%d %H:%M:%S'
                new_d = datetime.datetime.strftime(d, f)
                new_data.append(new_d)
            if isinstance(d, decimal.Decimal):
                new_d = float(d)
                new_data.append(new_d)
        return new_data


    def close_pool(self):
        self._Connection_Strategy.close_pool()
        self._logger.debug("Close the MySQL connection Pool.")

