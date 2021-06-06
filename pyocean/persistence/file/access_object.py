from pyocean.persistence.interface import OceanFao
from pyocean.persistence.mode import PersistenceMode
from pyocean.persistence.file.saver import BaseFileSaver
from pyocean.persistence.file.formatter import BaseFileFormatter
from pyocean.persistence.file.configuration import FileConfig
from pyocean.persistence.file.exceptions import PersistenceModeIsInvalid

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Tuple, Iterable, Union
import logging



class BaseFao(OceanFao):

    def __init__(self):
        self._file_name = FileConfig.file_name
        self._file_type = FileConfig.file_type
        self._dir = FileConfig.saving_directory


    def save(self, data: Union[List, Tuple]):
        checksum = None
        error = None
        try:
            data = self.data_handling(data=data)
            self.data_saving(data=data)
        except Exception as e:
            error = e
        else:
            checksum = True
        finally:
            return checksum, error


    @abstractmethod
    def data_handling(self, data: Union[List, Tuple]) -> Union[List, Tuple]:
        pass


    @abstractmethod
    def data_saving(self, data: Union[List, Tuple]) -> None:
        pass


    def save_data_as_json(self, file_path: str, data: Union[List, Tuple]):
        __saver = SingleFileSaver(file_path=file_path, file_format=JSONFormatter())
        if isinstance(data, List):
            __saver.save(data=data)
        else:
            logging.warning("The data structure is not perfectly mapping.")
            __saver.save(data=data)


    def save_data_as_csv(self, data: Union[List[Union[List, Tuple]], Tuple[Union[List, Tuple]]]):
        __saver = SingleFileSaver(file_path=cls.__CSV_File_Path, file_format=CSVFormatter())
        if isinstance(data, List):
            __saver.save(data=data)
        else:
            logging.warning("The data structure is not perfectly mapping.")
            __saver.save(data=data)


    def save_data_as_excel(self, data: Union[List[Union[List, Tuple]], Tuple[Union[List, Tuple]]]):
        __saver = SingleFileSaver(file_path=cls.__Excel_File_Path, file_format=ExcelFormatter())
        if isinstance(data, List):
            __saver.save(data=data)
        else:
            logging.warning("The data structure is not perfectly mapping.")
            __saver.save(data=data)



class SingleFao(BaseFao):
    pass



class MultiFao(BaseFao):
    pass

