from multirunnable.persistence.interface import BasePersistence
from multirunnable.persistence.database.strategy import BaseDatabaseConnection as _BaseDataBaseConnection

from abc import ABCMeta, ABC, abstractmethod
from typing import Tuple, Dict, Type, TypeVar, Generic, Any, Union, Optional


T = TypeVar("T")


class BaseDatabaseOperator(BasePersistence):

    def __init__(self, conn_strategy: _BaseDataBaseConnection, db_config: Dict = {}):
        self._conn_strategy = conn_strategy
        if self._conn_strategy.connection is None:
            self._conn_strategy.initial(**db_config)
        self._db_connection: Generic[T] = self._conn_strategy.connection
        self._db_cursor: Generic[T] = self.initial_cursor(connection=self._db_connection)


    @property
    def _connection(self) -> Generic[T]:
        if self._db_connection is None:
            self._db_connection = self._conn_strategy.connection
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


    # @property
    # def column_names(self) -> Generic[T]:
    #     raise NotImplementedError


    # @property
    # def row_count(self) -> Generic[T]:
    #     raise NotImplementedError


    # def next(self) -> Generic[T]:
    #     raise NotImplementedError


    @abstractmethod
    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> Generic[T]:
        pass


    def execute_many(self, operator: Any, seq_params=None) -> Generic[T]:
        raise NotImplementedError


    def fetch(self) -> Generic[T]:
        raise NotImplementedError


    def fetch_one(self) -> Generic[T]:
        raise NotImplementedError


    @abstractmethod
    def fetch_many(self, size: int = None) -> Generic[T]:
        pass


    def fetch_all(self) -> Generic[T]:
        raise NotImplementedError


    # def reset(self) -> None:
    #     raise NotImplementedError


    @abstractmethod
    def close(self) -> Generic[T]:
        pass



class DatabaseOperator(BaseDatabaseOperator, ABC):

    def close(self) -> Generic[T]:
        return self._conn_strategy.close()

