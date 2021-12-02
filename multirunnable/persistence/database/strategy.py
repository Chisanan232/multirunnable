import logging

from multirunnable.persistence.interface import BasePersistence
# from multirunnable.persistence.configuration import BaseDatabaseConfiguration
# from multirunnable.persistence.database.configuration import ConfigKey, DefaultConfig
from multirunnable.exceptions import GlobalizeObjectError
from multirunnable._singletons import NamedSingletonMeta
from multirunnable._utils import get_cls_name as _get_cls_name

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, TypeVar, Generic, cast, Union
from collections import defaultdict
from multiprocessing import cpu_count


T = TypeVar("T")

Database_Connection_Pools: Dict[str, Any] = {}
Database_Connection: Generic[T] = None
Database_Session: Generic[T] = None
Database_Cursor: Generic[T] = None


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

    # _Database_Connection: Generic[T] = None
    # _Database_Cursor: Generic[T] = None

    # def __init__(self, configuration: BaseDatabaseConfiguration = None, **kwargs):
    def __init__(self, **kwargs):
        self._database_connection: Generic[T] = None
        self._database_cursor: Generic[T] = None

        # # # # Deprecated
        # if configuration is not None:
        #     __username_val = configuration.username
        #     __password_val = configuration.password
        #     __host_val = configuration.host
        #     __port_val = configuration.port
        #     __database_val = configuration.database
        # else:
        #     __host_val = DefaultConfig.HOST.value
        #     __port_val = DefaultConfig.PORT.value
        #     __username_val = DefaultConfig.USERNAME.value
        #     __password_val = DefaultConfig.PASSWORD.value
        #     __database_val = DefaultConfig.DATABASE.value
        #
        # self._Database_Config[ConfigKey.USERNAME.value] = __username_val
        # self._Database_Config[ConfigKey.PASSWORD.value] = __password_val
        # self._Database_Config[ConfigKey.HOST.value] = __host_val
        # self._Database_Config[ConfigKey.PORT.value] = __port_val
        # self._Database_Config[ConfigKey.DATABASE.value] = __database_val

        _host = kwargs.get("host", self.__Default_Host)
        _port = kwargs.get("port", self.__Default_Port)
        _user = kwargs.get("user", self.__Default_User)
        _password = kwargs.get("password", self.__Default_Password)
        _database = kwargs.get("database", self.__Default_Database)

        self._Database_Config.update({
            "host": _host,
            "port": _port,
            "user": _user,
            "password": _password,
            "database": _database
        })


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
    def connection(self) -> Generic[T]:
        return self._database_connection


    @connection.setter
    def connection(self, conn: Generic[T]) -> None:
        self._database_connection = conn


    @property
    def cursor(self) -> Generic[T]:
        return self._database_cursor


    @cursor.setter
    def cursor(self, cur: Generic[T]) -> None:
        self._database_cursor = cur


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
    def get_one_connection(self) -> Generic[T]:
        """
        Description:
            Get one database connection instance.
        :return:
        """
        pass


    @abstractmethod
    def build_cursor(self) -> Generic[T]:
        """
        Description:
            Build cursor instance of one specific connection instance.
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



class BaseSingleConnection(BaseDatabaseConnection, ABC, metaclass=NamedSingletonMeta):

    def __init__(self, **kwargs):
        super(BaseSingleConnection, self).__init__(**kwargs)
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
        self.database_config = kwargs
        # # # # Global version
        # global Database_Connection, Database_Cursor
        # Database_Connection = self.connect_database(**kwargs)
        # Database_Cursor = self.build_cursor()
        # # # # Current
        print(f"[DEBUG] database config: {self.database_config}")
        self._database_connection = self.connect_database(**self.database_config)
        self._database_cursor = self.build_cursor()


    def get_one_connection(self) -> Generic[T]:
        if self.connection is not None:
            return self.connection
        self.connection = self.connect_database()
        return self.connection



class BaseConnectionPool(BaseDatabaseConnection):

    __Default_Pool_Name: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _pool_name = cast(str, kwargs.get("pool_name", self.__Default_Pool_Name))
        _pool_size = cast(int, kwargs.get("pool_size", cpu_count()))

        self._Database_Config.update({
            "pool_name": _pool_name,
            "pool_size": _pool_size
        })

        self.initial(**self._Database_Config)


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
        # # # # Old version
        # # Get value
        # __db_connection_number = cast(int, kwargs["db_conn_num"])
        # __pool_name = kwargs.get("pool_name", self.__Default_Pool_Name)
        #
        # # # Database Connections Pool part
        # # Initialize the Database Connection Instances Pool.
        # database_connections_pool = self.connect_database(pool_name=__pool_name, pool_size=__db_connection_number)
        # # Globalize object to share between different multiple processes
        # Globalize.connection_pool(pool=database_connections_pool)

        # # # # New version
        self.database_config = kwargs
        # Initialize the Database Connection Instances Pool.
        _db_pool = self.connect_database(**self.database_config)
        # Globalize object to share between different multiple processes
        _pool_name = kwargs.get("pool_name", "")
        Globalize.connection_pool(name=_pool_name, pool=_db_pool)


    @property
    def pool_size(self) -> int:
        """
        Description:
            Set the database connection pool size.
        :return:
        """
        return self._Database_Config["pool_size"]


    @pool_size.setter
    def pool_size(self, pool_size: int) -> None:
        """
        Description:
            Set the database connection pool size.
        :return:
        """
        self._Database_Config["pool_size"] = pool_size


    @property
    def database_connection_pools(self) -> Dict[str, Any]:
        """
        Description:
            Get the database connection pool which has been globalized.
        :return:
        """
        return Database_Connection_Pools


    def get_connection_pool(self, pool_name: str) -> Generic[T]:
        """
        Description:
            Get the database connection pool which has been globalized.
        :return:
        """
        try:
            _db_conn_pool = Database_Connection_Pools[pool_name]
        except KeyError as e:
            return None
        else:
            return _db_conn_pool


    @abstractmethod
    def close_pool(self) -> None:
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
            global Database_Connection
            Database_Connection = conn
        else:
            raise GlobalizeObjectError


    @staticmethod
    def session(session: Generic[T]) -> None:
        if session is not None:
            global Database_Session
            Database_Session = session
        else:
            raise GlobalizeObjectError


    @staticmethod
    def cursor(cursor: Generic[T]) -> None:
        if cursor is not None:
            global Database_Cursor
            Database_Cursor = cursor
        else:
            raise GlobalizeObjectError


    @staticmethod
    def connection_pool(name: str, pool: Generic[T]) -> None:
        if pool is not None:
            global Database_Connection_Pools
            Database_Connection_Pools[name] = pool
        else:
            raise GlobalizeObjectError

