from abc import ABCMeta, abstractmethod
from typing import List
import configparser
import pathlib
import os



class PropertiesUtil:

    __Properties_Utils_Instance = None
    _Config_Parser: configparser.RawConfigParser = None
    _Config_Parser_Encoding: str = "utf-8"
    __Properties_Key = "pyocean"

    def __new__(cls, *args, **kwargs):
        if cls.__Properties_Utils_Instance is None:
            return super(PropertiesUtil, cls).__new__(cls)
        return cls.__Properties_Utils_Instance


    def __init__(self, config_path: str = None):
        self.__Config_Parser = configparser.RawConfigParser()
        if config_path is None:
            __config_file_path = self.__get_config_path()
        else:
            __config_file_path = config_path
        ## Method 1.
        # file = open(config_file, encoding="utf-8")
        # self.__Config_Parser.read_file(file, config_file)
        ## Method 2.
        self.__Config_Parser.read(
            filenames=__config_file_path,
            encoding=self._Config_Parser_Encoding
        )


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


    def get_value_as_str(self, property_key: str, group: str = "") -> str:
        __group = self.__get_properties_group(group=group)
        return self.__Config_Parser.get(__group, property_key)


    def get_value_as_list(self, property_key: str, group: str = "", separate: str = ",") -> List:
        __group = self.__get_properties_group(group=group)
        return self.__Config_Parser.get(__group, property_key).split(separate)


    def __get_properties_group(self, group: str) -> str:
        return group[0].upper() + group[1:]


    def property_key(self, group: str) -> str:
        """
        Description:
            Get the configuration properties key.
        :return:
        """
        property_key = self.__Properties_Key
        return f"{property_key}.{group}.local."



class BaseConfiguration(metaclass=ABCMeta):

    pass



class DatabaseConfiguration(BaseConfiguration):

    pass



class FileConfiguration(BaseConfiguration):

    pass

