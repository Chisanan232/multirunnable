from enum import Enum
from typing import Dict


_Package: str = "pyocean"
_Parallel_Module: str = ".parallel.features"
_Concurrent_Module: str = ".concurrent.features"
_Coroutine_Module: str = ".coroutine.features"


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

    MultiProcessing: Dict[str, str] = {
        "module": _Parallel_Module,
        "queue": _Parallel_Feature_Class + _Queue_Class,
        "lock": _Parallel_Feature_Class + _Lock_Class,
        "communication": _Parallel_Feature_Class + _Communication_Class
    }

    MultiThreading: Dict[str, str] = {
        "module": _Concurrent_Module,
        "queue": _Concurrent_Feature_Class + _Queue_Class,
        "lock": _Concurrent_Feature_Class + _Lock_Class,
        "communication": _Concurrent_Feature_Class + _Communication_Class
    }

    MultiGreenlet: Dict[str, str] = {
        "module": _Coroutine_Module,
        "queue": _Greenlet_Feature_Class + _Queue_Class,
        "lock": _Greenlet_Feature_Class + _Lock_Class,
        "communication": _Greenlet_Feature_Class + _Communication_Class
    }

    Asynchronous: Dict[str, str] = {
        "module": _Coroutine_Module,
        "queue": _Async_Feature_Class + _Queue_Class,
        "lock": _Async_Feature_Class + _Lock_Class,
        "communication": _Async_Feature_Class + _Communication_Class
    }



class FactoryMode(Enum):

    Parallel: Dict[str, str] = {
        "simple_factory": _Parallel_Common_Class + _Simple_Factory_Class,
        "persistence_database_factory": _Parallel_Common_Class + _Persistence_Database_Factory_Class,
        "persistence_file_factory": _Parallel_Common_Class + _Persistence_File_Factory_Class
    }

    Concurrent: Dict[str, str] = {
        "simple_factory": _Concurrent_Common_Class + _Simple_Factory_Class,
        "persistence_database_factory": _Concurrent_Common_Class + _Persistence_Database_Factory_Class,
        "persistence_file_factory": _Concurrent_Common_Class + _Persistence_File_Factory_Class
    }

    Greenlet: Dict[str, str] = {
        "simple_factory": _Greenlet_Common_Class + _Simple_Factory_Class,
        "persistence_database_factory": _Greenlet_Common_Class + _Persistence_Database_Factory_Class,
        "persistence_file_factory": _Greenlet_Common_Class + _Persistence_File_Factory_Class
    }

    Asynchronous: Dict[str, str] = {
        "simple_factory": _Async_Common_Class + _Simple_Factory_Class,
        "persistence_database_factory": _Async_Common_Class + _Persistence_Database_Factory_Class,
        "persistence_file_factory": _Async_Common_Class + _Persistence_File_Factory_Class
    }



class ProcedureMode(Enum):

    Parallel: Dict[str, str] = {
        "procedure": _Parallel_Common_Class + _Procedure_Class
    }

    Concurrent: Dict[str, str] = {
        "procedure": _Concurrent_Common_Class + _Procedure_Class
    }

    Greenlet: Dict[str, str] = {
        "procedure": _Greenlet_Common_Class + _Procedure_Class
    }

    Asynchronous: Dict[str, str] = {
        "procedure": _Async_Common_Class + _Procedure_Class
    }



class StrategyMode(Enum):

    Parallel: Dict[str, str] = {
        "strategy": _Parallel_Common_Class + _Strategy_Class
    }

    Concurrent: Dict[str, str] = {
        "strategy": _Concurrent_Common_Class + _Strategy_Class
    }

    Greenlet: Dict[str, str] = {
        "strategy": _Greenlet_Common_Class + _Strategy_Class
    }

    Asynchronous: Dict[str, str] = {
        "strategy": _Async_Common_Class + _Strategy_Class
    }

