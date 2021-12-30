from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List, Any



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
    def worker_name(self) -> str:
        pass


    @property
    @abstractmethod
    def worker_ident(self) -> str:
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



class MRResult(BaseResult):

    _PID: str = ""
    _Worker_Name: str = ""
    _Worker_Ident: str = ""
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
    def worker_name(self) -> str:
        return self._Worker_Name


    @worker_name.setter
    def worker_name(self, worker_name) -> None:
        self._Worker_Name = worker_name


    @property
    def worker_ident(self) -> str:
        return self._Worker_Ident


    @worker_ident.setter
    def worker_ident(self, worker_id) -> None:
        self._Worker_Ident = worker_id


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



class PoolResult:

    _Data: List[Any] = None
    _Is_Successful: bool = None

    @property
    def data(self) -> List[Any]:
        return self._Data


    @data.setter
    def data(self, d) -> None:
        self._Data = d


    @property
    def is_successful(self) -> bool:
        return self._Is_Successful


    @is_successful.setter
    def is_successful(self, successful) -> None:
        self._Is_Successful = successful

