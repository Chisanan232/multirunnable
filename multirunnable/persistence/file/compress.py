from multirunnable.persistence.file.types import CompressObject
from multirunnable.persistence.file.file import BaseDataFormatterString

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Iterable, Union, overload
from zipfile import ZipFile
import zipfile



class BaseArchiver(metaclass=ABCMeta):

    _Archiver: CompressObject = None
    _Archiver_Path = ""
    _Archiver_Mode = "a"

    @property
    def path(self) -> str:
        return self._Archiver_Path


    @path.setter
    def path(self, path: str) -> None:
        self._Archiver_Path = path


    @property
    def mode(self) -> str:
        return self._Archiver_Mode


    @mode.setter
    def mode(self, mode: str) -> None:
        self._Archiver_Mode = mode


    @abstractmethod
    def init(self) -> CompressObject:
        """
        Description:
            Initialize compress object.
        :return:
        """
        pass


    @abstractmethod
    def write(self, data: List[BaseDataFormatterString]) -> None:
        """
        Description:
            Write data into target file in archiver.
        :param data:
        :return:
        """
        pass


    @abstractmethod
    def close(self) -> None:
        """
        Description:
            Close the compress object stream.
        :return:
        """
        pass



class ZipArchiver(BaseArchiver):

    def init(self) -> None:
        self._Archiver = ZipFile(
            file=self._Archiver_Path,
            mode=self._Archiver_Mode,
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=False
        )


    def write(self, data: List[BaseDataFormatterString]) -> None:
        for __data in data:
            __file = __data.file_path
            __data_string = __data.data
            self._Archiver.writestr(
                zinfo_or_arcname=__file,
                data=__data_string
            )


    def close(self) -> None:
        self._Archiver.close()

