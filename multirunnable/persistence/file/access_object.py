from multirunnable.persistence.interface import OceanFao
from multirunnable.persistence.file.configuration import FileConfig, ArchiverConfig
from multirunnable.persistence.file.strategy import (
    OneThreadOneFile,
    AllThreadOneFile,
    OneThreadOneFileAllInArchiver,
    AllThreadOneFileInArchiver
)

from typing import List, Tuple, Iterable, Callable, Union
import os
import re



class BaseFao(OceanFao):

    """
    File Access Object (FAO).
    """

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
            checksum = False
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

    def __init__(self, config: Union[FileConfig, str]):
        if type(config) is str:
            # Check and initialize configuration by the file path.
            is_file = os.path.isfile(path=config)
            file_extension = config.split(sep=".")[-1]
            is_properties_extension = re.search(r"properties", file_extension)
            if is_file and is_properties_extension:
                self._config = config
            else:
                raise Exception("It's not a valid file path.")
        else:
            # Check and integrate the config value to use.
            if config.file_type:
                raise Exception("File type value is empty.")
            if config.file_name:
                raise Exception("File name value is empty.")
            if config.saving_directory:
                raise Exception("Directory path value is empty.")
            self._config = config


    def one_thread_one_file(self, data: Union[List, Tuple], **kwargs):
        file_end = kwargs.get("file_end", "")
        self.save(
            data=data,
            saving_function=self._one_thread_one_file,
            file_end=file_end
        )


    def _one_thread_one_file(self, data: Union[List, Tuple], **kwargs):
        file_end = kwargs.get("file_end", "")
        self.__chk_unique(file_end=file_end)
        __strategy = OneThreadOneFile(file_config=self._config)
        __strategy.save_into_file(data=data, file_end=file_end)


    def __chk_unique(self, file_end: str):
        if self.__ID_Checksum is None:
            self.__ID_Checksum = file_end
        else:
            if self.__ID_Checksum == file_end:
                raise Exception("The file end word should be unique.")
            else:
                self.__ID_Checksum = file_end


    def all_thread_one_file(self, data: Union[List, Tuple]):
        self.save(
            data=data,
            saving_function=self._all_thread_one_file
        )


    def _all_thread_one_file(self, data: Union[List, Tuple]):
        __strategy = AllThreadOneFile(file_config=self._config)
        __strategy.save_into_file(data=data)



class SimpleArchiverFao(BaseFao):

    __ID_Checksum = None

    def __init__(self, config: Union[Tuple[Union[FileConfig, ArchiverConfig]], str]):
        if type(config) is str:
            # Check and initialize configuration by the file path.
            is_file = os.path.isfile(path=config)
            file_extension = config.split(sep=".")[-1]
            is_properties_extension = re.search(r"properties", file_extension)
            if is_file and is_properties_extension:
                # self._config = config
                self._file_config = FileConfig(config_path=config)
                self._archiver_config = ArchiverConfig(config_path=config)
            else:
                raise Exception("It's not a valid file path.")
        else:
            __file_config = filter(lambda c: isinstance(c, FileConfig), config)
            __archiver_config = filter(lambda c: isinstance(c, ArchiverConfig), config)
            self._file_config: FileConfig = list(__file_config)[0]
            self._archiver_config: ArchiverConfig = list(__archiver_config)[0]
            # Check and integrate the config value to use.
            if self._file_config.file_type:
                raise Exception("File type value is empty.")
            if self._file_config.file_name:
                raise Exception("File name value is empty.")
            if self._file_config.saving_directory:
                raise Exception("Directory path value is empty.")
            if self._archiver_config.compress_type:
                raise Exception("Archiver type value is empty.")
            if self._archiver_config.compress_name:
                raise Exception("Archiver name value is empty.")
            if self._archiver_config.compress_path:
                raise Exception("Archiver path value is empty.")


    def one_thread_one_file_all_in_archiver(self, data: Union[List, Tuple], **kwargs):
        file_end = kwargs.get("file_end", "")
        self.save(
            data=data,
            saving_function=self._one_thread_one_file_all_in_archiver,
            file_end=file_end
        )


    def _one_thread_one_file_all_in_archiver(self, data: Union[List, Tuple], **kwargs):
        file_end = kwargs.get("file_end", "")
        self.__chk_unique(file_end=file_end)
        __strategy = OneThreadOneFileAllInArchiver(file_config=self._file_config, archiver_config=self._archiver_config)
        __strategy.save_and_compress(data=data, file_end=file_end)


    def __chk_unique(self, file_end: str):
        if self.__ID_Checksum is None:
            self.__ID_Checksum = file_end
        else:
            if self.__ID_Checksum == file_end:
                raise Exception("The file end word should be unique.")
            else:
                self.__ID_Checksum = file_end


    def all_thread_one_file_in_archiver(self, data: Union[List, Tuple]):
        self.save(
            data=data,
            saving_function=self._all_thread_one_file_in_archiver
        )


    def _all_thread_one_file_in_archiver(self, data: Union[List, Tuple]):
        __strategy = AllThreadOneFileInArchiver(file_config=self._file_config, archiver_config=self._archiver_config)
        __strategy.save_and_compress(data=data)

