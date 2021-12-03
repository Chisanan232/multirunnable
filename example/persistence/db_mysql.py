from multirunnable.persistence.database.strategy import BaseDatabaseConnection,BaseSingleConnection, BaseConnectionPool
from multirunnable.persistence.database.operator import DatabaseOperator

from typing import Any, Tuple, cast
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from mysql.connector.errors import PoolError
from mysql.connector.cursor import MySQLCursor
import mysql.connector
import logging
import time
import os



class MySQLSingleConnection(BaseSingleConnection):

    @property
    def connection(self) -> MySQLConnection:
        return self._database_connection


    @connection.setter
    def connection(self, conn: MySQLConnection) -> None:
        self._database_connection = conn


    @property
    def cursor(self) -> MySQLCursor:
        # if self.connection.ping(reconnect=True) is False:
        #     print("[WARN] Ping to MySQL database fail, it will re-connect to database again.")
        #     self.close()
        #     self.initial(**self.database_config)
        #     if self.connection is None or self.cursor is None:
        #         raise ConnectionError
        return self._database_cursor


    @cursor.setter
    def cursor(self, cur: MySQLCursor) -> None:
        self._database_cursor = cur


    def connect_database(self, **kwargs) -> MySQLConnection:
        # return mysql.connector.connect(**self._Database_Config)
        _connection = mysql.connector.connect(**kwargs)
        print(f'[DEBUG] init MySQLSingleConnection.connection: {_connection}')
        return _connection


    def build_cursor(self) -> MySQLCursor:
        _cursor = self.connection.cursor(buffered=True)
        print(f'[DEBUG] init MySQLSingleConnection.cursor: {_cursor}')
        return _cursor


    def commit(self) -> None:
        self.connection.commit()


    def close(self) -> None:
        if self.connection is not None and self.connection.is_connected():
            if self.cursor is not None:
                self.cursor.close()
            self.connection.close()
            logging.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            logging.info("Connection has been disconnect or be killed before.")



class MySQLDriverConnectionPool(BaseConnectionPool):

    def get_database_conn_pool(self, name: str = "") -> MySQLConnectionPool:
        return super(MySQLDriverConnectionPool, self).get_database_conn_pool()


    @property
    def connection(self) -> PooledMySQLConnection:
        return super(MySQLDriverConnectionPool, self).connection


    @connection.setter
    def connection(self, conn: PooledMySQLConnection) -> None:
        super(MySQLDriverConnectionPool, self).connection = conn


    @property
    def cursor(self) -> MySQLCursor:
        return super(MySQLDriverConnectionPool, self).cursor


    @cursor.setter
    def cursor(self, cur: MySQLCursor) -> None:
        super(MySQLDriverConnectionPool, self).cursor = cur


    def connect_database(self, **kwargs) -> MySQLConnectionPool:
        # connection_pool = MySQLConnectionPool(**self._Database_Config)
        connection_pool = MySQLConnectionPool(**kwargs)
        return connection_pool


    def get_one_connection(self) -> PooledMySQLConnection:
        while True:
            try:
                # return self.database_connection_pool.get_connection()
                __connection = self.get_database_conn_pool.get_connection()
                logging.info(f"Get a valid connection: {__connection}")
                return __connection
            except PoolError as e:
                logging.error(f"Connection Pool: {self.get_database_conn_pool.pool_size} ")
                logging.error(f"Will sleep for 5 seconds to wait for connection is available. - {self.getName()}")
                time.sleep(5)


    def build_cursor(self) -> MySQLCursor:
        self.cursor = self.connection.cursor()
        return self.cursor


    def commit(self) -> None:
        self.connection.commit()


    def close_pool(self) -> None:
        self.get_database_conn_pool.close()


    def close(self) -> None:
        if self.connection is not None and self.connection.is_connected():
            if self.cursor is not None:
                self.cursor.close()
            self.connection.close()
            logging.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            logging.info("Connection has been disconnect or be killed before.")



class MySQLOperator(DatabaseOperator):
    
    def __init__(self, conn_strategy: BaseDatabaseConnection):
        super(MySQLOperator, self).__init__(conn_strategy=conn_strategy)
        self.conn_strategy = conn_strategy
        self._db_connection = self.conn_strategy.connection
        self._db_cursor = self.conn_strategy.cursor


    @property
    def _connection(self) -> MySQLConnection:
        if self._db_connection is None:
            print(f"[DEBUG] MySQLOperator._connection:: it lost instance...")
            self._db_connection = self.conn_strategy.connection
        print(f"[DEBUG] MySQLOperator._connection: {self._db_connection}")
        print(f"[DEBUG] ID of MySQLOperator._connection: {id(self._db_connection)}")
        return self._db_connection


    @property
    def _cursor(self) -> MySQLCursor:
        if self._db_cursor is None:
            print(f"[DEBUG] MySQLOperator._cursor:: it lost instance...")
            self._db_cursor = self.conn_strategy.cursor
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
        import multiprocessing as mp
        print(f"[DEBUG] Before execute the SQL query. - {mp.current_process}")
        print(f"[DEBUG] MySQLOperator._cursor: {self._cursor}")
        self.conn_strategy.cursor = self._cursor.execute(operation=operator, params=params, multi=multi)
        print(f"[DEBUG] After execute the SQL query. - {mp.current_process}")
        print(f"[DEBUG] MySQLOperator._cursor: {self._cursor}")
        return self.conn_strategy.cursor


    def execute_many(self, operator: Any, seq_params=None) -> MySQLCursor:
        return self._cursor.executemany(operation=operator, seq_params=seq_params)


    def fetch(self) -> MySQLCursor:
        return self._cursor.fetch()


    def fetch_one(self) -> MySQLCursor:
        return self._cursor.fetchone()


    def fetch_many(self, size: int = None) -> MySQLCursor:
        return self._cursor.fetchmany(size=size)


    def fetch_all(self) -> MySQLCursor:
        print(f"[YEE] MySQLOperator._cursor in MySQLOperator.fetch_all: {self._cursor}")
        return self._cursor.fetchall()


    def reset(self) -> None:
        self._cursor.reset()

