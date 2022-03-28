from multirunnable import set_mode, RunningMode
from multirunnable.adapter.context import context as adapter_context
from multirunnable.persistence.file import SavingStrategy, CSVFormatter
from multirunnable.persistence.file.layer import BaseFao
from multirunnable.persistence.file.saver import _Done_Flag, _Do_Nothing_Flag

from .._data import Test_Data_List, Test_JSON_Data

from typing import Union
from collections import namedtuple
import threading
import pytest
import os


Run_Result_Data_List = []

Thread_Number = 3
Thread_Counter = 0
Thread_Lock = threading.Lock()


class _ExampleTestingFao(BaseFao):
    pass



class _TestFaoMainThread:

    def __init__(self, strategy: SavingStrategy):
        self._strategy = strategy
        self._fao = _ExampleTestingFao(strategy=strategy)


    def process(self):
        thread_list = [_TestFaoClientThread(fao=self._fao) for _ in range(Thread_Number)]
        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        self._fao.save_as_csv(file="for_testing_all.csv", mode="a+", data=Run_Result_Data_List)
        if self._strategy == SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL:
            self._fao.compress_as_zip(file="for_testing.zip", mode="a", data=Run_Result_Data_List)



class _TestFaoClientThread(threading.Thread):

    def __init__(self, fao: BaseFao):
        super().__init__()
        self.fao = fao


    def run(self) -> None:
        with Thread_Lock:
            global Thread_Counter
            data = Test_Data_List[Thread_Counter]
            final_data = self.fao.save_as_csv(file=f"for_testing_{Thread_Counter}.csv", mode="a+", data=[data])
            if final_data != 0 and final_data != 1:
                for _data in final_data:
                    Run_Result_Data_List.append(_data)
            Thread_Counter += 1



class TestFao:

    @pytest.mark.parametrize(
        "saving_strategy",
        argvalues=[SavingStrategy.ONE_THREAD_ONE_FILE, SavingStrategy.ALL_THREADS_ONE_FILE, SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL],
    )
    def test_save_as_json(self, saving_strategy: SavingStrategy):
        set_mode(mode=RunningMode.Concurrent)

        _example_fao = _ExampleTestingFao(strategy=saving_strategy)
        _file_path = "test.json"
        # # Run in parent worker.
        _result = _example_fao.save_as_json(file=_file_path, mode="a+", data=[[Test_JSON_Data]])

        TestFao._checking_process(_strategy=saving_strategy, _result=_result, _file_path=_file_path)


    @pytest.mark.parametrize(
        "saving_strategy",
        argvalues=[SavingStrategy.ONE_THREAD_ONE_FILE, SavingStrategy.ALL_THREADS_ONE_FILE, SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL]
    )
    def test_save_as_csv(self, saving_strategy: SavingStrategy):
        set_mode(mode=RunningMode.Concurrent)

        _example_fao = _ExampleTestingFao(strategy=saving_strategy)
        _file_path = "test.csv"
        # # Run in parent worker.
        _result = _example_fao.save_as_csv(file=_file_path, mode="a+", data=Test_Data_List)

        TestFao._checking_process(_strategy=saving_strategy, _result=_result, _file_path=_file_path)


    @pytest.mark.xfail(reason="It doesn't support process data to streaming with file format '.xlsx'. But it supports '.json' and '.csv'.")
    @pytest.mark.parametrize(
        "saving_strategy",
        argvalues=[SavingStrategy.ONE_THREAD_ONE_FILE, SavingStrategy.ALL_THREADS_ONE_FILE, SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL]
    )
    def test_save_as_excel(self, saving_strategy: SavingStrategy):
        set_mode(mode=RunningMode.Concurrent)

        _example_fao = _ExampleTestingFao(strategy=saving_strategy)
        _file_path = "test.xlsx"
        # # Run in parent worker.
        _result = _example_fao.save_as_excel(file=_file_path, mode="a+", data=Test_Data_List)

        TestFao._checking_process(_strategy=saving_strategy, _result=_result, _file_path=_file_path)


    @staticmethod
    def _checking_process(_strategy: SavingStrategy, _result: Union[list, int], _file_path: str):
        if _strategy is SavingStrategy.ONE_THREAD_ONE_FILE:
            if TestFao._is_alone() is True:
                assert _result == _Done_Flag, "If it's children worker or alone by itself, it should save the data as target file format."
                TestFao._check_file_and_remove_it(_file_path=_file_path)
            else:
                assert _result == _Do_Nothing_Flag, "If it's main worker, it should do nothing."

        elif _strategy is SavingStrategy.ALL_THREADS_ONE_FILE:
            if TestFao._is_alone() is True:
                # Get the data we pass
                assert _result is not None, "If it's main worker, it should get the object which saving data."
            else:
                assert _result == _Done_Flag, "If it's main worker, it should save the data as target file format."
                TestFao._check_file_and_remove_it(_file_path=_file_path)

        elif _strategy is SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL:
            if TestFao._is_alone() is True:
                assert _result is not None, "If it's children worker or alone by itself, it should return the data streaming object."
            else:
                assert _result == _Do_Nothing_Flag, "If it's main worker but call method 'save_as_xxx', it should do nothing."

        else:
            assert False, "The option value is invalid."


    @staticmethod
    def _is_alone() -> bool:
        return adapter_context.active_workers_count() == 1


    @pytest.mark.parametrize(
        "saving_strategy",
        argvalues=[SavingStrategy.ONE_THREAD_ONE_FILE, SavingStrategy.ALL_THREADS_ONE_FILE, SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL]
    )
    def test_compress_as_zip(self, saving_strategy: SavingStrategy):
        set_mode(mode=RunningMode.Concurrent)

        _example_fao = _ExampleTestingFao(strategy=saving_strategy)
        _csv_file_path = "test.csv"
        _zip_file_path = "test.zip"
        try:
            _result_data = CSVFormatter().stream(data=Test_Data_List)
            _DataStream = namedtuple("DataStream", ("file_path", "data"))
            _DataStream.file_path = _csv_file_path
            _DataStream.data = _result_data
            _example_fao.compress_as_zip(file=_zip_file_path, mode="a", data=[_DataStream])
        except ValueError as ve:
            assert saving_strategy is not SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL, "It must be not 'SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL'."
            assert "The compress process only work with strategy 'ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL'" in str(ve), "It should raise an exception about it doesn't support current saving strategy."
        else:
            TestFao._check_file_and_remove_it(_file_path=_zip_file_path)


    @staticmethod
    def _check_file_and_remove_it(_file_path: str):
        _exist_file = os.path.exists(_file_path)
        assert _exist_file is True, f"It should exist file {_file_path}."
        os.remove(_file_path)


    def test_saving_strategy_one_thread_one_file(self):
        TestFao._init_thread_counter()

        tmt = _TestFaoMainThread(strategy=SavingStrategy.ONE_THREAD_ONE_FILE)
        tmt.process()

        for i in range(Thread_Counter - 1, -1, -1):
            file_name = f"./for_testing_{i}.csv"
            exist_file = os.path.exists(file_name)
            assert exist_file is True, f"It should exist .csv file {file_name}"
            os.remove(file_name)


    def test_saving_strategy_all_threads_one_file(self):
        TestFao._init_thread_counter()

        tmt = _TestFaoMainThread(strategy=SavingStrategy.ALL_THREADS_ONE_FILE)
        tmt.process()

        file_name = "./for_testing_all.csv"
        exist_file = os.path.exists(file_name)
        assert exist_file is True, f"It should exist .csv file {file_name}"
        os.remove(file_name)


    def test_saving_strategy_one_thread_one_file_and_compress_to_one_file(self):
        TestFao._init_thread_counter()

        tmt = _TestFaoMainThread(strategy=SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL)
        tmt.process()

        file_name = "./for_testing.zip"
        exist_file = os.path.exists(file_name)
        assert exist_file is True, f"It should exist .zip file {file_name}"
        os.remove(file_name)


    @staticmethod
    def _init_thread_counter():
        global Thread_Counter, Run_Result_Data_List
        Thread_Counter = 0
        Run_Result_Data_List = []

