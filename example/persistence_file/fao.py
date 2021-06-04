from pyocean.persistence.file import SingleFileSaver, MultiFileSaver, JSONFormatter, CSVFormatter, ExcelFormatter

from typing import Iterable, List
import logging



class TestFao:

    __JSON_File_Path = "/Users/bryantliu/DevelopProject/KobeDevelopProject/Crawler-PyFrameworok/" \
                       "apache-pyocean/example/sample_data/test_json_saver.json"
    __CSV_File_Path = "/Users/bryantliu/DevelopProject/KobeDevelopProject/Crawler-PyFrameworok/" \
                      "apache-pyocean/example/sample_data/test_json_saver.csv"
    __Excel_File_Path = "/Users/bryantliu/DevelopProject/KobeDevelopProject/Crawler-PyFrameworok/" \
                        "apache-pyocean/example/sample_data/test_json_saver.xlsx"

    @classmethod
    def save_data_as_json(cls, data: Iterable):
        __saver = SingleFileSaver(file_path=cls.__JSON_File_Path, file_format=JSONFormatter())
        if isinstance(data, List):
            __saver.save(data=data)
        else:
            logging.warning("The data structure is not perfectly mapping.")
            __saver.save(data=data)


    @classmethod
    def save_data_as_csv(cls, data: Iterable):
        __saver = SingleFileSaver(file_path=cls.__CSV_File_Path, file_format=CSVFormatter())
        if isinstance(data, List):
            __saver.save(data=data)
        else:
            logging.warning("The data structure is not perfectly mapping.")
            __saver.save(data=data)


    @classmethod
    def save_data_as_excel(cls, data: Iterable):
        __saver = SingleFileSaver(file_path=cls.__Excel_File_Path, file_format=ExcelFormatter())
        if isinstance(data, List):
            __saver.save(data=data)
        else:
            logging.warning("The data structure is not perfectly mapping.")
            __saver.save(data=data)



class TestAsyncFao:

    @classmethod
    def save_data_as_json(cls, data: Iterable):
        __saver = SingleFileSaver(file_path="", file_format=JSONFormatter())
        if isinstance(data, List):
            __saver.save(data=data)
        else:
            logging.warning("The data structure is not perfectly mapping.")
            __saver.save(data=data)
