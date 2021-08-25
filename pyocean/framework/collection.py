# from pyocean.framework.features import BaseFeatureAdapterFactory

from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Generic


T = TypeVar("T")


class BaseIterator(metaclass=ABCMeta):

    def __init__(self, factory_list: Generic[T]):
        pass


    @abstractmethod
    def has_next(self) -> bool:
        pass


    @abstractmethod
    def next(self) -> T:
        pass



class BaseList(metaclass=ABCMeta):

    _Max: int = -1
    _List: List[T] = []

    def __init__(self, max: int = None):
        if max is not None:
            if max == 0 or max < 0:
                raise ValueError("Max value should be more than 0.")
            if max > 0:
                self._Max = max


    def __len__(self):
        return len(self._List)


    @abstractmethod
    def index(self, index: int) -> T:
        pass


    @abstractmethod
    def append(self, feature: T) -> None:
        pass


    @abstractmethod
    def insert(self, index: int, value: T) -> None:
        pass


    @abstractmethod
    def extend(self, __iterator) -> None:
        pass


    @abstractmethod
    def pop(self, index: int) -> None:
        pass


    @abstractmethod
    def remove(self, value: T) -> None:
        pass


    @abstractmethod
    def clear(self) -> None:
        pass


    @abstractmethod
    def iterator(self) -> BaseIterator:
        pass

