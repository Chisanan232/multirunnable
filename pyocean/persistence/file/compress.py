from pyocean.persistence.file.types import CompressObject
from pyocean.persistence.file.formatter import BaseFileStream
from pyocean.persistence.file.configuration import FileConfig

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Iterable, Union, overload
from zipfile import ZipFile
import zipfile



class BaseArchiver(metaclass=ABCMeta):

    _Archiver: CompressObject = None
    _Archiver_Path = ""
    _Archiver_Mode = "a"


    def __init__(self):
        self._Archiver_Path = FileConfig.file_name


    @property
    def mode(self):
        return self._Archiver_Mode


    @mode.setter
    def mode(self, mode: str):
        self._Archiver_Mode = mode


    def compress(self, file: Union[BaseFileStream, List[BaseFileStream]]):
        """
        Description:
            Compress file(s) which saving target data with specific file format.
        :param file:
        :return:
        """
        self._Archiver = self.init()
        self.write(file=file)
        self.close()


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
    def write(self, files: List[BaseFileStream]) -> None:
        """
        Description:
            Write data into target file in archiver.
        :param files:
        :return:
        """
        pass


    @abstractmethod
    def write(self, file: BaseFileStream) -> None:
        """
        Description:
            Write data into target file in archiver.
        :param file:
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

    def init(self) -> CompressObject:
        return ZipFile(
            file=self._Archiver_Path,
            mode=self._Archiver_Mode,
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=False
        )


    @overload
    def write(self, files: List[BaseFileStream]) -> None:
        for __file in files:
            self.write(file=__file)


    def write(self, file: BaseFileStream) -> None:
        self._Archiver.writestr(zinfo_or_arcname=file.file_path, data=file.data)


    def close(self) -> None:
        self._Archiver.close()

