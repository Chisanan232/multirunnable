from abc import ABCMeta, abstractmethod
from typing import List, Any
from enum import Enum



class ResultState(Enum):

    SUCCESS = "successful"
    FAIL = "fail"
    INTERRUPT = "interrupt"
    CRASH = "crash"



class BaseResult(metaclass=ABCMeta):

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



class OceanResult(BaseResult):

    _PID: str = ""
    _Worker_ID: str = ""
    _Data: List[Any] = []
    _State: ResultState = None
    _Exception: Exception = None

    @property
    def pid(self) -> str:
        return self._PID


    @pid.setter
    def pid(self, pid: str) -> None:
        self._PID = pid


    @property
    def worker_id(self) -> str:
        return self._Worker_ID


    @worker_id.setter
    def worker_id(self, worker_id) -> None:
        self._Worker_ID = worker_id


    @property
    def data(self) -> List[Any]:
        return self._Data


    @data.setter
    def data(self, data: List[Any]) -> None:
        self._Data = data


    @property
    def state(self) -> ResultState:
        return self._State


    @state.setter
    def state(self, state: ResultState) -> None:
        self._State = state


    @property
    def exception(self) -> Exception:
        return self._Exception


    @exception.setter
    def exception(self, exception: Exception) -> None:
        self._Exception = exception
