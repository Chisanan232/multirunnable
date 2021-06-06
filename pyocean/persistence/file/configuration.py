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
    def file_type(self) -> str:
        """
        Description:
            Get username.
        :return:
        """
        pass


    @property
    @abstractmethod
    def file_name(self) -> str:
        """
        Description:
            Get password.
        :return:
        """
        pass


    @property
    @abstractmethod
    def saving_directory(self) -> str:
        """
        Description:
            Get host.
        :return:
        """
        pass



class BaseConfigurationKey(Enum):

    FILE_TYPE = "type"
    FILE_NAME = "name"
    SAVE_DIRECTORY = "path"



class BaseConfigDefaultValue(Enum):

    FILE_TYPE = ""
    FILE_NAME = ""
    SAVE_DIRECTORY = ""



class PropertiesUtil:

    _Config_Parser: configparser.RawConfigParser = None
    __Properties_Key = "pyocean"

    def __init__(self):
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
        file = os.path.join(root_dir, "sources", "config", "file", "file_config.properties")
        return file
        # file_path = __file__.split(sep="/")[:-1]
        # file_path.extend(["configuration", self.__Database_Driver + "_config.properties"])
        # return "/".join(file_path)


    def get_value_as_str(self, property_key: str) -> str:
        return self.__Config_Parser.get("", property_key)


    def get_value_as_list(self, property_key: str, separate: str = ",") -> List:
        return self.__Config_Parser.get("", property_key).split(separate)


    def property_key(self) -> str:
        """
        Description:
            Get the configuration properties key.
        :return:
        """
        property_key = self.__Properties_Key
        return f"{property_key}.file.local."



class FileConfig(BaseConfiguration):

    __PropertiesOptUtil = None

    def __init__(self):
        self.__PropertiesOptUtil = PropertiesUtil()
        self.__property_key = self.__PropertiesOptUtil.property_key()


    @property
    def file_type(self) -> List[str]:
        return self.__PropertiesOptUtil.get_value_as_list(property_key=f"{self.__property_key}type")


    @property
    def file_name(self) -> List[str]:
        return self.__PropertiesOptUtil.get_value_as_list(property_key=f"{self.__property_key}name")


    @property
    def saving_directory(self) -> List[str]:
        return self.__PropertiesOptUtil.get_value_as_list(property_key=f"{self.__property_key}path")

