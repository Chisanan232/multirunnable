from enum import Enum
from typing import Dict


_Package: str = "pyocean"
_Parallel_Module: str = ".parallel.features"
_Concurrent_Module: str = ".concurrent.features"
_Coroutine_Module: str = ".coroutine.features"

_Parallel_Class: str = "Process"
_Concurrent_Class: str = "Thread"
_Greenlet_Class: str = "Greenlet"
_Async_Class: str = "Async"

_Queue: str = "Queue"
_Lock: str = "Lock"
_Communication: str = "Communication"



class RunningMode(Enum):

    MultiProcessing: Dict[str, str] = {"module": _Parallel_Module, "class": "MultiProcessing"}
    MultiThreading: Dict[str, str] = {"module": _Concurrent_Module, "class": "MultiThreading"}
    MultiGreenlet: Dict[str, str] = {"module": _Coroutine_Module, "class": "GeventAPI"}
    Asynchronous: Dict[str, str] = {"module": _Coroutine_Module, "class": "AsynchronousAPI"}



class NewRunningMode(Enum):

    MultiProcessing: Dict[str, str] = {
        "module": _Parallel_Module,
        "queue": _Parallel_Class + _Queue,
        "lock": _Parallel_Class + _Lock,
        "communication": _Parallel_Class + _Communication
    }

    MultiThreading: Dict[str, str] = {
        "module": _Concurrent_Module,
        "queue": _Concurrent_Class + _Queue,
        "lock": _Concurrent_Class + _Lock,
        "communication": _Concurrent_Class + _Communication
    }

    MultiGreenlet: Dict[str, str] = {
        "module": _Coroutine_Module,
        "queue": _Greenlet_Class + _Queue,
        "lock": _Greenlet_Class + _Lock,
        "communication": _Greenlet_Class + _Communication
    }

    Asynchronous: Dict[str, str] = {
        "module": _Coroutine_Module,
        "queue": _Async_Class + _Queue,
        "lock": _Async_Class + _Lock,
        "communication": _Async_Class + _Communication
    }

