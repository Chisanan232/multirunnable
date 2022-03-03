from multirunnable.adapter.context import context
from multirunnable.persistence.interface import BasePersistence
from multirunnable.exceptions import GlobalizeObjectError

from abc import ABC, abstractmethod
from typing import Dict, Any, TypeVar, Generic, cast, Union
from collections import defaultdict
from multiprocessing import cpu_count
import logging


T = TypeVar("T")

_Database_Connection_Pools: Dict[str, Any] = {}


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



class BaseDatabaseConnection(BasePersistence):

    """
    Note:
        This class's responsibility is managing database connection and cursor (or session) instances.
        ONLY these instances, it doesn't care about any operations with database.
        Therefore it should consider about sharing instances between multiple different workers.
    """

    _DB_Connection_Config: Dict[str, Dict[str, Any]] = None

    _Default_Host: str = "127.0.0.1"
    _Default_Port: str = None
    _Default_User: str = "root"
    _Default_Password: str = "password"
    _Default_Database: str = "default"

    _Default_DB_Conn_Config: Dict[str, Any] = {
        "host": _Default_Host,
        "port": _Default_Port,
        "user": _Default_User,
        "password": _Default_Password,
        "database": _Default_Database,
    }

    _Default_Reconnect_Timeout: int = 3

    def __init__(self, **kwargs):
        self._DB_Connection_Config = defaultdict(lambda: self._Default_DB_Conn_Config)

        self._host = kwargs.get("host", self._Default_Host)
        self._port = kwargs.get("port", self._Default_Port)
        self._user = kwargs.get("user", self._Default_User)
        self._password = kwargs.get("password", self._Default_Password)
        self._database = kwargs.get("database", self._Default_Database)

        self._current_database_config = {
            "host": self._host,
            "port": self._port,
            "user": self._user,
            "password": self._password,
            "database": self._database
        }

        _instance_cls_name = self.__class__.__name__
        self._DB_Connection_Config.update({str(_instance_cls_name): self._current_database_config})


    def __repr__(self):
        return f"{self.__class__.__name__}({self.database_config}) at {id(self.__class__)}"


    @property
    def database_config(self) -> Dict[str, object]:
        """
        Description:
            Get all database configuration content.
        :return:
        """
        _instance_cls_name = self.__class__.__name__
        _db_config = self._DB_Connection_Config[_instance_cls_name]
        return _db_config


    @database_config.setter
    def database_config(self, config: Dict[str, Any]) -> None:
        """
        Description:
            Get all database configuration content.
        :return:
        """
        _instance_cls_name = self.__class__.__name__
        self._DB_Connection_Config.update({str(_instance_cls_name): config})


    def update_database_config(self, key: str, value: Any) -> None:
        """
        Description:
            Get all database configuration content.
        :return:
        """
        _instance_cls_name = self.__class__.__name__
        self._DB_Connection_Config[str(_instance_cls_name)][key] = value


    def get_all_database_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Description:
            Get all database configurations.
        :return:
        """
        return self._DB_Connection_Config


    @property
    @abstractmethod
    def current_connection(self) -> Union[Any, Dict[str, Any]]:
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
    def reconnect(self, timeout: int = 3, force: bool = False) -> Generic[T]:
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


    def is_connected(self, **kwargs) -> bool:
        """
        Description:
            It returns True if the connection instance is connected with database, or it returns False.
        :return:
        """
        pass


    @abstractmethod
    def commit(self, **kwargs) -> None:
        """
        Description:
            Commit the execution to database.
        :return:
        """
        pass


    @abstractmethod
    def close_connection(self, **kwargs) -> None:
        """
        Description:
            Close the database connection instance.
        :return:
        """
        pass



class BaseSingleConnection(BaseDatabaseConnection, ABC):

    def __init__(self, initial: bool = True, **kwargs):
        super(BaseSingleConnection, self).__init__(**kwargs)
        self._database_connection: Generic[T] = None
        self._database_cursor: Generic[T] = None
        self._connection_is_connected: bool = False

        if initial is True:
            self.initial(**self.database_config)


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
        self.database_config.update(kwargs)
        self._database_connection = self.connect_database(**self.database_config)


    @property
    def current_connection(self) -> Generic[T]:
        """
        Note:
            For resolving this issue, we should do something to avoid this issue.
            However, it has exception about "TypeError: can't pickle _mysql_connector.MySQL objects" for database package.
        :return:
        """
        return self._database_connection


    def is_connected(self) -> bool:
        return self._connection_is_connected


    def get_one_connection(self) -> Generic[T]:
        if self._database_connection is not None and self.is_connected() is True:
            return self._database_connection
        self._database_connection = self.connect_database(**self.database_config)
        return self._database_connection


    def connect_database(self, **kwargs) -> Generic[T]:
        """
        Description:
            Connection to database and return the connection or connection pool instance.
        :return:
        """
        _connection = self._connect_database(**kwargs)
        self._connection_is_connected = True
        return _connection


    @abstractmethod
    def _connect_database(self, **kwargs) -> Generic[T]:
        """
        Description:
            Connection to database and return the connection or connection pool instance.
        :return:
        """
        pass


    def reconnect(self, timeout: int = 3, force: bool = False) -> Generic[T]:
        if force is False and self._database_connection is not None and self.is_connected() is True:
            return self._database_connection

        _running_time = 0
        _db_connect_error = None
        while _running_time <= timeout:
            try:
                self._database_connection = self.connect_database(**self.database_config)
            except Exception as e:
                _db_connect_error = e
                logging.error(e)
            else:
                if self._database_connection is not None and self.is_connected() is True:
                    return self._database_connection

            _running_time += 1
        else:
            if _db_connect_error is not None:
                raise _db_connect_error from _db_connect_error
            raise ConnectionError(f"It's timeout to retry (Retry value is {timeout}). "
                                  f"Cannot reconnect to database.")


    @abstractmethod
    def commit(self) -> None:
        """
        Description:
            Commit the execution to database.
        :return:
        """
        pass


    def close_connection(self) -> None:
        """
        Description:
            Close connection instance.
        :return:
        """
        self._close_connection()
        self._connection_is_connected = False


    @abstractmethod
    def _close_connection(self) -> None:
        """
        Description:
            The implementation of closing connection instance.
        :return:
        """
        pass



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
        self._current_db_conn: Dict[str, Generic[T]] = defaultdict(lambda: None)
        self._connection_is_connected: Dict[str, bool] = defaultdict(lambda: False)

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
        self.database_config.update(kwargs)
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
    def pool_size(self) -> int:
        """
        Description:
            Set the database connection pool size.
            The number of the connection instances which target to do something operators with database.
        Note:
            The number be suggested to be roughly equal to the CPUs amount of host which the program be run.
        :return:
        """
        _db_conn_num: int = cast(int, self.database_config["pool_size"])
        if _db_conn_num < 0:
            raise ValueError("The database connection pool size cannot less than 0.")

        if _db_conn_num is None or _db_conn_num == 0:
            self.database_config["pool_size"] = cpu_count()
            return cast(int, self.database_config["pool_size"])
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

        self.database_config["pool_size"] = pool_size


    @abstractmethod
    def connect_database(self, **kwargs) -> Generic[T]:
        """
        Description:
            Connection to database and return the connection or connection pool instance.
        :return:
        """
        pass


    def reconnect(self, timeout: int = 3, force: bool = False) -> Generic[T]:
        _running_time = 0
        _db_connect_error = None
        while _running_time <= timeout:
            _db_pool = None
            try:
                _db_pool = self.connect_database(**self.database_config)
            except Exception as e:
                logging.error(e)
                _db_connect_error = e
            else:
                if _db_pool is not None:
                    _pool_name = self.database_config.get("pool_name", "")
                    Globalize.connection_pool(name=_pool_name, pool=_db_pool)

                    _conn_key = self._get_connections_key()
                    if force is True or self._current_db_conn[_conn_key] is None or self._connection_is_connected[_conn_key] is False:
                        self._current_db_conn[_conn_key] = self.get_one_connection(pool_name=_pool_name)

                    if self._current_db_conn[_conn_key] is not None and self._connection_is_connected[_conn_key] is True:
                        return self._current_db_conn[_conn_key]

            _running_time += 1
        else:
            if _db_connect_error is not None:
                raise _db_connect_error from _db_connect_error
            raise ConnectionError("Cannot reconnect to database.")


    @property
    def current_connection(self) -> Dict[str, Any]:
        _conn_key = self._get_connections_key()
        return self._current_db_conn[_conn_key]


    def is_connected(self) -> bool:
        _conn_key = self._get_connections_key()
        return self._connection_is_connected[_conn_key]


    def get_one_connection(self, pool_name: str = "", **kwargs) -> Generic[T]:
        """
        Description:
            Get one database connection instance.
        :return:
        """
        _pools = database_connection_pools()
        if pool_name not in _pools.keys():
            raise ValueError(f"Cannot get the one connection instance from connection pool because it doesn't exist the connection pool with the name '{pool_name}'.")

        _conn_key = self._get_connections_key()
        _connection = self._get_one_connection(pool_name=pool_name, **kwargs)
        self._current_db_conn[_conn_key] = _connection
        self._connection_is_connected[_conn_key] = True
        return _connection


    @abstractmethod
    def _get_one_connection(self, pool_name: str = "", **kwargs) -> Generic[T]:
        """
        Description:
            The truly implementation to let sub-class to implement to get one database connection instance from connection pool.
        :return:
        """
        pass


    def commit(self, conn: Any = None) -> None:
        _conn = conn
        if _conn is None:
            _conn_key = self._get_connections_key()
            _conn = self._current_db_conn[_conn_key]
            assert _conn is not None, f"The database connection instance with key '{_conn_key}' shouldn't be None object.'"
        self._commit(conn=_conn)


    @abstractmethod
    def _commit(self, conn: Any) -> None:
        """
        Description:
            The truly implementation to let sub-class to implement to commit the execution to database by the connection instance.
        :return:
        """
        pass


    def close_connection(self, conn: Any = None) -> None:
        """
        Description:
            Close connection instance.
        :return:
        """
        _conn_key = self._get_connections_key()
        if conn is None:
            conn = self._current_db_conn[_conn_key]
        self._close_connection(conn=conn)
        self._connection_is_connected[_conn_key] = False


    @abstractmethod
    def _close_connection(self, conn: Any) -> None:
        """
        Description:
            The truly implementation to let sub-class to implement to close connection instance.
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


    def _get_connections_key(self) -> str:
        """
        Description:
            In the ConnectionPoolStrategy, it would save the connection instance by the worker name (ex: Process-1, Thread-1, etc).
            This method responses of how it determine the key index to save it.
        :return:
        """
        _ident = context.get_current_worker_name()
        _cls_name = self.__class__.__name__
        return f"{_cls_name}_{_ident}"



class Globalize:

    @staticmethod
    def connection_pool(name: str, pool: Generic[T]) -> None:
        if pool is not None:
            global _Database_Connection_Pools
            _Database_Connection_Pools[name] = pool
        else:
            raise GlobalizeObjectError

