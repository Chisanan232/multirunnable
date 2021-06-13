from pyocean.persistence.file.configuration import SupportConfig, FileConfig, ArchiverConfig
from pyocean.persistence.file.saver import SingleFileSaver, ArchiverSaver
from pyocean.persistence.file.file import BaseFileFormatter, BaseDataFormatterString
from pyocean.persistence.file.compress import BaseArchiver

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Tuple, Iterable, Callable, Union
import logging
import os



class BaseFaoStrategy(metaclass=ABCMeta):

    """
    The persistence-file strategy:

    1.
        1-1. Multiple workers save their data as specific format.
        1-2. Compress all files into an archiver in main thread.

    2.
        2-1. Multiple workers return data back to main thread.
        2-2. Save data as specific file format and compress it into an archiver in main thread.

    Above strategies, compress process isn't necessary.
    """

    def __init__(self, file_config: Union[FileConfig, str] = None):
        if file_config is None:
            self._file_name = FileConfig.file_name
            self._file_type = FileConfig.file_type
            self._dir = FileConfig.saving_directory
        else:
            # Do something configure setting (new feature)
            if type(file_config) is str:
                __config = FileConfig(config_path=file_config)
            else:
                __config = file_config
            self._file_name = __config.file_name
            self._file_type = __config.file_type
            self._dir = __config.saving_directory


    @abstractmethod
    def file_path(self, **kwargs) -> List[str]:
        pass



class BaseFaoWithFileStrategy(BaseFaoStrategy):

    @abstractmethod
    def save_into_file(self, data: List,  formatter: Union[BaseFileFormatter, BaseDataFormatterString], **kwargs) -> None:
        pass



class BaseFaoWithArchiverStrategy(BaseFaoStrategy):

    def __init__(self, file_config: Union[FileConfig, str] = None,
                 archiver_config: Union[ArchiverConfig, str] = None):
        super().__init__(file_config=file_config)
        if archiver_config is None:
            self._archiver_type = ArchiverConfig.compress_type
            self._archiver_name = ArchiverConfig.compress_name
            self._archiver_path = ArchiverConfig.compress_path
        else:
            # Do something configure setting (new feature)
            if type(archiver_config) is str:
                __config = ArchiverConfig(config_path=archiver_config)
            else:
                __config = archiver_config
            self._archiver_type = __config.compress_type
            self._archiver_name = __config.compress_name
            self._archiver_path = __config.compress_path


    @abstractmethod
    def archiver_path(self) -> str:
        pass


    @abstractmethod
    def save_and_compress(self, archiver: BaseArchiver, data: List, **kwargs):
        pass



class OneThreadOneFile(BaseFaoWithFileStrategy):

    def file_path(self, **kwargs) -> List[str]:
        file_end = kwargs.get("file_end", "")
        # file_types = self._file_type.split(sep=",")
        return [os.path.join(self._dir, f"{self._file_name}_{file_end}.{__file_type}")
                for __file_type in self._file_type]


    def save_into_file(self, data: Union[List, Tuple],  formatter: BaseFileFormatter, **kwargs) -> None:
        file_end = kwargs.get("file_end", "")
        for __file_path in self.file_path(file_end=file_end):
            __saver = SingleFileSaver(file_path=f"{__file_path}", file_format=formatter)
            if isinstance(data, List):
                __saver.save(data=data)
            else:
                logging.warning("The data structure is not perfectly mapping.")
                raise TypeError("")



class AllThreadOneFile(BaseFaoWithFileStrategy):

    def file_path(self) -> List[str]:
        # file_types = self._file_type.split(sep=",")
        return [os.path.join(self._dir, f"{self._file_name}.{__file_type}") for __file_type in self._file_type]


    def save_into_file(self, data: List,  formatter: BaseFileFormatter, **kwargs) -> None:
        for __file_path in self.file_path():
            __saver = SingleFileSaver(file_path=__file_path, file_format=formatter)
            if isinstance(data, List):
                __saver.save(data=data)
            else:
                logging.warning("The data structure is not perfectly mapping.")
                raise TypeError("")



class OneThreadOneFileAllInArchiver(BaseFaoWithArchiverStrategy):

    __File_Strategy = OneThreadOneFile()

    def file_path(self, **kwargs) -> List[str]:
        file_end = kwargs.get("file_end", "")
        # file_types = self._file_type.split(sep=",")
        return [f"{self._file_name}_{file_end}.{__file_type}" for __file_type in self._file_type]


    def archiver_path(self) -> str:
        archiver_file_name = f"{self._archiver_name}.{self._archiver_type}"
        __path = os.path.join(self._archiver_path, archiver_file_name)
        return __path


    def save_and_compress(self, archiver: BaseArchiver, data: List, **kwargs):
        file_end = kwargs.get("file_end", "")
        archiver.path = self.archiver_path()
        __archiver = ArchiverSaver(archiver=archiver)
        __archiver.save(file_path=self.file_path(file_end=file_end), data=data)



class AllThreadOneFileInArchiver(BaseFaoWithArchiverStrategy):

    __File_Strategy = AllThreadOneFile()

    def file_path(self) -> List[str]:
        # file_types = self._file_type.split(sep=",")
        return [f"{self._file_name}.{__file_type}" for __file_type in self._file_type]


    def archiver_path(self) -> str:
        archiver_file_name = f"{self._archiver_name}.{self._archiver_type}"
        __path = os.path.join(self._archiver_path, archiver_file_name)
        return __path


    def save_and_compress(self, archiver: BaseArchiver, data: List, **kwargs):
        archiver.path = self.archiver_path()
        __archiver = ArchiverSaver(archiver=archiver)
        __archiver.save(file_path=self.file_path(), data=data)
