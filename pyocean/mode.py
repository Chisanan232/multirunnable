from enum import Enum


_Package: str = "pyocean"
_Parallel_Module: str = ".parallel."
_Concurrent_Module: str = ".concurrent."
_Coroutine_Module: str = ".coroutine."
_Feature_Module: str = "features"
_Factory_Module: str = "factory"
_Strategy_Module: str = "strategy"
_Operator_Module: str = "operator"


# # Feature class
_Parallel_Feature_Class: str = "Process"
_Concurrent_Feature_Class: str = "Thread"
_Greenlet_Feature_Class: str = "Greenlet"
_Async_Feature_Class: str = "Async"

_Queue_Class: str = "Queue"
_Lock_Class: str = "Lock"
_Communication_Class: str = "Communication"


# # Factory, Procedure, Strategy class
_Parallel_Common_Class: str = "MultiProcessing"
_Concurrent_Common_Class: str = "MultiThreading"
_Greenlet_Common_Class: str = "MultiGreenlet"
_Async_Common_Class: str = "Asynchronous"

_Simple_Factory_Class: str = "SimpleFactory"
_Persistence_Database_Factory_Class: str = "PersistenceDatabaseFactory"
_Persistence_File_Factory_Class: str = "PersistenceFileFactory"

_Procedure_Class: str = "Procedure"

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
        "factory_module": _Parallel_Module + _Factory_Module,
        "simple_factory": _Parallel_Common_Class + _Simple_Factory_Class,
        "persistence_database_factory": _Parallel_Common_Class + _Persistence_Database_Factory_Class,
        "persistence_file_factory": _Parallel_Common_Class + _Persistence_File_Factory_Class,
        "operator_module": _Parallel_Module + _Operator_Module,
        "procedure": _Parallel_Common_Class + _Procedure_Class,
        "strategy_module": _Parallel_Module + _Strategy_Module,
        "strategy": _Parallel_Common_Class + _Strategy_Class
    }

    Concurrent = {
        "factory_module": _Concurrent_Module + _Factory_Module,
        "simple_factory": _Concurrent_Common_Class + _Simple_Factory_Class,
        "persistence_database_factory": _Concurrent_Common_Class + _Persistence_Database_Factory_Class,
        "persistence_file_factory": _Concurrent_Common_Class + _Persistence_File_Factory_Class,
        "operator_module": _Concurrent_Module + _Operator_Module,
        "procedure": _Concurrent_Common_Class + _Procedure_Class,
        "strategy_module": _Concurrent_Module + _Strategy_Module,
        "strategy": _Concurrent_Common_Class + _Strategy_Class
    }

    Greenlet = {
        "factory_module": _Coroutine_Module + _Factory_Module,
        "simple_factory": _Greenlet_Common_Class + _Simple_Factory_Class,
        "persistence_database_factory": _Greenlet_Common_Class + _Persistence_Database_Factory_Class,
        "persistence_file_factory": _Greenlet_Common_Class + _Persistence_File_Factory_Class,
        "operator_module": _Coroutine_Module + _Operator_Module,
        "procedure": _Greenlet_Common_Class + _Procedure_Class,
        "strategy_module": _Coroutine_Module + _Strategy_Module,
        "strategy": _Greenlet_Common_Class + _Strategy_Class
    }

    Asynchronous = {
        "factory_module": _Coroutine_Module + _Factory_Module,
        "simple_factory": _Async_Common_Class + _Simple_Factory_Class,
        "persistence_database_factory": _Async_Common_Class + _Persistence_Database_Factory_Class,
        "persistence_file_factory": _Async_Common_Class + _Persistence_File_Factory_Class,
        "operator_module": _Coroutine_Module + _Operator_Module,
        "procedure": _Async_Common_Class + _Procedure_Class,
        "strategy_module": _Coroutine_Module + _Strategy_Module,
        "strategy": _Async_Common_Class + _Strategy_Class
    }

