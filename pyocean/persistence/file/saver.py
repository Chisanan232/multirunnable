from pyocean.persistence.interface import OceanPersistence
from pyocean.persistence.file.formatter import BaseFileFormatter
from pyocean.persistence.file.exceptions import FilePathCannotBeEmpty, ClassNotInstanceOfBaseFileFormatter, NotSupportHandlingFileType

from abc import ABCMeta, abstractmethod
from typing import List, Callable, Iterable, Union
import re



class BaseFileSaver(OceanPersistence):

    _File_Formatter: BaseFileFormatter = None
    __File_Formatter_Supper: List[str] = ["json", "csv", "xlsx"]

    __File_Path: str = ""
    __File_Opening_Mode: str = "a+"
    __File_Encoding: str = "UTF-8"

    def __init__(self, file_path: str, file_format: BaseFileFormatter):
        if len(file_path) != 0:
            self.__chk_file_is_valid(file_path)
        else:
            raise FilePathCannotBeEmpty

        if isinstance(file_format, BaseFileFormatter):
            self._File_Formatter = file_format
        else:
            raise ClassNotInstanceOfBaseFileFormatter


    def __chk_file_is_valid(self, file_path: str) -> None:
        file_type = self.__get_file_type(file_path)
        if self.__file_type_is_valid(file_type):
            self.__File_Path = file_path
        else:
            raise NotSupportHandlingFileType


    def __get_file_type(self, file_path: str) -> str:
        return str(file_path).split(".")[-1]


    def __file_type_is_valid(self, file_type: str) -> bool:
        for file_format in self.__File_Formatter_Supper:
            if re.search(re.escape(file_format), file_type) is not None:
                return True
        else:
            return False


    @property
    def file_path(self) -> str:
        return self.__File_Path


    @file_path.setter
    def file_path(self, path: str) -> None:
        self.__File_Path = path


    @property
    def file_open_mode(self) -> str:
        return self.__File_Opening_Mode


    @file_open_mode.setter
    def file_open_mode(self, mode: str) -> None:
        self.__File_Opening_Mode = mode


    @property
    def file_encoding(self) -> str:
        return self.__File_Encoding


    @file_encoding.setter
    def file_encoding(self, encoding: str) -> None:
        self.__File_Encoding = encoding


    @abstractmethod
    def save(self, data: list) -> None:
        pass



class SingleFileSaver(BaseFileSaver):

    def save(self, data: list) -> None:
        self._File_Formatter.open(file_path=self.__File_Path, open_mode=self.__File_Opening_Mode, encoding=self.__File_Encoding)
        fin_data = self._File_Formatter.data_handling(data=data)
        self._File_Formatter.write(data=fin_data)
        self._File_Formatter.done()



class MultiFileSaver(BaseFileSaver):

    def save(self, data: list) -> None:
        """
        Note:
            1. All processes or threads save data to their file.
            2. Express the data into a file like zip, tar, etc. in Main thread.
        :param data:
        :return:
        """
        pass


    def compress(self) -> None:
        pass
