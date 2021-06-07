from pyocean.persistence.interface import OceanFao
from pyocean.persistence.mode import PersistenceMode
from pyocean.persistence.file.configuration import FileConfig
from pyocean.persistence.file.saver import SingleFileSaver
from pyocean.persistence.file.formatter import BaseFileFormatter
from pyocean.persistence.file.exceptions import PersistenceModeIsInvalid

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Tuple, Iterable, Union
import logging



class BaseFao(OceanFao):

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

    @property
    def file_path(self) -> str:
        return self._dir + self._file_name + self._file_type


    def data_saving(self, data: Union[List, Tuple],  formatter: BaseFileFormatter) -> None:
        __saver = SingleFileSaver(file_path=self.file_path, file_format=formatter)
        if isinstance(data, List):
            __saver.save(data=data)
        else:
            logging.warning("The data structure is not perfectly mapping.")
            __saver.save(data=data)



class MultiFao(BaseFao):

    @property
    def file_path(self) -> str:
        # Need to check the zip directory and file  path.
        pass


    @property
    @abstractmethod
    def compression_path(self) -> str:
        pass


    @abstractmethod
    def compress_process(self) -> None:
        pass

