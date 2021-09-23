from enum import Enum


_Package: str = "pyocean"
_Parallel_Package: str = ".parallel."
_Concurrent_Package: str = ".concurrent."
_Coroutine_Package: str = ".coroutine."
_Feature_Package: str = "features"
_Strategy_Package: str = "strategy"


# # Feature class
_Parallel_Class: str = "Process"
_Concurrent_Class: str = "Thread"
_GreenThread_Class: str = "GreenThread"
_Asynchronous_Class: str = "Asynchronous"

_Queue_Class: str = "Queue"
_Lock_Class: str = "Lock"
_Communication_Class: str = "Communication"


# # Strategy class
_Strategy_Class: str = "Strategy"
_General_Strategy_Class: str = "GeneralStrategy"
_Pool_Strategy_Class: str = "PoolStrategy"



class FeatureMode(Enum):

    Parallel = {
        "module": _Parallel_Package + _Feature_Package,
        "queue": _Parallel_Class + _Queue_Class,
        "lock": _Parallel_Class + _Lock_Class,
        "communication": _Parallel_Class + _Communication_Class
    }

    Concurrent = {
        "module": _Concurrent_Package + _Feature_Package,
        "queue": _Concurrent_Class + _Queue_Class,
        "lock": _Concurrent_Class + _Lock_Class,
        "communication": _Concurrent_Class + _Communication_Class
    }

    GreenThread = {
        "module": _Coroutine_Package + _Feature_Package,
        "queue": _GreenThread_Class + _Queue_Class,
        "lock": _GreenThread_Class + _Lock_Class,
        "communication": _GreenThread_Class + _Communication_Class
    }

    Asynchronous = {
        "module": _Coroutine_Package + _Feature_Package,
        "queue": _Asynchronous_Class + _Queue_Class,
        "lock": _Asynchronous_Class + _Lock_Class,
        "communication": _Asynchronous_Class + _Communication_Class
    }



class RunningMode(Enum):

    Parallel = {
        "strategy_module": _Parallel_Package + _Strategy_Package,
        "class_key": _Parallel_Class,
        "executor_strategy": _Parallel_Class + _Strategy_Class,
        "pool_strategy": _Parallel_Class + _Pool_Strategy_Class
    }

    Concurrent = {
        "strategy_module": _Concurrent_Package + _Strategy_Package,
        "class_key": _Concurrent_Class,
        "executor_strategy": _Concurrent_Class + _Strategy_Class,
        "pool_strategy": _Concurrent_Class + _Pool_Strategy_Class
    }

    GreenThread = {
        "strategy_module": _Coroutine_Package + _Strategy_Package,
        "class_key": _GreenThread_Class,
        "executor_strategy": _GreenThread_Class + _Strategy_Class,
        "pool_strategy": _GreenThread_Class + _Pool_Strategy_Class
    }

    Asynchronous = {
        "strategy_module": _Coroutine_Package + _Strategy_Package,
        "class_key": _Asynchronous_Class,
        "executor_strategy": _Asynchronous_Class + _Strategy_Class,
        "pool_strategy": _Asynchronous_Class + _Pool_Strategy_Class
    }

