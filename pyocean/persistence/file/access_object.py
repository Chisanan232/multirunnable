from pyocean.persistence.interface import OceanFao
from pyocean.persistence.mode import PersistenceMode
from pyocean.persistence.file.configuration import SupportConfig, FileConfig, ArchiverConfig
from pyocean.persistence.file.saver import SingleFileSaver, MultiFileSaver, ArchiverSaver
from pyocean.persistence.file.formatter import BaseFileFormatter, BaseDataFormatterString
from pyocean.persistence.file.compress import BaseArchiver
from pyocean.persistence.file.exceptions import PersistenceModeIsInvalid

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Tuple, Iterable, Callable, Union
import logging
import os



class BaseFao(OceanFao):

    """
    File Access Object (FAO).
    """

    def __init__(self):
        self._file_name = FileConfig.file_name
        self._file_type = FileConfig.file_type
        self._dir = FileConfig.saving_directory


    @property
    @abstractmethod
    def file_path(self) -> str:
        pass


    def save(self, data: Union[List, Tuple],  formatter: BaseFileFormatter):
        checksum = None
        error = None
        try:
            data = self.data_handling(data=data)
            self.data_saving(data=data, formatter=formatter)
        except Exception as e:
            error = e
        else:
            checksum = True
        finally:
            return checksum, error


    def data_handling(self, data: Union[List, Tuple]) -> Union[List, Tuple]:
        return data


    @abstractmethod
    def data_saving(self, data: Union[List, Tuple],  formatter: BaseFileFormatter) -> None:
        pass


    def data_saving_with_mode(self, mode: PersistenceMode) -> None:
        if mode is PersistenceMode.SINGLE_FILE_IO:
            pass
        elif mode is PersistenceMode.MULTI_FILE_IO:
            pass
        else:
            raise PersistenceModeIsInvalid



class SingleFao(BaseFao):

    """
    Single files saving strategy:
    Saving final data which has been integrated and handled to
    file(s) in Main Thread.
    """

    @property
    def file_path(self) -> List[str]:
        file_types = self._file_type.split(sep=",")
        return [os.path.join(self._dir, f"{self._file_name}.{__file_type}") for __file_type in file_types]


    def data_saving(self, data: Union[List, Tuple],  formatter: BaseFileFormatter) -> None:
        __saver = SingleFileSaver(file_path=self.file_path, file_format=formatter)
        if isinstance(data, List):
            __saver.save(data=data)
        else:
            logging.warning("The data structure is not perfectly mapping.")
            __saver.save(data=data)



class MultiFao(BaseFao):

    """
    Multiple files saving strategy:
    Saving file(s) in each workers and compress all file(s) in Main Thread.
    """

    def __init__(self):
        super().__init__()
        self.__archiver_type = ArchiverConfig.compress_type
        self.__archiver_name = ArchiverConfig.compress_name
        self.__archiver_path = ArchiverConfig.compress_path


    @property
    def file_path(self) -> List[str]:
        file_types = self._file_type.split(sep=",")
        return [f"{self._file_name}.{__file_type}" for __file_type in file_types]


    @property
    def archiver_path(self) -> str:
        archiver_file_name = f"{self.__archiver_name}.{self.__archiver_type}"
        __path = os.path.join(self.__archiver_path, archiver_file_name)
        return __path


    @abstractmethod
    def compress_process(self) -> None:
        pass

