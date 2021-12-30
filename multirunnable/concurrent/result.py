from multirunnable.framework.result import MRResult as _MRResult, PoolResult as _PoolResult

from typing import List, Any



class ConcurrentResult(_MRResult):

    _Native_ID: str = ""

    @property
    def native_id(self) -> str:
        return self._Native_ID


    @native_id.setter
    def native_id(self, native_id: str) -> None:
        self._Native_ID = native_id



class ThreadPoolResult(_PoolResult):
    pass
