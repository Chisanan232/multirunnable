from pyocean.persistence.database.exceptions import InvalidDriverException, InvalidHostTypeException

from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List
import configparser
import pathlib
import os



class BaseConfiguration(metaclass=ABCMeta):

    @property
    @abstractmethod
    def username(self) -> str:
        """
        Description:
            Get username.
        :return:
        """
        pass


    @property
    @abstractmethod
    def password(self) -> str:
        """
        Description:
            Get password.
        :return:
        """
        pass


    @property
    @abstractmethod
    def host(self) -> str:
        """
        Description:
            Get host.
        :return:
        """
        pass


    @property
    @abstractmethod
    def port(self) -> str:
        """
        Description:
            Get port.
        :return:
        """
        pass


    @property
    @abstractmethod
    def database(self) -> str:
        """
        Description:
            Get database.
        :return:
        """
        pass



class BaseConfigurationKey(Enum):

    USERNAME = "user"
    PASSWORD = "password"
    HOST = "host"
    PORT = "port"
    CLUSTER = "cluster"
    DATABASE = "database"



class BaseConfigDefaultValue(Enum):

    USERNAME = "username"
    PASSWORD = "password"
    HOST = "127.0.0.1"
    PORT = "8080"
    CLUSTER = "cluster"
    DATABASE = "default"



class DatabaseDriver(Enum):

    MySQL = "mysql"
    PostgreSQL = "postgresql"
    Cassandra = "cassandra"
    ClickHouse = "clickhouse"
    MongoDB = "mongodb"
    SQLite = "sqlite"



class HostEnvType(Enum):

    Localhost = "localhost"
    Local = "local"
    Cloud = "cloud"



class PropertiesUtil:

    _Config_Parser: configparser.RawConfigParser = None
    __Properties_Key = "pyocean"
    __Database_Driver = ""
    __Host_Type = ""

    def __init__(self, database_driver: DatabaseDriver, host_type: HostEnvType):
        if isinstance(database_driver, DatabaseDriver):
            self.__Database_Driver = database_driver.value
        else:
            raise InvalidDriverException

        if isinstance(host_type, HostEnvType):
            self.__Host_Type = host_type.value
        else:
            raise InvalidHostTypeException

        self.__Config_Parser = configparser.RawConfigParser()
        config_file = self.__get_config_path()
        ## Method 1.
        # file = open(config_file, encoding="utf-8")
        # self.__Config_Parser.read_file(file, config_file)
        ## Method 2.
        self.__Config_Parser.read(filenames=config_file, encoding="utf-8")


    def __get_config_path(self) -> str:
        """
        Description:
            Get the database configuration file path.
        :return:
        """
        root_dir = pathlib.Path(__file__).parent.parent.parent.parent
        # # deprecated path
        # file = os.path.join(root_dir, "sources", "database_configuration", f"{self.__Database_Driver}_config.properties")
        # # new
        file = os.path.join(root_dir, "sources", "config", "database", f"{self.__Database_Driver}_config.properties")
        return file
        # file_path = __file__.split(sep="/")[:-1]
        # file_path.extend(["configuration", self.__Database_Driver + "_config.properties"])
        # return "/".join(file_path)


    def get_value_as_str(self, property_key: str) -> str:
        return self.__Config_Parser.get(self.__Host_Type, property_key)


    def get_value_as_list(self, property_key: str, separate: str = ",") -> List:
        return self.__Config_Parser.get(self.__Host_Type, property_key).split(separate)


    def property_key(self) -> str:
        """
        Description:
            Get the configuration properties key.
        :return:
        """
        property_key = self.__Properties_Key
        db_driver = self.__Database_Driver
        host_type = self.__Host_Type
        return f"{property_key}.database.{host_type}.{db_driver}."



class DatabaseConfig(BaseConfiguration):

    __PropertiesOptUtil = None

    def __init__(self, database_driver: DatabaseDriver, host_type: HostEnvType):
        self.__PropertiesOptUtil = PropertiesUtil(database_driver=database_driver, host_type=host_type)
        self.__property_key = self.__PropertiesOptUtil.property_key()


    @property
    def username(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(property_key=f"{self.__property_key}username")


    @property
    def password(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(property_key=f"{self.__property_key}password")


    @property
    def host(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(property_key=f"{self.__property_key}host")


    @property
    def port(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(property_key=f"{self.__property_key}port")


    @property
    def database(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(property_key=f"{self.__property_key}database")


