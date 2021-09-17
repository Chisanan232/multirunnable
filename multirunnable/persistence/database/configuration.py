from multirunnable.persistence.mode import PersistenceMode, DatabaseDriver
from multirunnable.persistence.configuration import PropertiesUtil, BaseDatabaseConfiguration

from enum import Enum



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



class DatabaseConfig(BaseDatabaseConfiguration):

    __PropertiesOptUtil = None
    __Mode = PersistenceMode.DATABASE

    def __init__(self, config_path: str, database_driver: DatabaseDriver):
        # self.__PropertiesOptUtil = PropertiesUtil(database_driver=database_driver, host_type=host_type)
        self.__PropertiesOptUtil = PropertiesUtil(
            mode=self.__Mode,
            config_path=config_path,
            database_driver=database_driver)
        self.__database_driver = database_driver.value.get("properties_key", "")
        self.__property_key = self.__PropertiesOptUtil.property_key()


    @property
    def username(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(
            group=self.__database_driver,
            property_key=".".join([self.__property_key, "username"]))


    @property
    def password(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(
            group=self.__database_driver,
            property_key=".".join([self.__property_key, "password"]))


    @property
    def host(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(
            group=self.__database_driver,
            property_key=".".join([self.__property_key, "host"]))


    @property
    def port(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(
            group=self.__database_driver,
            property_key=".".join([self.__property_key, "port"]))


    @property
    def database(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(
            group=self.__database_driver,
            property_key=".".join([self.__property_key, "database"]))

