from multirunnable.persistence.database.strategy import get_connection_pool, database_connection_pools, BaseDatabaseConnection, BaseSingleConnection, BaseConnectionPool
from multirunnable.persistence.database.operator import DatabaseOperator
from multirunnable.parallel.share import sharing_in_processes

from multiprocessing.managers import NamespaceProxy
from typing import Any, Tuple, Dict, Union
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from mysql.connector.errors import PoolError
from mysql.connector.cursor import MySQLCursor
import mysql.connector
import time
import os



class MySQLSingleConnectionProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'connection', 'cursor')



class MySQLDriverConnectionPoolProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'connection', 'cursor')


# @sharing_in_processes(proxytype=MySQLSingleConnectionProxy)
# @sharing_in_processes()
class MySQLSingleConnection(BaseSingleConnection):

    @property
    def connection(self) -> MySQLConnection:
        """
        Note:
            For resolving this issue, we should do something to avoid this issue.
            However, it has exception about "TypeError: can't pickle _mysql_connector.MySQL objects" for database package.
        :return:
        """
        return self._database_connection


    def connect_database(self, **kwargs) -> MySQLConnection:
        # return mysql.connector.connect(**self._Database_Config)
        _connection = mysql.connector.connect(**kwargs)
        print(f'[DEBUG] init MySQLSingleConnection.connection ping: {_connection}')
        return _connection


    def commit(self) -> None:
        self.connection.commit()


    def close(self) -> None:
        if self.connection is not None and self.connection.is_connected():
            # if self.cursor is not None:
            #     self.cursor.close()
            self.connection.close()
            print(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            print("Connection has been disconnect or be killed before.")


# @sharing_in_processes
class MySQLDriverConnectionPool(BaseConnectionPool):

    def connect_database(self, **kwargs) -> MySQLConnectionPool:
        # connection_pool = MySQLConnectionPool(**self._Database_Config)
        connection_pool = MySQLConnectionPool(**kwargs)
        return connection_pool


    def get_one_connection(self, pool_name: str = "", **kwargs) -> PooledMySQLConnection:
        while True:
            try:
                # return self.database_connection_pool.get_connection()
                __connection = get_connection_pool(pool_name=pool_name).get_connection()
                print(f"Get a valid connection: {__connection}")
                return __connection
            except PoolError as e:
                print(f"Connection Pool: {get_connection_pool(pool_name=pool_name).pool_size} ")
                print(f"Will sleep for 5 seconds to wait for connection is available.")
                time.sleep(5)
            except AttributeError as ae:
                raise ConnectionError(f"Cannot get the one connection instance from connection pool because it doesn't exist the connection pool with the name '{pool_name}'.")


    def commit(self) -> None:
        self.connection.commit()


    def close_pool(self) -> None:
        # self.get_connection_pool(pool_name=pool_name).close()
        pass


    def close(self) -> None:
        pass
        # if conn.is_connected():
        #     cursor.close()
        #     conn.close()
        #     print(f"MySQL connection is closed. - PID: {os.getpid()}")
        # else:
        #     print("Connection has been disconnect or be killed before.")


# @sharing_in_processes()
class MySQLOperator(DatabaseOperator):

    def __init__(self, conn_strategy: BaseDatabaseConnection, db_config: Dict = {}):
        super().__init__(conn_strategy=conn_strategy, db_config=db_config)


    def initial_cursor(self, connection: Union[MySQLConnection, PooledMySQLConnection]) -> MySQLCursor:
        return self._db_connection.cursor(buffered=True)


    @property
    def _connection(self) -> MySQLConnection:
        if self._db_connection is None:
            print(f"[DEBUG] MySQLOperator._connection:: it lost instance...")
            self._db_connection = self._conn_strategy.connection
            if self._db_connection is None:
                print(f"[DEBUG] the connection instance still be None so it will require to reconnect to database.")
                self._db_connection = self._conn_strategy.reconnect(timeout=3)
        print(f"[DEBUG] MySQLOperator._connection: {self._db_connection}")
        print(f"[DEBUG] ID of MySQLOperator._connection: {id(self._db_connection)}")
        return self._db_connection


    @property
    def _cursor(self) -> MySQLCursor:
        if self._db_cursor is None:
            print(f"[DEBUG] MySQLOperator._cursor:: it lost instance...")
            # self._db_cursor = self._db_connection.cursor(buffered=True)
            self._db_cursor = self._connection.cursor(buffered=True)
            if self._db_cursor is None:
                raise ConnectionError("Cannot instantiate database cursor object.")
        print(f"[DEBUG] MySQLOperator._cursor: {self._db_cursor}")
        print(f"[DEBUG] ID of MySQLOperator._cursor: {id(self._db_cursor)}")
        return self._db_cursor


    @property
    def column_names(self) -> MySQLCursor:
        return self._cursor.column_names


    @property
    def row_count(self) -> MySQLCursor:
        return self._cursor.rowcount


    def next(self) -> MySQLCursor:
        return self._cursor.next()


    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> MySQLCursor:
        return self._cursor.execute(operation=operator, params=params, multi=multi)


    def execute_many(self, operator: Any, seq_params=None) -> MySQLCursor:
        return self._cursor.executemany(operation=operator, seq_params=seq_params)


    def fetch(self) -> MySQLCursor:
        return self._cursor.fetch()


    def fetch_one(self) -> MySQLCursor:
        return self._cursor.fetchone()


    def fetch_many(self, size: int = None) -> MySQLCursor:
        return self._cursor.fetchmany(size=size)


    def fetch_all(self) -> MySQLCursor:
        return self._cursor.fetchall()


    def reset(self) -> None:
        self._cursor.reset()

