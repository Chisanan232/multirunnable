from multirunnable import set_mode, get_current_mode, RunningMode
from multirunnable.parallel.strategy import Global_Manager
from multirunnable.persistence.file import SavingStrategy, SavingMediator
from multirunnable.persistence.file.saver import FileSaver, ArchiverSaver, _Done_Flag, _Do_Nothing_Flag
from multirunnable.persistence.file.files import File
from multirunnable.persistence.file.archivers import Archiver

from tests.test_config import Under_Test_RunningModes
from .._data import Test_Data_List

from collections import namedtuple
from typing import List
import multiprocessing
import threading
import pytest
import os


Global_Run_Flags: dict = Global_Manager.dict({
    "Run_Open_Process_Flag": False,
    "Run_Write_Process_Flag": False,
    "Run_Close_Process_Flag": False
})

Run_Open_Process_Flag: bool = False
Run_Write_Process_Flag: bool = False
Run_Close_Process_Flag: bool = False
Run_Procedure_List: List[str] = Global_Manager.list()

Compress_Initial_Flag: bool = False
Compress_Process_Flag: bool = False
Compress_Close_Flag: bool = False
Compress_Result_Data_List = []


class _ExampleTestingFile(File):

    def open(self) -> None:
        global Global_Run_Flags, Run_Procedure_List
        Global_Run_Flags["Run_Open_Process_Flag"] = True
        Run_Procedure_List.append("open")
        print("Running 'open' process to initial file object.")


    def write(self, data: List[list]) -> None:
        global Global_Run_Flags, Run_Procedure_List
        Global_Run_Flags["Run_Write_Process_Flag"] = True
        Run_Procedure_List.append("write")
        print("Running 'write' process to save data into target file object.")


    def close(self) -> None:
        global Global_Run_Flags, Run_Procedure_List
        Global_Run_Flags["Run_Close_Process_Flag"] = True
        Run_Procedure_List.append("close")
        print("Running 'close' process to finish file object.")


    def stream(self, data: List[list]) -> str:
        pass


class _TestProcess(multiprocessing.Process):

    def __init__(self, fs: FileSaver):
        super().__init__()
        self.fs = fs

    def run(self) -> None:
        _thread_result = self.fs.save(file="no.no", mode="yee", encoding="UTF-8", data=Test_Data_List)
        assert _thread_result == _Done_Flag, ""


class _TestThread(threading.Thread):

    def __init__(self, fs):
        super().__init__()
        self.fs = fs

    def run(self) -> None:
        _thread_result = self.fs.save(file="no.no", mode="yee", encoding="UTF-8", data=Test_Data_List)
        assert _thread_result == _Done_Flag, ""


@pytest.fixture(scope="function")
def file_saver(request) -> FileSaver:
    set_mode(mode=request.param)

    TestFileSaver._init_flag()

    fs = FileSaver(file=_ExampleTestingFile())
    return fs



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
        global Global_Run_Flags, Run_Procedure_List
        assert Global_Run_Flags["Run_Open_Process_Flag"] is True, "It should experience 'open' process."
        assert Global_Run_Flags["Run_Write_Process_Flag"] is True, "It should experience 'write' process."
        assert Global_Run_Flags["Run_Close_Process_Flag"] is True, "It should experience 'close' process."
        assert Run_Procedure_List[0] == "open", "It should run 'open' process first."
        assert Run_Procedure_List[1] == "write", "It should run 'write' process second."
        assert Run_Procedure_List[2] == "close", "It should run 'close' process finally."


    @pytest.mark.parametrize(
        argnames="file_saver",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_saving_with_one_worker_one_file(self, file_saver: FileSaver):
        _mediator = SavingMediator()
        file_saver.register(mediator=_mediator, strategy=SavingStrategy.ONE_THREAD_ONE_FILE)

        if get_current_mode(force=True) is RunningMode.Parallel:
            _worker = _TestProcess(file_saver)
        else:
            _worker = _TestThread(file_saver)
        _worker.start()
        _worker.join()

        _result = file_saver.save(file="no.no", mode="yee", encoding="UTF-8", data=Test_Data_List)
        assert _result == _Do_Nothing_Flag, ""

        global Global_Run_Flags, Run_Procedure_List
        assert Global_Run_Flags["Run_Open_Process_Flag"] is True, "It should experience 'open' process."
        assert Global_Run_Flags["Run_Write_Process_Flag"] is True, "It should experience 'write' process."
        assert Global_Run_Flags["Run_Close_Process_Flag"] is True, "It should experience 'close' process."
        assert Run_Procedure_List[0] == "open", "It should run 'open' process first."
        assert Run_Procedure_List[1] == "write", "It should run 'write' process second."
        assert Run_Procedure_List[2] == "close", "It should run 'close' process finally."


    @pytest.mark.parametrize(
        argnames="file_saver",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_saving_with_all_workers_one_file(self, file_saver: FileSaver):

        class _TestThread(threading.Thread):
            def run(self) -> None:
                _thread_result = file_saver.save(file="no.no", mode="yee", encoding="UTF-8", data=Test_Data_List)
                assert _thread_result is not None, ""

        _mediator = SavingMediator()
        file_saver.register(mediator=_mediator, strategy=SavingStrategy.ALL_THREADS_ONE_FILE)

        _thread = _TestThread()
        _thread.start()
        _thread.join()

        _result = file_saver.save(file="no.no", mode="yee", encoding="UTF-8", data=Test_Data_List)
        assert _result == _Done_Flag, ""

        global Global_Run_Flags, Run_Procedure_List
        assert Global_Run_Flags["Run_Open_Process_Flag"] is True, "It should experience 'open' process."
        assert Global_Run_Flags["Run_Write_Process_Flag"] is True, "It should experience 'write' process."
        assert Global_Run_Flags["Run_Close_Process_Flag"] is True, "It should experience 'close' process."
        assert Run_Procedure_List[0] == "open", "It should run 'open' process first."
        assert Run_Procedure_List[1] == "write", "It should run 'write' process second."
        assert Run_Procedure_List[2] == "close", "It should run 'close' process finally."


    @pytest.mark.parametrize(
        argnames="file_saver",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_saving_with_one_worker_one_file_and_compress_all(self, file_saver: FileSaver):

        class _TestThread(threading.Thread):
            def run(self) -> None:
                _thread_result = file_saver.save(file="no.no", mode="yee", encoding="UTF-8", data=Test_Data_List)
                assert _thread_result is not None, ""

        _mediator = SavingMediator()
        file_saver.register(mediator=_mediator, strategy=SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL)

        _thread = _TestThread()
        _thread.start()
        _thread.join()

        _result = file_saver.save(file="no.no", mode="yee", encoding="UTF-8", data=Test_Data_List)
        assert _result == _Do_Nothing_Flag, ""

        assert Run_Open_Process_Flag is False, "It should not experience 'open' process."
        assert Run_Write_Process_Flag is False, "It should not experience 'write' process."
        assert Run_Close_Process_Flag is False, "It should not experience 'close' process."
        assert len(Run_Procedure_List) == 0, "It should have nothing in running procedure list."


    @staticmethod
    def _init_flag():
        global Global_Run_Flags, Run_Procedure_List
        Global_Run_Flags["Run_Open_Process_Flag"] = False
        Global_Run_Flags["Run_Write_Process_Flag"] = False
        Global_Run_Flags["Run_Close_Process_Flag"] = False
        Run_Procedure_List[:] = []


    @staticmethod
    def _check_file_and_remove_it(_file_path: str):
        _exist_file = os.path.exists(_file_path)
        assert _exist_file is True, f"It should exist file {_file_path}."
        os.remove(_file_path)



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

    def test_archiver_saving_procedure(self):

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
        Compress_Result_Data_List[:] = []


