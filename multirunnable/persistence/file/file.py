from multirunnable.persistence.file.exceptions import DataRowFormatIsInvalidError

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Iterable, Union
from openpyxl import Workbook
import json
import csv
import io



class BaseFileFormatter(metaclass=ABCMeta):

    _File_IO_Wrapper: object = None

    @abstractmethod
    def open(self, file_path: str, open_mode: str, encoding: str) -> None:
        pass


    @abstractmethod
    def data_handling(self, data: List[list]) -> Union[List[list], str]:
        new_data = self.chk_data_rows_format(data=data)
        return new_data


    def chk_data_rows_format(self, data: Iterable) -> List:
        """
        Description:
            Check the data format of data row is valid or invalid.
            It will raise DataRowFormatIsInvalidError if the data
            format is invalid.
        :param data:
        :return:
        """
        __checksum = map(self.__is_data_row, data)
        if False in list(__checksum):
            raise DataRowFormatIsInvalidError
        else:
            return data


    def __is_data_row(self, data_row: Iterable) -> bool:
        """
        Description:
            First step: Checking first level of data format tree.
        :param data_row:
        :return:
        """
        if isinstance(data_row, List) or isinstance(data_row, Tuple):
            return self.__is_data_content(data_row=data_row)
        else:
            return False


    def __is_data_content(self, data_row: Iterable) -> bool:
        """
        Description:
            First step: Checking second level of data format tree.
        :param data_row:
        :return:
        """
        chk_data_content = map(
            lambda row: False if isinstance(row, List) or isinstance(row, Tuple) else True,
            data_row)
        if False in list(chk_data_content):
            return False
        else:
            return True


    @abstractmethod
    def write(self, data: list) -> None:
        pass


    @abstractmethod
    def done(self) -> None:
        pass



class CsvFileFormatter(BaseFileFormatter):

    def open(self, file_path: str, open_mode: str, encoding: str) -> None:
        self._File_IO_Wrapper = open(file=file_path, mode=open_mode, newline='', encoding=encoding)


    def data_handling(self, data: List[list]) -> Union[List[list], str]:
        data = super(CsvFileFormatter, self).data_handling(data=data)
        csv_data: List[list] = [d for d in data]
        return csv_data


    def write(self, data: list) -> None:
        csv_obj = csv.writer(self._File_IO_Wrapper)
        for data_line in data:
            csv_obj.writerow(data_line)


    def done(self) -> None:
        self._File_IO_Wrapper.close()



class XlsxFileFormatter(BaseFileFormatter):

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


    def data_handling(self, data: List[list]) -> Union[List[list], str]:
        data = super(XlsxFileFormatter, self).data_handling(data=data)
        csv_data: List[list] = [d for d in data]
        return csv_data


    def write(self, data: list) -> None:
        for d in data:
            self.__Work_Sheet_Page.append(d)


    def done(self) -> None:
        self._File_IO_Wrapper.save(self.__Excel_File_Path)



class JsonFileFormatter(BaseFileFormatter):

    def open(self, file_path: str, open_mode: str, encoding: str) -> None:
        self._File_IO_Wrapper = open(file=file_path, mode=open_mode, encoding=encoding)


    def data_handling(self, data: List[list]) -> Union[List[list], str]:
        json_data = json.dumps(data, ensure_ascii=False)
        return json_data


    def write(self, data: list) -> None:
        self._File_IO_Wrapper.write(data)


    def done(self) -> None:
        self._File_IO_Wrapper.close()



class BaseDataFormatterString(metaclass=ABCMeta):

    @property
    @abstractmethod
    def file_path(self) -> str:
        pass


    @file_path.setter
    @abstractmethod
    def file_path(self, path: str) -> None:
        pass


    @property
    @abstractmethod
    def data(self) -> str:
        pass


    @data.setter
    @abstractmethod
    def data(self, data: str) -> None:
        pass


    @abstractmethod
    def data_string(self, data: List[list]) -> Union[str, bytes]:
        pass



class CsvDataString(BaseDataFormatterString):

    __File_Path: str = ""
    __Data: Union[str, bytes] = ""

    @property
    def file_path(self) -> str:
        return self.__File_Path


    @file_path.setter
    def file_path(self, path: str) -> None:
        self.__File_Path = path


    @property
    def data(self) -> str:
        return self.__Data


    @data.setter
    def data(self, data: str) -> None:
        self.__Data = data


    def data_string(self, data: List[list]) -> None:
        string_io = io.StringIO()
        csv_writer = csv.writer(string_io)
        for __data_row in data:
            csv_writer.writerow(__data_row)
        string_io.seek(0)
        self.data = string_io.read()



class JsonDataString(BaseDataFormatterString):

    __File_Path: str = ""
    __Data: Union[str, bytes] = ""

    @property
    def file_path(self) -> str:
        return self.__File_Path


    @file_path.setter
    def file_path(self, path: str) -> None:
        self.__File_Path = path


    @property
    def data(self) -> str:
        return self.__Data


    @data.setter
    def data(self, data: str) -> None:
        self.__Data = data


    def data_string(self, data: List[list]) -> None:
        json_data = json.dumps(data, ensure_ascii=False)
        self.data = json_data
