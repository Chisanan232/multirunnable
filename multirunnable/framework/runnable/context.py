from typing import List, Any
from abc import ABCMeta, abstractmethod



class BaseContext(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def get_current_worker() -> Any:
        pass


    @staticmethod
    @abstractmethod
    def get_parent_worker() -> Any:
        pass


    @staticmethod
    @abstractmethod
    def current_worker_is_parent() -> bool:
        pass


    @staticmethod
    @abstractmethod
    def get_current_worker_ident() -> str:
        pass


    @staticmethod
    @abstractmethod
    def get_current_worker_name() -> str:
        pass


    @staticmethod
    @abstractmethod
    def current_worker_is_alive() -> bool:
        pass


    @staticmethod
    @abstractmethod
    def active_workers_count() -> int:
        pass


    @staticmethod
    @abstractmethod
    def children_workers() -> List[Any]:
        pass


