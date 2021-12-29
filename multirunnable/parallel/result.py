from multirunnable.framework.result import MRResult as _MRResult

from typing import List, Any



class ParallelResult(_MRResult):

    _PPID: str = ""
    _Exit_Code: str = ""

    @property
    def ppid(self) -> str:
        return self._PPID


    @ppid.setter
    def ppid(self, ppid: str) -> None:
        self._PPID = ppid


    @property
    def exit_code(self) -> str:
        return self._Exit_Code


    @exit_code.setter
    def exit_code(self, exit_code: str) -> None:
        self._Exit_Code = exit_code



class ProcessPoolResult:

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

