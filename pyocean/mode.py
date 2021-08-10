from enum import Enum


_Package: str = "pyocean"
_Parallel_Module: str = ".parallel."
_Concurrent_Module: str = ".concurrent."
_Coroutine_Module: str = ".coroutine."
_Feature_Module: str = "features"
_Strategy_Module: str = "strategy"


# # Feature class
_Parallel_Feature_Class: str = "Process"
_Concurrent_Feature_Class: str = "Thread"
_Greenlet_Feature_Class: str = "Greenlet"
_Async_Feature_Class: str = "Async"

_Queue_Class: str = "Queue"
_Lock_Class: str = "Lock"
_Communication_Class: str = "Communication"


# # Strategy class
_Parallel_Common_Class: str = "MultiProcessing"
_Concurrent_Common_Class: str = "MultiThreading"
_Greenlet_Common_Class: str = "MultiGreenlet"
_Async_Common_Class: str = "Asynchronous"

_Strategy_Class: str = "Strategy"



class FeatureMode(Enum):

    MultiProcessing = {
        "module": _Parallel_Module + _Feature_Module,
        "queue": _Parallel_Feature_Class + _Queue_Class,
        "lock": _Parallel_Feature_Class + _Lock_Class,
        "communication": _Parallel_Feature_Class + _Communication_Class
    }

    MultiThreading = {
        "module": _Concurrent_Module + _Feature_Module,
        "queue": _Concurrent_Feature_Class + _Queue_Class,
        "lock": _Concurrent_Feature_Class + _Lock_Class,
        "communication": _Concurrent_Feature_Class + _Communication_Class
    }

    MultiGreenlet = {
        "module": _Coroutine_Module + _Feature_Module,
        "queue": _Greenlet_Feature_Class + _Queue_Class,
        "lock": _Greenlet_Feature_Class + _Lock_Class,
        "communication": _Greenlet_Feature_Class + _Communication_Class
    }

    Asynchronous = {
        "module": _Coroutine_Module + _Feature_Module,
        "queue": _Async_Feature_Class + _Queue_Class,
        "lock": _Async_Feature_Class + _Lock_Class,
        "communication": _Async_Feature_Class + _Communication_Class
    }



class RunningMode(Enum):

    Parallel = {
        "strategy_module": _Parallel_Module + _Strategy_Module,
        "strategy": _Parallel_Common_Class + _Strategy_Class
    }

    Concurrent = {
        "strategy_module": _Concurrent_Module + _Strategy_Module,
        "strategy": _Concurrent_Common_Class + _Strategy_Class
    }

    Greenlet = {
        "strategy_module": _Coroutine_Module + _Strategy_Module,
        "strategy": _Greenlet_Common_Class + _Strategy_Class
    }

    Asynchronous = {
        "strategy_module": _Coroutine_Module + _Strategy_Module,
        "strategy": _Async_Common_Class + _Strategy_Class
    }

