from collections import namedtuple

from multirunnable.persistence.file.saver import FileSaver, ArchiverSaver
from multirunnable.persistence.file.files import File
from multirunnable.persistence.file.archivers import Archiver

from .._data import Test_Data_List, Test_JSON_Data

from typing import List
import pytest


Run_Open_Process_Flag: bool = False
Run_Write_Process_Flag: bool = False
Run_Close_Process_Flag: bool = False
Run_Procedure_List: List[str] = []
Run_Result_Data_List = []

Compress_Initial_Flag: bool = False
Compress_Process_Flag: bool = False
Compress_Close_Flag: bool = False
Compress_Result_Data_List = []


class _ExampleTestingFile(File):

    def open(self) -> None:
        global Run_Open_Process_Flag, Run_Procedure_List
        Run_Open_Process_Flag = True
        Run_Procedure_List.append("open")
        print("Running 'open' process to initial file object.")


    def write(self, data: List[list]) -> None:
        global Run_Write_Process_Flag, Run_Procedure_List
        Run_Write_Process_Flag = True
        Run_Procedure_List.append("write")
        print("Running 'write' process to save data into target file object.")


    def close(self) -> None:
        global Run_Close_Process_Flag, Run_Procedure_List
        Run_Close_Process_Flag = True
        Run_Procedure_List.append("close")
        print("Running 'close' process to finish file object.")


    def stream(self, data: List[list]) -> str:
        pass



class TestFileSaver:

    def test_file_saving_procedure(self):

        class TestErrorFormatter:
            pass

        TestFileSaver._init_flag()

        # Test for invalid value
        try:
            fs = FileSaver(file=TestErrorFormatter())
        except TypeError as e:
            assert type(e) is TypeError, "It should raise exception 'TypeError' if the option value is invalid."
        except Exception as e:
            assert False, "Occur something unexpected error."

        # Test for CSV
        fs = FileSaver(file=_ExampleTestingFile())
        fs.save(file="no.no", mode="yee", encoding="UTF-8", data=Test_Data_List)
        assert Run_Open_Process_Flag is True, "It should experience 'open' process."
        assert Run_Write_Process_Flag is True, "It should experience 'write' process."
        assert Run_Close_Process_Flag is True, "It should experience 'close' process."
        assert Run_Procedure_List[0] == "open", "It should run 'open' process first."
        assert Run_Procedure_List[1] == "write", "It should run 'write' process second."
        assert Run_Procedure_List[2] == "close", "It should run 'close' process finally."


    @staticmethod
    def _init_flag():
        global Run_Open_Process_Flag, Run_Write_Process_Flag, Run_Close_Process_Flag, Run_Result_Data_List
        Run_Open_Process_Flag = False
        Run_Write_Process_Flag = False
        Run_Close_Process_Flag = False
        Run_Result_Data_List = []


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_archiver_saver_procedure(self):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_saving_stream_procedure(self):
        pass



class _ExampleTestingArchiver(Archiver):

    def init(self) -> None:
        global Compress_Initial_Flag, Compress_Result_Data_List
        Compress_Initial_Flag = True
        Compress_Result_Data_List.append("init")


    def compress(self, data_map_list: List[namedtuple]) -> None:
        global Compress_Process_Flag, Compress_Result_Data_List
        Compress_Process_Flag = True
        Compress_Result_Data_List.append("compress")


    def close(self) -> None:
        global Compress_Close_Flag, Compress_Result_Data_List
        Compress_Close_Flag = True
        Compress_Result_Data_List.append("close")



class TestArchiverSaver:

    def test_file_saving_procedure(self):

        class TestErrorFormatter:
            pass

        TestArchiverSaver._init_flag()

        # Test for invalid value
        try:
            acs = ArchiverSaver(archiver=TestErrorFormatter())
        except TypeError as e:
            assert type(e) is TypeError, "It should raise exception 'TypeError' if the option value is invalid."
        except Exception as e:
            assert False, "Occur something unexpected error."

        # Test for CSV
        acs = ArchiverSaver(archiver=_ExampleTestingArchiver())
        acs.compress(file="no.no", mode="yee", data=Test_Data_List)
        assert Compress_Initial_Flag is True, "It should experience 'init' process."
        assert Compress_Process_Flag is True, "It should experience 'compress' process."
        assert Compress_Close_Flag is True, "It should experience 'close' process."
        assert Compress_Result_Data_List[0] == "init", "It should run 'init' process first."
        assert Compress_Result_Data_List[1] == "compress", "It should run 'compress' process second."
        assert Compress_Result_Data_List[2] == "close", "It should run 'close' process finally."


    @staticmethod
    def _init_flag():
        global Compress_Initial_Flag, Compress_Process_Flag, Compress_Close_Flag, Compress_Result_Data_List
        Compress_Initial_Flag = False
        Compress_Initial_Flag = False
        Compress_Close_Flag = False
        Compress_Result_Data_List = []


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_archiver_saver_procedure(self):
        pass



