from pyocean.persistence.mode import PersistenceMode
from pyocean.persistence.configuration import PropertiesUtil, BaseFileConfiguration, BaseArchiverConfiguration

from abc import ABCMeta
from typing import List
from enum import Enum
import configparser
import pathlib
import os

from deprecation import deprecated



class SupportConfig:

    File_Format: List[str] = ["json", "csv", "xlsx"]
    Data_String_Format: List[str] = ["json", "csv"]
    Archiver_Format: List[str] = ["zip"]



class ConfigType(Enum):

    FILE_GROUP = "file"
    ARCHIVER_GROUP = "archiver"



class DefaultConfig(Enum):

    FILE_TYPE = "json"
    FILE_NAME = "example_data"
    FILE_SAVE_DIRECTORY = "/Users/bryantliu/Downloads"

    ARCHIVER_TYPE = "zip"
    ARCHIVER_PATH = "/Users/bryantliu/Downloads/example_data"



@deprecated(
    deprecated_in="0.7.3",
    removed_in="0.8.1",
    current_version="0.7.3",
    details="Moving the object and annotation to template object.")
class OldPropertiesUtil:

    __Properties_Utils_Instance = None
    _Config_Parser: configparser.RawConfigParser = None
    __Properties_Key = "pyocean"

    def __new__(cls, *args, **kwargs):
        if cls.__Properties_Utils_Instance is None:
            return super(OldPropertiesUtil, cls).__new__(cls)
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
            encoding="utf-8"
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



@deprecated(
    deprecated_in="0.7.3",
    removed_in="0.8.1",
    current_version="0.7.3",
    details="Moving the object and annotation to template object.")
class BaseFileConfig(metaclass=ABCMeta):

    pass



class FileConfig(BaseFileConfiguration):

    __PropertiesOptUtil = None
    __Config_Type = ConfigType.FILE_GROUP.value
    __Mode = PersistenceMode.FILE

    __File_Type = None
    __File_Name = None
    __File_Save_Dir = None

    def __init__(self, config_path: str = None):
        self.__PropertiesOptUtil = PropertiesUtil(mode=self.__Mode, config_path=config_path)
        self.__property_key = self.__PropertiesOptUtil.property_key()


    @property
    def file_type(self) -> List[str]:
        return self.__PropertiesOptUtil.get_value_as_list(
            group=self.__Config_Type,
            property_key=".".join([self.__property_key, "type"]))


    @file_type.setter
    def file_type(self, file_type: str) -> None:
        self.__File_Type = file_type


    @property
    def file_name(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(
            group=self.__Config_Type,
            property_key=".".join([self.__property_key, "name"]))


    @file_name.setter
    def file_name(self, file_name: str) -> None:
        self.__File_Name = file_name


    @property
    def saving_directory(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(
            group=self.__Config_Type,
            property_key=".".join([self.__property_key, "path"]))


    @saving_directory.setter
    def saving_directory(self, file_dir: str) -> None:
        self.__File_Save_Dir = file_dir



class ArchiverConfig(BaseArchiverConfiguration):

    __PropertiesOptUtil = None
    __Config_Type = ConfigType.ARCHIVER_GROUP.value
    __Mode = PersistenceMode.ARCHIVER

    __Archiver_Type = None
    __Archiver_Name = None
    __Archiver_Path = None

    def __init__(self, config_path: str = None):
        self.__PropertiesOptUtil = PropertiesUtil(mode=self.__Mode, config_path=config_path)
        self.__property_key = self.__PropertiesOptUtil.property_key()


    @property
    def compress_type(self) -> List[str]:
        return self.__PropertiesOptUtil.get_value_as_list(
            group=self.__Config_Type,
            property_key=".".join([self.__property_key, "type"]))


    @compress_type.setter
    def compress_type(self, compress_type: List[str]) -> None:
        self.__Archiver_Type = compress_type


    @property
    def compress_name(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(
            group=self.__Config_Type,
            property_key=".".join([self.__property_key, "name"]))


    @compress_name.setter
    def compress_name(self, compress_name: str) -> None:
        self.__Archiver_Name = compress_name


    @property
    def compress_path(self) -> str:
        return self.__PropertiesOptUtil.get_value_as_str(
            group=self.__Config_Type,
            property_key=".".join([self.__property_key, "path"]))


    @compress_path.setter
    def compress_path(self, compress_path: str) -> None:
        self.__Archiver_Path = compress_path

