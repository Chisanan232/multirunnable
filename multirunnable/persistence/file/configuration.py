from multirunnable.persistence.mode import PersistenceMode
from multirunnable.persistence.configuration import PropertiesUtil, BaseFileConfiguration, BaseArchiverConfiguration

from typing import List
from enum import Enum



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

