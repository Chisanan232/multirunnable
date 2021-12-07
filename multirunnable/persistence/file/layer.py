from multirunnable.persistence.interface import DataPersistenceLayer
from . import SavingStrategy
from .mediator import BaseMediator, SavingMediator
from .saver import FileSaver, ArchiverSaver
from .files import BaseFile, CSVFormatter, XLSXFormatter, JSONFormatter
from .archivers import BaseArchiver, ZIPArchiver

from abc import ABC
from typing import List



class FileAccessObject(DataPersistenceLayer, ABC):

    def __init__(self, **kwargs):
        super(FileAccessObject, self).__init__(**kwargs)



class BaseFao(FileAccessObject):

    def __init__(self, strategy: SavingStrategy, **kwargs):
        super().__init__(**kwargs)
        self.__mediator = SavingMediator()
        self.__strategy = strategy


    def save_as_json(self, file: str, mode: str, data: List[list]):
        result = BaseFao._save(
            fileformat=JSONFormatter(),
            mediator=self.__mediator,
            strategy=self.__strategy,
            file=file, mode=mode, data=data)
        return result


    def save_as_csv(self, file: str, mode: str, data: List[list]):
        result = BaseFao._save(
            fileformat=CSVFormatter(),
            mediator=self.__mediator,
            strategy=self.__strategy,
            file=file, mode=mode, data=data)
        return result


    def save_as_excel(self, file: str, mode: str, data: List[list]):
        result = BaseFao._save(
            fileformat=XLSXFormatter(),
            mediator=self.__mediator,
            strategy=self.__strategy,
            file=file, mode=mode, data=data)
        return result


    @staticmethod
    def _save(fileformat: BaseFile, mediator: BaseMediator, strategy: SavingStrategy, file: str, mode: str, data: List[list]):
        file_saver = FileSaver(file=fileformat)
        file_saver.register(mediator=mediator, strategy=strategy)
        result = file_saver.save(file=file, mode=mode, data=data)
        return result


    def compress_as_zip(self, file: str, mode: str, data: List):
        if self.__strategy is not SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL:
            raise ValueError("The compress process only work with strategy 'ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL'.")

        BaseFao._compress(
            archiverformat=ZIPArchiver(),
            mediator=self.__mediator,
            strategy=self.__strategy,
            file=file, mode=mode, data=data)


    @staticmethod
    def _compress(archiverformat: BaseArchiver, mediator: BaseMediator, strategy: SavingStrategy, file: str, mode: str, data: List[list]) -> None:
        archiver_saver = ArchiverSaver(archiver=archiverformat)
        archiver_saver.register(mediator=mediator, strategy=strategy)
        archiver_saver.compress(file=file, mode=mode, data=data)

