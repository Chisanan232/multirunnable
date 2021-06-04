from abc import ABCMeta, abstractmethod
from typing import List
from openpyxl import Workbook
import json
import csv



class BaseFileFormatter(metaclass=ABCMeta):

    _File_IO_Wrapper: object = None


    @abstractmethod
    def open(self, file_path: str, open_mode: str, encoding: str) -> None:
        pass


    @abstractmethod
    def data_handling(self, data: list) -> list:
        pass


    @abstractmethod
    def write(self, data: list) -> None:
        pass


    @abstractmethod
    def done(self) -> None:
        pass



class CSVFormatter(BaseFileFormatter):

    def open(self, file_path: str, open_mode: str, encoding: str) -> None:
        self._File_IO_Wrapper = open(file=file_path, mode=open_mode, newline='', encoding=encoding)


    def data_handling(self, data: List[list]) -> list:
        csv_data: List[list] = []
        for i, d in enumerate(data):
            # self.__save_headers(index=i, data_list=csv_data, data_content=d)
            self.__save_data_content(data_list=csv_data, data_content=d)
        return csv_data


    def __save_headers(self, index: int, data_list: List[list], data_content: dict) -> None:
        if self.__is_headers(index):
            data_list.append(list(data_content.keys()))


    def __is_headers(self, index: int) -> bool:
        return index == 0


    def __save_data_content(self, data_list: List[list], data_content: List) -> None:
        data_list.append(data_content)


    def write(self, data: list) -> None:
        csv_obj = csv.writer(self._File_IO_Wrapper)
        for data_line in data:
            csv_obj.writerow(data_line)


    def done(self) -> None:
        self._File_IO_Wrapper.close()



class ExcelFormatter(BaseFileFormatter):

    # __Work_Book = None
    __Work_Sheet_Page = None

    __Excel_File_Path = ""
    __Sheet_Page_Name = "Data"

    def set_sheet_name(self, name: str) -> None:
        self.__Sheet_Page_Name = name


    def open(self, file_path: str, open_mode: str, encoding: str) -> None:
        self.__Excel_File_Path = file_path
        self._File_IO_Wrapper: Workbook = Workbook()
        self.__Work_Sheet_Page = self._File_IO_Wrapper.create_sheet(index=0, title=self.__Sheet_Page_Name)


    def data_handling(self, data: list) -> list:
        excel_data: List[list] = []
        for i, d in enumerate(data):
            # self.__save_headers(index=i, data_list=excel_data, data_content=d)
            self.__save_data_content(data_list=excel_data, data_content=d)
        return excel_data


    def __save_headers(self, index: int, data_list: List[list], data_content: dict) -> None:
        if self.__is_headers(index):
            data_list.append(list(data_content.keys()))


    def __is_headers(self, index: int) -> bool:
        return index == 0


    def __save_data_content(self, data_list: List[list], data_content: List) -> None:
        data_list.append(data_content)


    def write(self, data: list) -> None:
        for d in data:
            self.__Work_Sheet_Page.append(d)


    def done(self) -> None:
        self._File_IO_Wrapper.save(self.__Excel_File_Path)



class JSONFormatter(BaseFileFormatter):

    def open(self, file_path: str, open_mode: str, encoding: str) -> None:
        self._File_IO_Wrapper = open(file=file_path, mode=open_mode, encoding=encoding)


    def data_handling(self, data: list) -> list:
        json_data = json.dumps(data, ensure_ascii=False)
        return json_data


    def write(self, data: list) -> None:
        self._File_IO_Wrapper.write(data)


    def done(self) -> None:
        self._File_IO_Wrapper.close()
