from multirunnable.persistence.file import SavingStrategy
from multirunnable.persistence.file.layer import BaseFao

from .._data import Test_Data_List, Test_JSON_Data

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

        self._fao.save_as_csv(file=f"for_testing_all.csv", mode="a+", data=Run_Result_Data_List)
        if self._strategy == SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL:
            self._fao.compress_as_zip(file=f"for_testing.zip", mode="a", data=Run_Result_Data_List)



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



@pytest.fixture(scope="function")
def example_fao() -> _ExampleTestingFao:
    return _ExampleTestingFao(strategy=SavingStrategy.ONE_THREAD_ONE_FILE)



class TestFao:

    @pytest.mark.skip(reason="Not implement testing logic yet.")
    def test_save_as_json(self, example_fao: _ExampleTestingFao):
        pass


    @pytest.mark.skip(reason="Not implement testing logic yet.")
    def test_save_as_csv(self, example_fao: _ExampleTestingFao):
        pass


    @pytest.mark.skip(reason="Not implement testing logic yet.")
    def test_save_as_excel(self, example_fao: _ExampleTestingFao):
        pass


    @pytest.mark.skip(reason="Not implement testing logic yet.")
    def test_compress_as_zip(self, example_fao: _ExampleTestingFao):
        pass


    def test_one_thread_one_file_as_csv(self):
        TestFao._init_thread_counter()

        tmt = _TestFaoMainThread(strategy=SavingStrategy.ONE_THREAD_ONE_FILE)
        tmt.process()

        for i in range(Thread_Counter - 1, -1, -1):
            file_name = f"./for_testing_{i}.csv"
            exist_file = os.path.exists(file_name)
            assert exist_file is True, f"It should exist .csv file {file_name}"
            os.remove(file_name)


    def test_all_threads_one_file_as_csv(self):
        TestFao._init_thread_counter()

        tmt = _TestFaoMainThread(strategy=SavingStrategy.ALL_THREADS_ONE_FILE)
        tmt.process()

        file_name = f"./for_testing_all.csv"
        exist_file = os.path.exists(file_name)
        assert exist_file is True, f"It should exist .csv file {file_name}"
        os.remove(file_name)


    def test_one_thread_one_file_and_compress_to_one_file_as_csv_in_zip(self):
        TestFao._init_thread_counter()

        tmt = _TestFaoMainThread(strategy=SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL)
        tmt.process()

        file_name = f"./for_testing.zip"
        exist_file = os.path.exists(file_name)
        assert exist_file is True, f"It should exist .zip file {file_name}"
        os.remove(file_name)


    @staticmethod
    def _init_thread_counter():
        global Thread_Counter, Run_Result_Data_List
        Thread_Counter = 0
        Run_Result_Data_List = []

