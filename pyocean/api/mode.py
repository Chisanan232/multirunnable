from enum import Enum
from typing import Dict


_Package: str = "pyocean"
# _Parallel_Module: str = "..parallel.features"
# _Concurrent_Module: str = "..concurrent.features"
_Parallel_Module: str = ".parallel.features"
_Concurrent_Module: str = ".concurrent.features"
_Coroutine_Module: str = ".coroutine.features"



class RunningMode(Enum):

    MultiProcessing: Dict[str, str] = {"module": _Parallel_Module, "class": "MultiProcessing"}
    MultiThreading: Dict[str, str] = {"module": _Concurrent_Module, "class": "MultiThreading"}
    MultiGreenlet: Dict[str, str] = {"module": _Coroutine_Module, "class": "GeventAPI"}
    Asynchronous: Dict[str, str] = {"module": _Coroutine_Module, "class": "AsynchronousAPI"}

