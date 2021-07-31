from abc import ABCMeta, abstractmethod
from typing import List, Any
from enum import Enum



class ResultState(Enum):

    SUCCESS = "successful"
    FAIL = "fail"
    INTERRUPT = "interrupt"
    CRASH = "crash"



class OceanResult(metaclass=ABCMeta):

    @property
    @abstractmethod
    def pid(self) -> str:
        pass


    @property
    @abstractmethod
    def worker_id(self) -> str:
        pass


    @property
    @abstractmethod
    def data(self) -> List[Any]:
        pass


    @property
    @abstractmethod
    def state(self) -> ResultState:
        pass


    @property
    @abstractmethod
    def exception(self) -> Exception:
        pass

