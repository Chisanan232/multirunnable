from pyocean.persistence.interface import OceanFao
from pyocean.persistence.file.file import BaseFileFormatter, BaseDataFormatterString
from pyocean.persistence.file.compress import BaseArchiver, ZipArchiver
from pyocean.persistence.file.strategy import (
    OneThreadOneFile,
    AllThreadOneFile,
    OneThreadOneFileAllInArchiver,
    AllThreadOneFileInArchiver
)

from typing import List, Tuple, Iterable, Callable, Union



class BaseFao(OceanFao):

    """
    File Access Object (FAO).
    """

    def __init__(self, config=None):
        if config is None:
            # Get data from properties file
            self._config = config
        else:
            # Check and integrate the config value to use.
            self._config = config


    def save(self, data: Union[List, Tuple],  saving_function: Callable, *args, **kwargs):
        checksum = None
        error = None
        try:
            data = self.data_handling(data=data)
            kwargs["data"] = data
            saving_function(*args, **kwargs)
        except Exception as e:
            self.exception_handling(error=e)
            error = e
        else:
            checksum = True
        finally:
            return checksum, error


    def data_handling(self, data: Union[List, Tuple]) -> Union[List, Tuple]:
        return data


    def exception_handling(self, error: Exception) -> None:
        pass



class SimpleFileFao(BaseFao):

    """
    Single files saving strategy:
    Saving final data which has been integrated and handled to
    file(s) in Main Thread.
    """

    __ID_Checksum = None

    def one_thread_one_file(self, data: Union[List, Tuple],  formatter: BaseFileFormatter, **kwargs):
        file_end = kwargs.get("file_end", "")
        self.save(
            data=data,
            saving_function=self.__one_thread_one_file,
            formatter=formatter,
            file_end=file_end
        )


    def __one_thread_one_file(self, data: Union[List, Tuple],  formatter: BaseFileFormatter, **kwargs):
        file_end = kwargs.get("file_end", "")
        self.__chk_unique(file_end=file_end)
        __strategy = OneThreadOneFile(config=self._config)
        __strategy.save_into_file(data=data, formatter=formatter, file_end=file_end)


    def __chk_unique(self, file_end: str):
        if self.__ID_Checksum is None:
            self.__ID_Checksum = file_end
        else:
            if self.__ID_Checksum == file_end:
                raise Exception("The file end word should be unique.")
            else:
                self.__ID_Checksum = file_end


    def all_thread_one_file(self, data: Union[List, Tuple],  formatter: BaseFileFormatter):
        self.save(
            data=data,
            saving_function=self.__all_thread_one_file,
            formatter=formatter
        )


    def __all_thread_one_file(self, data: Union[List, Tuple],  formatter: BaseFileFormatter):
        __strategy = AllThreadOneFile(config=self._config)
        __strategy.save_into_file(data=data, formatter=formatter)



class SimpleArchiverFao(BaseFao):

    __ID_Checksum = None

    def one_thread_one_file_all_in_archiver(self, data: Union[List, Tuple], archiver: BaseArchiver, **kwargs):
        file_end = kwargs.get("file_end", "")
        self.save(
            data=data,
            saving_function=self.__one_thread_one_file_all_in_archiver,
            archiver=archiver,
            file_end=file_end
        )


    def __one_thread_one_file_all_in_archiver(self, data: Union[List, Tuple], archiver: BaseArchiver, **kwargs):
        file_end = kwargs.get("file_end", "")
        self.__chk_unique(file_end=file_end)
        __strategy = OneThreadOneFileAllInArchiver(config=self._config)
        __strategy.save_and_compress(archiver=archiver, data=data, file_end=file_end)


    def __chk_unique(self, file_end: str):
        if self.__ID_Checksum is None:
            self.__ID_Checksum = file_end
        else:
            if self.__ID_Checksum == file_end:
                raise Exception("The file end word should be unique.")
            else:
                self.__ID_Checksum = file_end


    def all_thread_one_file_in_archiver(self, data: Union[List, Tuple], archiver: BaseArchiver):
        self.save(
            data=data,
            saving_function=self.__all_thread_one_file_in_archiver,
            archiver=archiver
        )


    def __all_thread_one_file_in_archiver(self, data: Union[List, Tuple], archiver: BaseArchiver):
        __strategy = AllThreadOneFileInArchiver(config=self._config)
        __strategy.save_and_compress(archiver=archiver, data=data)

