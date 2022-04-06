from .archivers import BaseArchiver as _BaseArchiver
from .mediator import BaseMediator as _BaseMediator
from .files import BaseFile as _BaseFile
from . import (
    SavingStrategy as _SavingStrategy,
    _Super_Worker_Saving_File_Key,
    _Sub_Worker_Saving_File_Key,
    _Activate_Compress_Key
)
from ...parallel.strategy import Global_Manager

from collections import namedtuple
from typing import List, Union
from abc import ABCMeta, abstractmethod
import logging


_Done_Flag = 1
_Do_Nothing_Flag = 0
_Error_Flag = -1

_Run_Children_History_Flag: dict = Global_Manager.dict({"history": False})


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
            self._saving_process(file=file, mode=mode, encoding=encoding, data=data)
            return _Done_Flag
        else:
            if self.__Mediator.super_worker_running is True:
                if self.__Mediator.child_worker_running:
                    return self._one_worker_one_file_and_compress_all_process(file=file, data=data)
                else:
                    return self._all_workers_one_file_process(file=file, mode=mode, encoding=encoding, data=data)
            else:
                return self._one_worker_one_file_process(file=file, mode=mode, encoding=encoding, data=data)


    def _one_worker_one_file_process(self, file: str, mode: str, encoding: str, data: List) -> int:
        if self._is_children_worker():
            global _Run_Children_History_Flag
            _Run_Children_History_Flag["history"] = True
            # It must to be 'One Thread One File' strategy.
            self._saving_process(file=file, mode=mode, encoding=encoding, data=data)
            self.__Has_Data = False
            return _Done_Flag
        elif self._is_main_worker():
            if self._has_run_children_before():
                logging.warning("This's main worker (thread, process, etc) so that it doesn't do anything here.")
                self.__Has_Data = False
                return _Do_Nothing_Flag
            else:
                self._saving_process(file=file, mode=mode, encoding=encoding, data=data)
                self.__Has_Data = False
                return _Done_Flag
        else:
            raise RuntimeError


    def _all_workers_one_file_process(self, file: str, mode: str, encoding: str, data: List) -> Union[int, list]:
        # 'ALL_THREADS_ONE_FILE' strategy.
        if self._is_children_worker():
            global _Run_Children_History_Flag
            _Run_Children_History_Flag["history"] = True
            # This's child worker and its responsibility is compressing all files
            self.__Has_Data = True
            return data
        elif self._is_main_worker():
            # This's super worker and its responsibility is saving data as file
            self._saving_process(file=file, mode=mode, encoding=encoding, data=data)
            self.__Has_Data = False
            return _Done_Flag
        else:
            raise RuntimeError


    def _one_worker_one_file_and_compress_all_process(self, file: str, data: List):
        # 'ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL' strategy.
        if self._is_children_worker():
            global _Run_Children_History_Flag
            _Run_Children_History_Flag["history"] = True
            # This's child worker and its responsibility is generating data stream with one specific file format
            data_stream = self._saving_stream(file=file, data=data)
            self.__Has_Data = True
            return data_stream
        elif self._is_main_worker():
            if self._has_run_children_before():
                # This's super worker and its responsibility is compressing all files
                # This process should not handle and run here. It's Archiver's responsibility.
                logging.warning("This's main worker (thread, process, etc) so that it doesn't do anything here.")
                self.__Has_Data = False
                return _Do_Nothing_Flag
            else:
                # This's child worker and its responsibility is generating data stream with one specific file format
                data_stream = self._saving_stream(file=file, data=data)
                self.__Has_Data = True
                return data_stream
        else:
            raise RuntimeError


    def has_data(self) -> bool:
        return self.__Has_Data


    def _has_run_children_before(self) -> bool:
        return _Run_Children_History_Flag["history"] is True


    def _is_main_worker(self) -> bool:
        return self.__Mediator.is_super_worker() is True


    def _is_children_worker(self) -> bool:
        return self.__Mediator.is_super_worker() is not True


    def _saving_process(self, file: str, mode: str, encoding: str, data: List[list]) -> None:
        self.__File.file_path = file
        self.__File.mode = mode
        self.__File.encoding = encoding
        self.__File.open()
        self.__File.write(data=data)
        self.__File.close()


    def _saving_stream(self, file: str, data: List):
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
            self._compress_process(file=file, mode=mode, data=data)
        else:
            if self.__Mediator.super_worker_running is True:
                if self.__Mediator.child_worker_running is True:
                    # 'ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL' strategy.
                    if self.__Mediator.is_super_worker():
                        # This's super worker and its responsibility is compressing all files
                        # This process should not handle and run here. It's Archiver's responsibility.
                        self._compress_process(file=file, mode=mode, data=data)


    def _compress_process(self, file: str, mode: str, data: List):
        self.__Archiver.file_path = file
        self.__Archiver.mode = mode
        self.__Archiver.init()
        self.__Archiver.compress(data_map_list=data)
        self.__Archiver.close()


