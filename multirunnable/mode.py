from enum import Enum


_Parallel_Package: str = ".parallel."
_Concurrent_Package: str = ".concurrent."
_Coroutine_Package: str = ".coroutine."
_Context_Package: str = "context"
_Strategy_Package: str = "strategy"
_Synchronization_Package: str = "synchronization"
_Queue_Package: str = "queue"


# # Context class
_Context_Class: str = "context"
_GreenThread_Context_Class: str = "green_thread_"
_AsyncTask_Context_Class: str = "async_task_"


# # Strategy class
_Strategy_Class: str = "Strategy"
_General_Strategy_Class: str = "GeneralStrategy"
_Pool_Strategy_Class: str = "PoolStrategy"


# # Feature class
_Parallel_Class: str = "Process"
_Concurrent_Class: str = "Thread"
_GreenThread_Class: str = "GreenThread"
_Asynchronous_Class: str = "Asynchronous"

_Queue_Class: str = "Queue"
_Lock_Class: str = "Lock"
_Communication_Class: str = "Communication"



class ContextMode(Enum):

    Parallel = {
        "module": _Parallel_Package + _Context_Package,
        "context": _Context_Class
    }

    Concurrent = {
        "module": _Concurrent_Package + _Context_Package,
        "context": _Context_Class
    }

    GreenThread = {
        "module": _Coroutine_Package + _Context_Package,
        "context": _GreenThread_Context_Class + _Context_Class
    }

    Asynchronous = {
        "module": _Coroutine_Package + _Context_Package,
        "context": _AsyncTask_Context_Class + _Context_Class
    }



class FeatureMode(Enum):

    Parallel = {
        "module": _Parallel_Package + _Synchronization_Package,
        "queue": _Parallel_Class + _Queue_Class,
        "lock": _Parallel_Class + _Lock_Class,
        "communication": _Parallel_Class + _Communication_Class
    }

    Concurrent = {
        "module": _Concurrent_Package + _Synchronization_Package,
        "queue": _Concurrent_Class + _Queue_Class,
        "lock": _Concurrent_Class + _Lock_Class,
        "communication": _Concurrent_Class + _Communication_Class
    }

    GreenThread = {
        "module": _Coroutine_Package + _Synchronization_Package,
        "queue": _GreenThread_Class + _Queue_Class,
        "lock": _GreenThread_Class + _Lock_Class,
        "communication": _GreenThread_Class + _Communication_Class
    }

    Asynchronous = {
        "module": _Coroutine_Package + _Synchronization_Package,
        "queue": _Asynchronous_Class + _Queue_Class,
        "lock": _Asynchronous_Class + _Lock_Class,
        "communication": _Asynchronous_Class + _Communication_Class
    }



class RunningMode(Enum):

    Parallel = {
        "strategy_module": _Parallel_Package + _Strategy_Package,
        "class_key": _Parallel_Class,
        "executor_strategy": _Parallel_Class + _Strategy_Class,
        "pool_strategy": _Parallel_Class + _Pool_Strategy_Class,
        "feature": FeatureMode.Parallel,
        "context": ContextMode.Parallel
    }

    Concurrent = {
        "strategy_module": _Concurrent_Package + _Strategy_Package,
        "class_key": _Concurrent_Class,
        "executor_strategy": _Concurrent_Class + _Strategy_Class,
        "pool_strategy": _Concurrent_Class + _Pool_Strategy_Class,
        "feature": FeatureMode.Concurrent,
        "context": ContextMode.Concurrent
    }

    GreenThread = {
        "strategy_module": _Coroutine_Package + _Strategy_Package,
        "class_key": _GreenThread_Class,
        "executor_strategy": _GreenThread_Class + _Strategy_Class,
        "pool_strategy": _GreenThread_Class + _Pool_Strategy_Class,
        "feature": FeatureMode.GreenThread,
        "context": ContextMode.GreenThread
    }

    Asynchronous = {
        "strategy_module": _Coroutine_Package + _Strategy_Package,
        "class_key": _Asynchronous_Class,
        "executor_strategy": _Asynchronous_Class + _Strategy_Class,
        "pool_strategy": _Asynchronous_Class + _Pool_Strategy_Class,
        "feature": FeatureMode.Asynchronous,
        "context": ContextMode.Asynchronous
    }

