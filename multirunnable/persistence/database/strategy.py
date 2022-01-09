from multirunnable.persistence.interface import BasePersistence
from multirunnable.exceptions import GlobalizeObjectError
from multirunnable._utils import get_cls_name as _get_cls_name

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, TypeVar, Generic, cast, Union
from multiprocessing import cpu_count
import logging


T = TypeVar("T")

_Database_Connection_Pools: Dict[str, Any] = {}
_Database_Connection: Generic[T] = None
_Database_Session: Generic[T] = None
_Database_Cursor: Generic[T] = None


def database_connection_pools() -> Dict[str, Any]:
    """
    Description:
        Get the database connection pool which has been globalized.
    :return:
    """
    return _Database_Connection_Pools


def get_connection_pool(pool_name: str) -> Generic[T]:
    """
    Description:
        Get the database connection pool which has been globalized.
    :return:
    """
    try:
        _db_conn_pool = _Database_Connection_Pools[pool_name]
    except KeyError as e:
        return None
    else:
        return _db_conn_pool


class G:
    """
    Description:
        Some operations about getting or setting global variable like connection, cursor or something else.
    """

    @classmethod
    def get_connection(cls) -> Generic[T]:
        return _Database_Connection


    @classmethod
    def set_connection(cls, conn: Generic[T]) -> None:
        global _Database_Connection
        _Database_Connection = conn


    @classmethod
    def get_session(cls) -> Generic[T]:
        return _Database_Session


    @classmethod
    def set_session(cls, conn: Generic[T]) -> None:
        global _Database_Session
        _Database_Session = conn


    @classmethod
    def get_cursor(cls) -> Generic[T]:
        return _Database_Cursor


    @classmethod
    def set_cursor(cls, conn: Generic[T]) -> None:
        global _Database_Cursor
        _Database_Cursor = conn



class BaseDatabaseConnection(BasePersistence):

    """
    Note:
        This class's responsibility is managing database connection and cursor (or session) instances.
        ONLY these instances, it doesn't care about any operations with database.
        Therefore it should consider about sharing instances between multiple different workers.
    """

    _Database_Config: Dict[str, Union[str, int]] = {
        "host": "",
        "port": "",
        "user": "",
        "password": "",
        "database": ""
    }

    __Default_Host = "127.0.0.1"
    __Default_Port = "8080"
    __Default_User = "admin"
    __Default_Password = "password"
    __Default_Database = "default"

    def __init__(self, **kwargs):
        _host = kwargs.get("host", self.__Default_Host)
        _port = kwargs.get("port", self.__Default_Port)
        _user = kwargs.get("user", self.__Default_User)
        _password = kwargs.get("password", self.__Default_Password)
        _database = kwargs.get("database", self.__Default_Database)

        self.database_config = {
            "host": _host,
            "port": _port,
            "user": _user,
            "password": _password,
            "database": _database
        }


    def __str__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}({self._Database_Config})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    def __repr__(self):
        return f"{self.__str__()} at {id(self.__class__)}"


    @property
    def database_config(self) -> Dict[str, object]:
        """
        Description:
            Get all database configuration content.
        :return:
        """
        return self._Database_Config


    @database_config.setter
    def database_config(self, config: Dict[str, Any]) -> None:
        """
        Description:
            Get all database configuration content.
        :return:
        """
        self._Database_Config.update(config)


    def update_database_config(self, key: str, value: Any) -> None:
        """
        Description:
            Get all database configuration content.
        :return:
        """
        self._Database_Config[key] = value


    @property
    @abstractmethod
    def connection(self) -> Generic[T]:
        pass


    @abstractmethod
    def initial(self, **kwargs) -> None:
        """
        Description:
            Initialize something which be needed before operate something with database.
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def connect_database(self, **kwargs) -> Generic[T]:
        """
        Description:
            Connection to database and return the connection or connection pool instance.
        :return:
        """
        pass


    @abstractmethod
    def reconnect(self, timeout: int = 3) -> Generic[T]:
        """
        Description:
            Reconnection to database and return the connection or connection pool instance.
        :return:
        """
        pass


    @abstractmethod
    def get_one_connection(self, **kwargs) -> Generic[T]:
        """
        Description:
            Get one database connection instance.
        :return:
        """
        pass


    @abstractmethod
    def commit(self) -> None:
        """
        Description:
            Commit feature.
        :return:
        """
        pass


    @abstractmethod
    def close(self) -> None:
        """
        Description:
            Close connection and cursor instance.
        :return:
        """
        pass



class BaseSingleConnection(BaseDatabaseConnection, ABC):

    def __init__(self, initial: bool = True, **kwargs):
        super(BaseSingleConnection, self).__init__(**kwargs)
        self._database_connection: Generic[T] = None
        self._database_cursor: Generic[T] = None
        if initial is True:
            self.initial(**self._Database_Config)


    def initial(self, **kwargs) -> None:
        """
        Note:
            Deprecated the method about multiprocessing saving with one connection and change to use multiprocessing
            saving with pool size is 1 connection pool. The reason is database instance of connection pool is already,
            but for the locking situation, we should:
            lock acquire -> new instance -> execute something -> close instance -> lock release . and loop and loop until task finish.
            But connection pool would:
            new connection instances and save to pool -> semaphore acquire -> GET instance (not NEW) ->
            execute something -> release instance back to pool (not CLOSE instance) -> semaphore release

            Because only one connection instance, the every process take turns to using it to saving data. In other words,
            here doesn't need to initial anything about database connection.

        Procedure in multirunnable:
            Multi-workers use the same connection or cursor instance of database.
            Only open it in the initial process and close it in the final ending time.

        New feature in the future:
            Singleton Pattern of each strategies.
        :param kwargs:
        :return:
        """
        if kwargs:
            self._database_connection = self.connect_database(**kwargs)
        else:
            self._database_connection = self.connect_database(**self.database_config)


    def reconnect(self, timeout: int = 3) -> Generic[T]:
        _running_time = 0
        _db_connect_error = None
        while _running_time <= timeout:
            try:
                self._database_connection = self.connect_database(**self.database_config)
            except Exception as e:
                _db_connect_error = e
                logging.error(e)
            if _db_connect_error is None and self._database_connection is not None:
                return self._database_connection

            _running_time += 1
        else:
            if _db_connect_error is not None:
                raise _db_connect_error
            raise ConnectionError(f"It's timeout to retry (Retry value is {timeout}). "
                                  f"Cannot reconnect to database.")


    def get_one_connection(self) -> Generic[T]:
        if self._database_connection is not None:
            return self._database_connection
        self._database_connection = self.connect_database()
        return self._database_connection



class BaseConnectionPool(BaseDatabaseConnection):

    __Default_Pool_Name: str = ""
    __Current_Pool_Name: str = ""

    def __init__(self, initial: bool = True, **kwargs):
        super().__init__(**kwargs)
        _pool_name = cast(str, kwargs.get("pool_name", self.__Default_Pool_Name))
        _pool_size = cast(int, kwargs.get("pool_size", cpu_count()))
        if _pool_size < 0:
            raise ValueError("The database connection pool size cannot less than 0.")

        self.database_config.update({
            "pool_name": _pool_name,
            "pool_size": _pool_size
        })
        self.__Current_Pool_Name = _pool_name

        if initial is True:
            self.initial(**self.database_config)


    def initial(self, **kwargs) -> None:
        """
        Description:
            Target to initialize Process Semaphore and Database connection
            pool object, and globalize them to let processes to use.

        Procedure in smoothcrawler:
            Multi-workers use the same connection or cursor instance of database.
            Only open it in the initial process and close it in the final ending time.

        New feature in the future:
            Singleton Pattern of each strategies. (Be more clearer, lazy initialization of database pool instance.)
        :param kwargs:
        :return:
        """
        self.database_config = kwargs
        # Initialize the Database Connection Instances Pool.
        _db_pool = self.connect_database(**self.database_config)
        # Globalize object to share between different multiple processes
        _pool_name = kwargs.get("pool_name", "")
        Globalize.connection_pool(name=_pool_name, pool=_db_pool)


    @property
    def current_pool_name(self) -> str:
        return self.__Current_Pool_Name


    @current_pool_name.setter
    def current_pool_name(self, pool_name: str) -> None:
        self.__Current_Pool_Name = pool_name


    @property
    def connection(self) -> Generic[T]:
        _connection = self.get_one_connection(pool_name=self.__Current_Pool_Name)
        return _connection


    @property
    def pool_size(self) -> int:
        """
        Description:
            Set the database connection pool size.
            The number of the connection instances which target to do something operators with database.
        Note:
            The number be suggested to be roughly equal to the CPUs amount of host which the program be run.
        :return:
        """
        _db_conn_num = self._Database_Config["pool_size"]
        if _db_conn_num < 0:
            raise ValueError("The database connection pool size cannot less than 0.")

        if _db_conn_num is None or _db_conn_num == 0:
            self._Database_Config["pool_size"] = cpu_count()
            return self._Database_Config["pool_size"]
        else:
            if _db_conn_num > cpu_count():
                logging.warning("Warning about suggestion is the best "
                                "configuration of database connection instance "
                                "should be less than CPU amounts.")
            return _db_conn_num


    @pool_size.setter
    def pool_size(self, pool_size: int) -> None:
        """
        Description:
            Set the database connection pool size.
        :return:
        """
        if pool_size < 0:
            raise ValueError("The database connection pool size cannot less than 0.")

        self._Database_Config["pool_size"] = pool_size


    def reconnect(self, timeout: int = 3) -> Generic[T]:
        _running_time = 0
        _db_connect_error = None
        while _running_time <= timeout:
            _db_pool = None
            try:
                _db_pool = self.connect_database(**self.database_config)
            except Exception as e:
                logging.error(e)
                _db_connect_error = e
            if _db_pool is not None:
                _pool_name = self.database_config.get("pool_name", "")
                Globalize.connection_pool(name=_pool_name, pool=_db_pool)
                return self.get_one_connection(pool_name=_pool_name)

            _running_time += 1
        else:
            if _db_connect_error is not None:
                raise _db_connect_error
            raise ConnectionError("Cannot reconnect to database.")


    @abstractmethod
    def get_one_connection(self, pool_name: str = "", **kwargs) -> Generic[T]:
        """
        Description:
            Get one database connection instance.
        :return:
        """
        pass


    @abstractmethod
    def close_pool(self, pool_name: str) -> None:
        """
        Description:
            Close the database connection pool instance.
        :return:
        """
        pass



class Globalize:

    @staticmethod
    def connection(conn: Generic[T]) -> None:
        if conn is not None:
            global _Database_Connection
            _Database_Connection = conn
        else:
            raise GlobalizeObjectError


    @staticmethod
    def session(session: Generic[T]) -> None:
        if session is not None:
            global _Database_Session
            _Database_Session = session
        else:
            raise GlobalizeObjectError


    @staticmethod
    def cursor(cursor: Generic[T]) -> None:
        if cursor is not None:
            global _Database_Cursor
            _Database_Cursor = cursor
        else:
            raise GlobalizeObjectError


    @staticmethod
    def connection_pool(name: str, pool: Generic[T]) -> None:
        if pool is not None:
            global _Database_Connection_Pools
            _Database_Connection_Pools[name] = pool
        else:
            raise GlobalizeObjectError

