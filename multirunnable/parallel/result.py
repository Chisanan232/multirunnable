from multirunnable.framework.result import MRResult as _MRResult, PoolResult as _PoolResult

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



class ProcessPoolResult(_PoolResult):
    pass

