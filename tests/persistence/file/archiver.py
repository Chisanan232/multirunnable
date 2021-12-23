from multirunnable.persistence.file.archivers import ZIPArchiver
from multirunnable.persistence.file.saver import FileSaver
from multirunnable.persistence.file.files import CSVFormatter

from .._data import Test_Data_List

from collections import namedtuple
from pathlib import Path
import pytest
import os


Test_CSV_File_Path: str = str(Path("./for_testing.csv"))
Test_ZIP_File_Path: str = str(Path("./for_testing.zip"))

Test_Mode: str = "a"
Test_Encoding: str = "UTF-8"

ZipData = namedtuple("ZipData", ["file_path", "data"])


@pytest.fixture(scope="function")
def zip_archiver():
    return ZIPArchiver()


class TestArchiver:

    def test_compress_as_zip(self, zip_archiver: ZIPArchiver):
        _test_file_path = Test_ZIP_File_Path
        zip_archiver.file_path = _test_file_path
        zip_archiver.mode = Test_Mode
        assert zip_archiver.file_path == _test_file_path
        assert zip_archiver.mode == Test_Mode

        _csv_format = CSVFormatter()
        _csv_format.file_path = Test_CSV_File_Path
        _csv_format.mode = Test_Mode
        _csv_format.encoding = Test_Encoding
        _data_stream = _csv_format.stream(data=Test_Data_List)
        _zip_data = ZipData(file_path=Test_CSV_File_Path, data=_data_stream)

        try:
            zip_archiver.init()
            zip_archiver.compress(data_map_list=[_zip_data])
            zip_archiver.close()
        except Exception as e:
            assert False, f""
        else:
            assert True, f""

        _exist_file = os.path.exists(_test_file_path)
        assert _exist_file is True, "It should exist a .zip file."

        os.remove(_test_file_path)

