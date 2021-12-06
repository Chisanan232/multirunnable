from abc import ABCMeta, abstractmethod, ABC
from typing import List
from collections import namedtuple



class BaseArchiver(metaclass=ABCMeta):

    @property
    @abstractmethod
    def file_path(self) -> str:
        pass


    @file_path.setter
    @abstractmethod
    def file_path(self, path: str) -> None:
        pass


    @property
    @abstractmethod
    def mode(self) -> str:
        pass


    @mode.setter
    @abstractmethod
    def mode(self, mode: str) -> None:
        pass


    @abstractmethod
    def init(self) -> None:
        pass


    @abstractmethod
    def compress(self, data_map_list: List[namedtuple]) -> None:
        pass


    @abstractmethod
    def close(self) -> None:
        pass



class Archiver(BaseArchiver, ABC):

    _File_Path: str = ""
    _Mode: str = ""

    @property
    def file_path(self) -> str:
        return self._File_Path


    @file_path.setter
    def file_path(self, path: str) -> None:
        self._File_Path = path


    @property
    def mode(self) -> str:
        return self._Mode


    @mode.setter
    def mode(self, mode: str) -> None:
        self._Mode = mode



class ZIPArchiver(Archiver):

    __Archiver = None

    def init(self) -> None:
        from zipfile import ZipFile, ZIP_DEFLATED

        self.__Archiver = ZipFile(
            file=self.file_path,
            mode=self.mode,
            compression=ZIP_DEFLATED,
            allowZip64=False
        )


    def compress(self, data_map_list: List[namedtuple]) -> None:
        for __data in data_map_list:
            __file = __data.file_path
            __data_string = __data.data
            self.__Archiver.writestr(
                zinfo_or_arcname=__file,
                data=__data_string
            )


    def close(self) -> None:
        self.__Archiver.close()

