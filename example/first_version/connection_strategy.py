from multirunnable.persistence.database import SingleConnection, MultiConnections
from multirunnable.persistence.database.configuration import BaseDatabaseConfiguration
from multirunnable.logger import ocean_logger

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from mysql.connector.errors import PoolError
from mysql.connector.cursor import MySQLCursor
import mysql.connector
import time
import os



class SingleTestConnectionStrategy(SingleConnection):

    def __init__(self, configuration: BaseDatabaseConfiguration):
        super().__init__(configuration)
        self._logger = ocean_logger


    def connect_database(self) -> MySQLConnection:
        """
        Note:
            It should have lock object to gaurantee that it always has only one thread run here.
        :return:
        """
        return mysql.connector.connect(**self._Database_Config)


    def build_cursor(self, connection: MySQLConnection) -> MySQLCursor:
        return connection.cursor()


    def close_instance(self, connection: MySQLConnection, cursor: MySQLConnection) -> None:
        if connection is not None and connection.is_connected():
            if cursor is not None:
                cursor.close()
            connection.close()
            self._logger.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            self._logger.info("Connection has been disconnect or be killed before.")



class MultiTestConnectionStrategy(MultiConnections):

    def __init__(self, configuration: BaseDatabaseConfiguration = None):
        super().__init__(configuration=configuration)
        self._logger = ocean_logger
        self._logger.debug("Class MultiTestConnectionStrategy be newed (including logging) ...")


    def set_pool_size(self, pool_size: int) -> None:
        self._Database_Config["pool_reset_session"] = True,
        self._Database_Config["pool_size"] = pool_size
        print("[DEBUG] set connection pool configuration done")


    def connect_database(self, **kwargs) -> MySQLConnectionPool:
        print("[DEBUG] set connection pool configuration configure: ", kwargs)
        for key, value in kwargs.items():
            # self.__MySQL_Stock_Data_Config[key] = value
            self._Database_Config[key] = value
        print("[DEBUG] database config: ", self._Database_Config)
        connection_pool = MySQLConnectionPool(**self._Database_Config)
        self._logger.debug(f"MySQL_Connection_Pool at 'connection_strategy.init_connection_pool': {connection_pool}")
        return connection_pool


    def get_one_connection(self) -> PooledMySQLConnection:
        while True:
            try:
                # return self.database_connection_pool.get_connection()
                __connection = self.database_connection_pool.get_connection()
                self._logger.info(f"Get a valid connection: {__connection}")
                return __connection
            except PoolError as e:
                self._logger.error(f"Connection Pool: {self.database_connection_pool.pool_size} ")
                self._logger.error(f"Will sleep for 5 seconds to wait for connection is available. - {self.getName()}")
                time.sleep(5)


    def build_cursor(self, connection: PooledMySQLConnection) -> MySQLCursor:
        return connection.cursor()


    def close_instance(self, connection: PooledMySQLConnection, cursor: MySQLCursor) -> None:
        if connection is not None and connection.is_connected():
            if cursor is not None:
                cursor.close()
            connection.close()
            self._logger.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            self._logger.info("Connection has been disconnect or be killed before.")


    def close_pool(self) -> None:
        self.database_connection_pool.close()
