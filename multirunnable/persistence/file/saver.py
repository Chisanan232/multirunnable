from . import (
    SavingStrategy as _SavingStrategy,
    _Super_Worker_Saving_File_Key,
    _Sub_Worker_Saving_File_Key,
    _Activate_Compress_Key
)
from .files import BaseFile as _BaseFile
from .archivers import BaseArchiver as _BaseArchiver
from .mediator import BaseMediator as _BaseMediator

from abc import ABCMeta, abstractmethod
from typing import List, Union, Optional
from collections import namedtuple
import logging


_Done_Flag = 1
_Do_Nothing_Flag = 0
_Error_Flag = -1


class BaseSaver(metaclass=ABCMeta):

    @abstractmethod
    def register(self, mediator: _BaseMediator, strategy: _SavingStrategy) -> None:
        pass



class FileSaver(BaseSaver):

    __File: _BaseFile = None
    __Mediator: _BaseMediator = None
    __Has_Data: bool = None

    def __init__(self, file: _BaseFile):
        if not isinstance(file, _BaseFile):
            raise TypeError("Parameter *file* should be one of smoothcrawler.persistence.(CSVFormatter, XLSXFormatter, JSONFormatter).")
        self.__File = file


    def register(self, mediator: _BaseMediator, strategy: _SavingStrategy) -> None:
        self.__Mediator = mediator
        self.__Mediator.super_worker_running = strategy.value[_Super_Worker_Saving_File_Key]
        self.__Mediator.child_worker_running = strategy.value[_Sub_Worker_Saving_File_Key]
        self.__Mediator.enable_compress = strategy.value[_Activate_Compress_Key]


    def save(self, file: str, mode: str, data: List[list], encoding: str = "UTF-8"):
        if self.__Mediator is None:
            self.__saving_process(file=file, mode=mode, encoding=encoding, data=data)
        else:
            if self.__Mediator.super_worker_running is True:
                if self.__Mediator.child_worker_running is True:
                    # 'ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL' strategy.
                    if self.__Mediator.is_super_worker():
                        # This's super worker and its responsibility is compressing all files
                        # This process should not handle and run here. It's Archiver's responsibility.
                        logging.warning(f"This's main worker (thread, process, etc) so that it doesn't do anything here.")
                        self.__Has_Data = False
                        return _Do_Nothing_Flag
                    else:
                        # This's child worker and its responsibility is generating data stream with one specific file format
                        data_stream = self.__saving_stream(file=file, data=data)
                        self.__Has_Data = True
                        return data_stream
                else:
                    # 'ALL_THREADS_ONE_FILE' strategy.
                    if self.__Mediator.is_super_worker():
                        # This's super worker and its responsibility is saving data as file
                        self.__saving_process(file=file, mode=mode, encoding=encoding, data=data)
                        self.__Has_Data = False
                        return _Done_Flag
                    else:
                        # This's child worker and its responsibility is compressing all files
                        self.__Has_Data = True
                        return data
            else:
                if self.__Mediator.is_super_worker():
                    logging.warning(f"This's main worker (thread, process, etc) so that it doesn't do anything here.")
                    self.__Has_Data = False
                    return _Do_Nothing_Flag
                else:
                    # It must to be 'One Thread One File' strategy.
                    self.__saving_process(file=file, mode=mode, encoding=encoding, data=data)
                    self.__Has_Data = False
                    return _Done_Flag


    def has_data(self) -> bool:
        return self.__Has_Data


    def __saving_process(self, file: str, mode: str, encoding: str, data: List[list]):
        self.__File.file_path = file
        self.__File.mode = mode
        self.__File.encoding = encoding
        self.__File.open()
        self.__File.write(data=data)
        self.__File.close()


    def __saving_stream(self, file: str, data: List):
        data = self.__File.stream(data=data)
        DataStream = namedtuple("DataStream", ("file_path", "data"))
        DataStream.file_path = file
        DataStream.data = data
        return DataStream



class ArchiverSaver:

    __Archiver: _BaseArchiver = None
    __Mediator: _BaseMediator = None

    def __init__(self, archiver: _BaseArchiver):
        if not isinstance(archiver, _BaseArchiver):
            raise TypeError("Parameter *file* should be one of smoothcrawler.persistence.(ZIPArchiver).")
        self.__Archiver = archiver


    def register(self, mediator: _BaseMediator, strategy: _SavingStrategy) -> None:
        self.__Mediator = mediator
        self.__Mediator.super_worker_running = strategy.value[_Super_Worker_Saving_File_Key]
        self.__Mediator.child_worker_running = strategy.value[_Sub_Worker_Saving_File_Key]
        self.__Mediator.enable_compress = strategy.value[_Activate_Compress_Key]


    def compress(self, file: str, mode: str, data: List[namedtuple]) -> None:
        if self.__Mediator is None:
            self.__compress_process(file=file, mode=mode, data=data)
        else:
            if self.__Mediator.super_worker_running is True:
                if self.__Mediator.child_worker_running is True:
                    # 'ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL' strategy.
                    if self.__Mediator.is_super_worker():
                        # This's super worker and its responsibility is compressing all files
                        # This process should not handle and run here. It's Archiver's responsibility.
                        self.__compress_process(file=file, mode=mode, data=data)


    def __compress_process(self, file: str, mode: str, data: List):
        self.__Archiver.file_path = file
        self.__Archiver.mode = mode
        self.__Archiver.init()
        self.__Archiver.compress(data_map_list=data)
        self.__Archiver.close()


