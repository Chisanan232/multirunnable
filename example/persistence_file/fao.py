from pyocean.persistence.file import SimpleFileFao, SimpleArchiverFao

from typing import Iterable, List, Union, Tuple



class ExampleFao:

    __Config_Path = "The .properties configuration file path."

    def __init__(self):
        self.__file_fao = SimpleFileFao(config=self.__Config_Path)
        self.__archiver_fao = SimpleArchiverFao(config=self.__Config_Path)


    def one_thread_one_file(self, data: List, file_end: str):
        self.__file_fao.one_thread_one_file(
            data=data,
            file_end=file_end
        )


    def all_thread_one_file(self, data: List):
        self.__file_fao.all_thread_one_file(
            data=data
        )


    def one_thread_one_file_all_in_archiver(self, data: List, file_end: str):
        self.__archiver_fao.one_thread_one_file_all_in_archiver(
            archiver=self.__archiver,
            data=data,
            file_end=file_end
        )


    def all_thread_one_file_in_archiver(self, data: List):
        self.__archiver_fao.all_thread_one_file_in_archiver(data=data)

