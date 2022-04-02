from typing import Tuple, Dict, TypeVar, Generic, Any
from abc import ABC, abstractmethod

from .strategy import BaseDatabaseConnection as _BaseDataBaseConnection, BaseConnectionPool


T = TypeVar("T")


class BaseDatabaseOperator:

    def __init__(self, conn_strategy: _BaseDataBaseConnection, db_config: Dict = {}, timeout: int = 1):
        self._conn_strategy = conn_strategy
        self._db_conn_config = db_config

        self._db_connection: Generic[T] = self._conn_strategy.current_connection

        if self._db_connection is None:
            self._conn_strategy.initial(**self._db_conn_config)
            if isinstance(self._conn_strategy, BaseConnectionPool) is True:
                self._pool_name = self._db_conn_config.get("pool_name", None)
                if self._pool_name is None:
                    raise ValueError("Pool name could not be empty value.")
                self._db_connection = self._conn_strategy.get_one_connection(pool_name=self._pool_name)
            else:
                self._db_connection = self._conn_strategy.get_one_connection()
        else:
            if self._conn_strategy.is_connected() is False:
                self.reconnect(timeout=timeout, force=True)

        self._db_cursor: Generic[T] = self.initial_cursor(connection=self._db_connection)


    @property
    def _connection(self) -> Generic[T]:
        if self._db_connection is None:
            if isinstance(self._conn_strategy, BaseConnectionPool):
                self._db_connection = self._conn_strategy.get_one_connection(pool_name=self._db_conn_config.get("pool_name", None))
            else:
                self._db_connection = self._conn_strategy.get_one_connection()
            assert self._db_connection is not None, "The database connection should not be None object."
        return self._db_connection


    @property
    def _cursor(self) -> Generic[T]:
        if self._db_cursor is None:
            self._db_cursor = self.initial_cursor(connection=self._connection)
            assert self._db_cursor is not None, "The cursor instance of database connection should not be None object."
        return self._db_cursor


    @abstractmethod
    def reconnect(self, timeout: int = 1, force: bool = False) -> None:
        pass


    @abstractmethod
    def commit(self, **kwargs) -> None:
        pass


    @abstractmethod
    def close_connection(self, **kwargs) -> None:
        pass


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

    def reconnect(self, timeout: int = 1, force: bool = False) -> None:
        self._db_connection = self._conn_strategy.reconnect(timeout=timeout, force=force)
        self._db_cursor = self.initial_cursor(connection=self._db_connection)


    def commit(self, **kwargs) -> None:
        self._conn_strategy.commit(**kwargs)


    def close_connection(self, **kwargs) -> None:
        self._conn_strategy.close_connection(**kwargs)

