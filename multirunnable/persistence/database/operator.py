from .strategy import BaseDatabaseConnection as _BaseDataBaseConnection, BaseSingleConnection, BaseConnectionPool

from abc import ABC, abstractmethod
from typing import Tuple, Dict, TypeVar, Generic, Any


T = TypeVar("T")


class BaseDatabaseOperator:

    def __init__(self, conn_strategy: _BaseDataBaseConnection, db_config: Dict = {}):
        self._conn_strategy = conn_strategy
        self._db_connection: Generic[T] = self._conn_strategy.current_connection

        if self._db_connection is None:
            self._conn_strategy.initial(**db_config)
            if isinstance(self._conn_strategy, BaseConnectionPool) is True:
                self._pool_name = db_config.get("pool_name", "")
                self._db_connection = self._conn_strategy.get_one_connection(pool_name=self._pool_name)
            else:
                self._db_connection = self._conn_strategy.get_one_connection()

        self._db_cursor: Generic[T] = self.initial_cursor(connection=self._db_connection)


    @property
    def _connection(self) -> Generic[T]:
        if self._db_connection is None:
            if isinstance(self._conn_strategy, BaseConnectionPool):
                self._db_connection = self._conn_strategy.get_one_connection(pool_name=self._pool_name)
            else:
                self._db_connection = self._conn_strategy.get_one_connection()
            if self._db_connection is None:
                self._db_connection = self._conn_strategy.reconnect(timeout=3)
        return self._db_connection


    @property
    def _cursor(self) -> Generic[T]:
        if self._db_cursor is None:
            self._db_cursor = self.initial_cursor(connection=self._connection)
            if self._db_cursor is None:
                raise ConnectionError("Cannot instantiate database cursor object.")
        return self._db_cursor


    @abstractmethod
    def initial_cursor(self, connection: Generic[T]) -> Generic[T]:
        pass


    @abstractmethod
    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> Generic[T]:
        pass


    def execute_many(self, operator: Any, seq_params=None) -> Generic[T]:
        raise NotImplementedError


    def fetch_one(self) -> list:
        raise NotImplementedError


    @abstractmethod
    def fetch_many(self, size: int = None) -> list:
        pass


    def fetch_all(self) -> list:
        raise NotImplementedError


    @abstractmethod
    def close_cursor(self) -> Generic[T]:
        pass



class DatabaseOperator(BaseDatabaseOperator, ABC):

    def reconnect(self, timeout: int = 1) -> None:
        self._db_connection = self._conn_strategy.reconnect(timeout=timeout)
        self._db_cursor = self.initial_cursor(connection=self._db_connection)


    def commit(self, **kwargs) -> None:
        if isinstance(self._conn_strategy, BaseConnectionPool):
            _conn = DatabaseOperator._chk_conn(**kwargs)
            self._conn_strategy.commit(conn=_conn)
        else:
            self._conn_strategy.commit()


    def close_connection(self, **kwargs):
        if isinstance(self._conn_strategy, BaseConnectionPool):
            _conn = DatabaseOperator._chk_conn(**kwargs)
            self._conn_strategy.close_connection(conn=_conn)
        else:
            self._conn_strategy.close_connection()


    @staticmethod
    def _chk_conn(**kwargs) -> Any:
        _conn = kwargs.get("conn", None)
        if _conn is None:
            raise ValueError("Option *conn* cannot be None object if connection strategy is BaseConnectionPool type.")
        return _conn

