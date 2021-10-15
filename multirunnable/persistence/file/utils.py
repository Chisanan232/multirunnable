from multirunnable.persistence.file.file import BaseFileFormatter, BaseDataFormatterString
from multirunnable.persistence.file.compress import BaseArchiver

from typing import List, Tuple, Iterable, Callable, Union
from importlib import import_module



class FileImportUtils:

    _RootPackage = "multirunnable"
    _FormatterPackage = ".persistence.file.file"
    _CompressPackage = ".persistence.file.compress"

    _File_Formatter_Class = "FileFormatter"
    _Data_String_Class = "DataString"
    _Archiver_Class = "Archiver"

    def __init__(self):
        self.__package = None
        self.__class = None
        self.__class_instance = None


    def get_file_formatter_instance(self, file_type: str) -> BaseFileFormatter:
        __class_info = self.__get_formatter(extension=file_type) + self._File_Formatter_Class
        self.__class = self.get_class(pkg_path=self._FormatterPackage, cls_name=__class_info)
        self.__class_instance: BaseFileFormatter = self.__class()
        return self.__class_instance


    def get_data_formatter_instance(self, file_type: str) -> BaseDataFormatterString:
        __class_info = self.__get_formatter(extension=file_type) + self._Data_String_Class
        self.__class = self.get_class(pkg_path=self._FormatterPackage, cls_name=__class_info)
        self.__class_instance: BaseDataFormatterString = self.__class()
        return self.__class_instance


    def get_archiver_instance(self, archiver_type: str) -> BaseArchiver:
        __class_info = self.__get_formatter(extension=archiver_type) + self._Archiver_Class
        self.__class = self.get_class(pkg_path=self._CompressPackage, cls_name=__class_info)
        self.__class_instance: BaseArchiver = self.__class()
        return self.__class_instance


    def __get_formatter(self, extension: str) -> str:
        __class_info = extension[0].upper() + extension[1:]
        return __class_info


    def get_class(self, pkg_path: str, cls_name: str) -> Callable:
        self.__package = import_module(name=pkg_path, package=self._RootPackage)
        self.__class: Callable = getattr(self.__package, cls_name)
        return self.__class

