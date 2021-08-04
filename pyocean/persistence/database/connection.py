from pyocean.persistence.interface import OceanPersistence
from pyocean.persistence.configuration import BaseDatabaseConfiguration
from pyocean.persistence.database.configuration import BaseConfigurationKey, BaseConfigDefaultValue

from abc import abstractmethod
from typing import Dict



class BaseConnection(OceanPersistence):

    _Database_Config: Dict[str, object] = {
        "user": "",
        "password": "",
        "host": "",
        "port": "",
        "database": ""
    }

    def __init__(self, configuration: BaseDatabaseConfiguration = None):
        if configuration is not None:
            __username_val = configuration.username
            __password_val = configuration.password
            __host_val = configuration.host
            __port_val = configuration.port
            __database_val = configuration.database
        else:
            __username_val = BaseConfigDefaultValue.USERNAME.value
            __password_val = BaseConfigDefaultValue.PASSWORD.value
            __host_val = BaseConfigDefaultValue.HOST.value
            __port_val = BaseConfigDefaultValue.PORT.value
            __database_val = BaseConfigDefaultValue.DATABASE.value

        self._Database_Config[BaseConfigurationKey.USERNAME.value] = __username_val
        self._Database_Config[BaseConfigurationKey.PASSWORD.value] = __password_val
        self._Database_Config[BaseConfigurationKey.HOST.value] = __host_val
        self._Database_Config[BaseConfigurationKey.PORT.value] = __port_val
        self._Database_Config[BaseConfigurationKey.DATABASE.value] = __database_val


    @property
    def database_config(self) -> Dict[str, object]:
        """
        Description:
            Get all database configuration content.
        :return:
        """
        return self._Database_Config


    @abstractmethod
    def initialize(self, **kwargs) -> None:
        """
        Description:
            Initialize something which be needed before operate something with database.
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def connect_database(self, **kwargs) -> object:
        """
        Description:
            Connection to database and return the connection or connection pool instance.
        :return:
        """
        pass


    @abstractmethod
    def get_one_connection(self) -> object:
        """
        Description:
            Get one database connection instance.
        :return:
        """
        pass


    @abstractmethod
    def build_cursor(self, connection: object) -> object:
        """
        Description:
            Build cursor instance of one specific connection instance.
        :return:
        """
        pass


    @abstractmethod
    def close_instance(self, connection: object, cursor: object) -> None:
        """
        Description:
            Close connection and cursor instance.
        :return:
        """
        pass

