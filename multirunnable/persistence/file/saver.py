from multirunnable.persistence.interface import OceanPersistence
from multirunnable.persistence.file.file import BaseFileFormatter, BaseDataFormatterString
from multirunnable.persistence.file.compress import BaseArchiver
from multirunnable.persistence.file.utils import FileImportUtils
from multirunnable.persistence.file.exceptions import FilePathCannotBeEmpty, ClassNotInstanceOfBaseFileFormatter, NotSupportHandlingFileType

from abc import ABCMeta, abstractmethod
from typing import List, Callable, Iterable, Union
import re



class BaseFileSaver(OceanPersistence):

    _File_Formatter: BaseFileFormatter = None
    __File_Formatter_Supper: List[str] = ["json", "csv", "xlsx"]

    _File_Path: str = ""
    _File_Opening_Mode: str = "a+"
    _File_Encoding: str = "UTF-8"

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
            self._File_Path = file_path
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
        return self._File_Path


    @file_path.setter
    def file_path(self, path: str) -> None:
        self._File_Path = path


    @property
    def file_open_mode(self) -> str:
        return self._File_Opening_Mode


    @file_open_mode.setter
    def file_open_mode(self, mode: str) -> None:
        self._File_Opening_Mode = mode


    @property
    def file_encoding(self) -> str:
        return self._File_Encoding


    @file_encoding.setter
    def file_encoding(self, encoding: str) -> None:
        self._File_Encoding = encoding


    @abstractmethod
    def save(self, data: list) -> None:
        pass



class SingleFileSaver(BaseFileSaver):

    def save(self, data: list) -> None:
        self._File_Formatter.open(file_path=self._File_Path, open_mode=self._File_Opening_Mode, encoding=self._File_Encoding)
        fin_data = self._File_Formatter.data_handling(data=data)
        self._File_Formatter.write(data=fin_data)
        self._File_Formatter.done()



class BaseArchiverSaver(metaclass=ABCMeta):

    def __init__(self, archiver: BaseArchiver):
        self._archiver = archiver


    def save(self, file_path: List[str], data: List):
        data_string = self.data_handling(file_path=file_path, data=data)
        self.compress(data=data_string)


    @abstractmethod
    def data_handling(self, file_path: List[str], data: List) -> List[BaseDataFormatterString]:
        pass


    @abstractmethod
    def compress(self, data: List[BaseDataFormatterString]) -> None:
        """
        Description:
            Compress file(s) which saving target data with specific file format.
        :param data:
        :return:
        """
        pass



class ArchiverSaver(BaseArchiverSaver):

    def data_handling(self, file_path: List[str], data: List) -> List[BaseDataFormatterString]:
        _util = FileImportUtils()
        __data_string = []

        for __file_path in file_path:
            __file_type = __file_path.split(sep=".")[-1]
            data_formatter: BaseDataFormatterString = _util.get_data_formatter_instance(file_type=__file_type)
            data_formatter.file_path = __file_path
            data_formatter.data_string(data=data)
            __data_string.append(data_formatter)

        return __data_string


    def compress(self, data: List[BaseDataFormatterString]) -> None:
        self._archiver.init()
        self._archiver.write(data=data)
        self._archiver.close()

