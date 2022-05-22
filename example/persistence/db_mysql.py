from multirunnable.persistence.database.strategy import (
    get_connection_pool,
    BaseDatabaseConnection, BaseSingleConnection, BaseConnectionPool)
from multirunnable.persistence.database.operator import DatabaseOperator
from multirunnable.parallel.share import sharing_in_processes

from multiprocessing.managers import NamespaceProxy
from typing import Tuple, Dict, Any, cast, Generic, Union
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from mysql.connector.errors import PoolError
from mysql.connector.cursor import MySQLCursor
import mysql.connector
import logging
import time
import os



class MySQLSingleConnectionProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'connection')



class MySQLDriverConnectionPoolProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'connection')



class MySQLOperatorProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', '_connection', '_cursor')



# @sharing_in_processes(proxytype=MySQLSingleConnectionProxy)
# @sharing_in_processes()
class MySQLSingleConnection(BaseSingleConnection):

    def _connect_database(self, **kwargs) -> MySQLConnection:
        # return mysql.connector.connect(**self._Database_Config)
        _connection = mysql.connector.connect(**kwargs)
        return _connection


    def _is_connected(self) -> bool:
        return self.current_connection.is_connected()


    def commit(self) -> None:
        self.current_connection.commit()


    def _close_connection(self) -> None:
        if self.current_connection is not None and self.current_connection.is_connected():
            self.current_connection.close()
            logging.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            logging.info("Connection has been disconnect or be killed before.")



# @sharing_in_processes(proxytype=MySQLSingleConnectionProxy)
class MySQLDriverConnectionPool(BaseConnectionPool):

    def connect_database(self, **kwargs) -> MySQLConnectionPool:
        connection_pool = MySQLConnectionPool(**kwargs)
        return connection_pool


    def _get_one_connection(self, pool_name: str = "", **kwargs) -> PooledMySQLConnection:
        while True:
            try:
                # return self.database_connection_pool.get_connection()
                __connection = get_connection_pool(pool_name=pool_name).get_connection()
                logging.info(f"Get a valid connection: {__connection}")
                return __connection
            except PoolError as e:
                logging.error(f"Connection Pool: {get_connection_pool(pool_name=pool_name)} ")
                logging.error(f"Will sleep for 5 seconds to wait for connection is available.")
                time.sleep(5)
            except AttributeError as ae:
                raise ConnectionError(f"Cannot get the one connection instance from connection pool because it doesn't exist the connection pool with the name '{pool_name}'.")


    def _is_connected(self, conn: PooledMySQLConnection) -> bool:
        return conn.is_connected()


    def _commit(self, conn: PooledMySQLConnection) -> None:
        conn.commit()


    def _close_connection(self, conn: PooledMySQLConnection) -> None:
        if conn is not None:
            conn.close()
            logging.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            logging.info("Connection has been disconnect or be killed before.")


    def close_pool(self, pool_name: str) -> None:
        pass



# @sharing_in_processes(proxytype=MySQLOperatorProxy)
class MySQLOperator(DatabaseOperator):

    def __init__(self, conn_strategy: BaseDatabaseConnection, db_config: Dict = {}):
        super().__init__(conn_strategy=conn_strategy, db_config=db_config)


    def initial_cursor(self, connection: Union[MySQLConnection, PooledMySQLConnection]) -> MySQLCursor:
        return connection.cursor(buffered=True)


    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> MySQLCursor:
        return self._cursor.execute(operation=operator, params=params, multi=multi)


    def execute_many(self, operator: Any, seq_params=None) -> MySQLCursor:
        return self._cursor.executemany(operation=operator, seq_params=seq_params)


    def fetch_one(self) -> list:
        return self._cursor.fetchone()


    def fetch_many(self, size: int = None) -> list:
        return self._cursor.fetchmany(size=size)


    def fetch_all(self) -> list:
        return self._cursor.fetchall()

