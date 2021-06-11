from pyocean.persistence.file.types import CompressObject
from pyocean.persistence.file.file import BaseDataFormatterString
from pyocean.persistence.file.configuration import ArchiverConfig

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Iterable, Union, overload
from zipfile import ZipFile
import zipfile



class BaseArchiver(metaclass=ABCMeta):

    _Archiver: CompressObject = None
    _Archiver_Path = ""
    _Archiver_Mode = "a"

    def __init__(self, path: str):
        self._Archiver_Path = path


    @property
    def mode(self):
        return self._Archiver_Mode


    @mode.setter
    def mode(self, mode: str):
        self._Archiver_Mode = mode


    @abstractmethod
    def init(self) -> CompressObject:
        """
        Description:
            Initialize compress object.
        :return:
        """
        pass


    @overload
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
    def write(self, data: BaseDataFormatterString) -> None:
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


    @overload
    def write(self, data: List[BaseDataFormatterString]) -> None:
        for __data in data:
            self.write(data=__data)


    def write(self, data: BaseDataFormatterString) -> None:
        self._Archiver.writestr(zinfo_or_arcname=data.file_path, data=data.data)


    def close(self) -> None:
        self._Archiver.close()

