from pyocean.framework.builder import RunnableBuilder
from pyocean.persistence.database.connection import BaseConnection
from pyocean.persistence.database.single_connection import SingleConnection
from pyocean.persistence.database.multi_connections import MultiConnections
from pyocean.persistence.database.access_object import BaseDao
from pyocean.logging.level import Logger

from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection, MySQLConnection
from mysql.connector import Error
from mysql.connector.cursor import MySQLCursor
from typing import Dict, Callable, Union
import os

from deprecated.sphinx import deprecated



class TestDao(BaseDao):

    def __init__(self, connection_strategy: BaseConnection, logger: Logger):
        super().__init__(connection_strategy=connection_strategy)


    def run(self) -> object:
        """
        Note (?) need to consider:
            How to abstractilize the logic or how to be more clear ?
        :return:
        """
        # Running directly
        if isinstance(self._Connection_Strategy, MultiConnections):
            self._logger.debug("Running all things with Bounded Semaphore.")
            # data = RunnableBuilder.run_with_semaphore(function=self.sql_process_new)
            data = RunnableBuilder.run_with_bounded_semaphore(function=self.sql_process_new)
            print("[DEBUG] at fun 'run': ", data)
            return data
        else:
            self._logger.debug("Running all things with Lock.")
            return RunnableBuilder.run_with_lock(function=self.sql_process_new)


    def sql_process_new(self):
        sql_tasks = self.get_all_sql_tasks()
        self._logger.debug(f"SQL tasks: {sql_tasks}")
        sql_query = sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {sql_query}")
        data = self.running_sql_query_process(sql_query=sql_query)
        self._logger.debug(f"at fun 'sql_process_new': {data}")
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
        return {"pid": os.getpid(), "state": running_state, "data": data, "exception_info": exception_info}



@deprecated(version="0.4", reason="Adjust the software architecture")
class DatabaseSqlQuery:

    def __init__(self, strategy: MultiConnections, logger: Logger):
        self.__Strategy: Union[SingleConnection, MultiConnections] = strategy
        self.__logger = logger


    def run(self) -> object:
        """
        Note (?) need to consider:
            How to abstractilize the logic or how to be more clear ?
        :return:
        """
        # Running directly
        if isinstance(self.__Strategy, MultiConnections):
            self.__logger.debug("Running all things with Semaphore.")
            return RunnableBuilder.run_with_semaphore(function=self.sql_process_new)
        else:
            self.__logger.debug("Running all things with Lock.")
            return RunnableBuilder.run_with_lock(function=self.sql_process_new)
        # return self.sql_process()

        # # Running with try-except catch
        # self.try_body(function=self.sql_process, index=index)


    @deprecated(version="0.1", reason="Remove useless code.")
    def sql_process(self) -> object:
        # from connection_strategy import Process_Semaphore
        from pyocean.framework.strategy import Running_Semaphore

        self.__logger.debug(f"Thread start - PID: {os.getpid()}")
        # with Process_Semaphore:
        with Running_Semaphore:
            connection = None
            cursor = None
            try:
                connection = self.__Strategy.get_one_connection()
            except Error as e:
                self.__error_process(e=e)
            else:
                self.__running_query_process(connection=connection)
            finally:
                self.__Strategy.close_instance(connection, cursor)
        return {"pid": os.getpid(), "state": True}


    def sql_process_new(self):
        self.__logger.debug(f"Thread start - PID: {os.getpid()}")
        connection = None
        cursor = None
        try:
            connection: Union[MySQLConnection, PooledMySQLConnection] = self.__Strategy.get_one_connection()
        except Error as e:
            self.__error_process(e=e)
            running_state = False
        else:
            self.__running_query_process(connection=connection)
            running_state = True
        finally:
            self.__Strategy.close_instance(connection, cursor)
        return {"pid": os.getpid(), "state": running_state}


    def try_body(self, function: Callable, **kwargs) -> object:
        try:
            return function(**kwargs)
        except Exception as e:
            self.__logger.warning("Occur something error!")
            return e


    def __error_process(self, e: Error) -> None:
        # Print error message
        self.__logger.error(f"Got an error! ")
        self.__logger.error("error: ", e)
        self.__logger.error("e.sqlstate: ", e.sqlstate)
        self.__logger.error("e.errno: ", e.errno)
        self.__logger.error("e.msg: ", e.msg)


    def __running_query_process(self, connection: PooledMySQLConnection) -> None:
        if connection.is_connected():
            self.__logger.info(f"Get a valid connection! PID: {os.getpid()}")
            self.__logger.info(f"Connection object: {connection}")
            cursor: MySQLCursor = self.__Strategy.build_cursor(connection)
            self.__execute_sql_query_new(cursor)
        else:
            self.__logger.warning(f"Doesn't get a connection ... - PID: {os.getpid()}")


    @deprecated(version="0.1", reason="Remove useless code.")
    def __execute_sql_query(self, cursor: MySQLCursor) -> None:
        # from connection_strategy import Process_Queue
        # from running_strategy.strategy_framework import Running_Queue
        from pyocean.framework.strategy import Running_Queue

        __sql = Running_Queue.get()
        self.__logger.debug(f"Get task from Queue: {__sql} - PID: {os.getpid()}")
        cursor.execute(__sql)
        # cursor.execute("select * from stock_data_2330 limit 1;")

        # # Print result method 1
        self.__logger.info(f"The SQL running result: {list(cursor.fetchall())} - PID: {os.getpid()}")

        # # Print result method 2
        # for c in cursor.fetchall():
        #     print("data: ", c)

        # record = cursor.fetchone()
        # print(f"Your connected to - ", record)


    def __execute_sql_query_new(self, cursor: MySQLCursor) -> None:
        Running_Queue = RunnableBuilder.get_queue()
        __sql = Running_Queue.get()
        self.__logger.debug(f"Get task from Queue: {__sql} - PID: {os.getpid()}")
        cursor.execute(__sql)
        # cursor.execute("select * from stock_data_2330 limit 1;")

        # # Print result method 1
        self.__logger.info(f"The SQL running result: {list(cursor.fetchall())} - PID: {os.getpid()}")

        # # Print result method 2
        # for c in cursor.fetchall():
        #     print("data: ", c)

        # record = cursor.fetchone()
        # print(f"Your connected to - ", record)
