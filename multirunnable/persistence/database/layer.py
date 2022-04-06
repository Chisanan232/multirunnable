from typing import Tuple, TypeVar, Generic, Any
from abc import ABC, abstractmethod

from .strategy import BaseDatabaseConnection, BaseConnectionPool
from .operator import DatabaseOperator
from ..interface import DataPersistenceLayer
from ... import get_current_mode


T = TypeVar("T")


class DatabaseAccessObject(DataPersistenceLayer, ABC):
    pass



class BaseDao(DatabaseAccessObject):

    _Database_Connection_Strategy: BaseDatabaseConnection = None
    _Database_Opts_Instance: DatabaseOperator = None

    def __init__(self):
        self._Database_Connection_Strategy = self._instantiate_strategy()
        if isinstance(self._Database_Connection_Strategy, BaseConnectionPool):
            _current_running_mode = get_current_mode()
            if _current_running_mode is None:
                raise ValueError("The RunningMode cannot be None object if it works persistence process as 'BaseConnectionPool'.")
        self._Database_Opts_Instance = self._instantiate_database_opts(strategy=self._Database_Connection_Strategy)


    @property
    def database_opts(self) -> DatabaseOperator:
        if self._Database_Opts_Instance is None:
            self._Database_Connection_Strategy = self._instantiate_strategy()
            self._Database_Opts_Instance = self._instantiate_database_opts(strategy=self._Database_Connection_Strategy)
        return self._Database_Opts_Instance


    @abstractmethod
    def _instantiate_strategy(self) -> BaseDatabaseConnection:
        pass


    @abstractmethod
    def _instantiate_database_opts(self, strategy: BaseDatabaseConnection) -> DatabaseOperator:
        pass


    def reconnect(self, timeout: int = 1, force: bool = False) -> None:
        self.database_opts.reconnect(timeout=timeout, force=force)


    def commit(self) -> None:
        self.database_opts.commit()


    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> Generic[T]:
        return self.database_opts.execute(operator=operator, params=params, multi=multi)


    def execute_many(self, operator: Any, seq_params: Tuple = None) -> Generic[T]:
        return self.database_opts.execute_many(operator=operator, seq_params=seq_params)


    def fetch_one(self) -> list:
        return self.database_opts.fetch_one()


    def fetch_many(self, size: int = None) -> list:
        return self.database_opts.fetch_many(size=size)


    def fetch_all(self) -> list:
        return self.database_opts.fetch_all()


    def close_cursor(self) -> Generic[T]:
        return self.database_opts.close_cursor()


    def close_connection(self) -> Generic[T]:
        self.database_opts.close_connection()

