from typing import List, Any

from pyocean.framework.result import ResultState, OceanResult



class ParallelResult(OceanResult):

    __PID: str = ""
    __Worker_ID: str = ""
    __Data: List[Any] = []
    __State: ResultState = None
    __Exception: Exception = None

    @property
    def pid(self) -> str:
        return self.__PID


    @pid.setter
    def pid(self, pid: str) -> None:
        self.__PID = pid


    @property
    def worker_id(self) -> str:
        return self.__Worker_ID


    @worker_id.setter
    def worker_id(self, worker_id) -> None:
        self.__Worker_ID = worker_id


    @property
    def data(self) -> List[Any]:
        return self.__Data


    @data.setter
    def data(self, data: List[Any]) -> None:
        self.__Data = data


    @property
    def state(self) -> ResultState:
        return self.__State


    @state.setter
    def state(self, state: ResultState) -> None:
        self.__State = state


    @property
    def exception(self) -> Exception:
        return self.__Exception


    @exception.setter
    def exception(self, exception: Exception) -> None:
        self.__Exception = exception

