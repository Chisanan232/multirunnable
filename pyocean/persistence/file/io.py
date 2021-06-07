from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Iterable, Union
from openpyxl import Workbook
import json
import csv
import io



class BaseDataIO(metaclass=ABCMeta):

    _String_IO = io.StringIO()

    @property
    # @abstractmethod
    def file_path(self) -> str:
        pass


    @abstractmethod
    def generate_io(self, data: Union[List, Tuple]) -> str:
        pass



class CSVDataIO(BaseDataIO):

    def generate_io(self, data: Union[List, Tuple]) -> str:
        csv_writer = csv.writer(self._String_IO)
        for __data_row in data:
            csv_writer.writerow(__data_row)
        return self._String_IO.read()



class ExcelDataIO(BaseDataIO):

    __Sheet_Page_Name = "data"

    def generate_io(self, data: Union[List, Tuple]) -> str:
        workbook = Workbook()
        sheet_page = workbook.create_sheet(index=0, title=self.__Sheet_Page_Name)
        for __data_row in data:
            sheet_page.append(__data_row)
        workbook.save(self.file_path)



class JSONDataIO(BaseDataIO):

    def generate_io(self, data: Union[List, Tuple]) -> str:
        json_data = json.dumps(data, ensure_ascii=False)
        return json_data

