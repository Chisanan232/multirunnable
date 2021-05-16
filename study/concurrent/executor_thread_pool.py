from concurrent.futures import ThreadPoolExecutor, Future
from datetime import datetime
from typing import List
import os


class ThreadExecutorTest:

    def __init__(self, executor_number: int):
        self.__executor_number = executor_number


    def init_data(self):
        return ["ele_1", "ele_2", "ele_3", "ele_4", "ele_5", "ele_6"]


    def running_process(self, ele):
        print(f"ele: {ele} - {datetime.now()} - {os.getpid()}")


    def test_main(self):
        target_ele = self.init_data()
        # self.open_and_run_as_with(target_ele=target_ele)
        self.open_and_run_as_list(target_ele=target_ele)


    def open_and_run_as_with(self, target_ele: List[str]) -> None:
        """
        Initialize and activate the Future type objects to run via keyword 'with'
        :param target_ele:
        :return:
        """

        future_list = []

        with ThreadPoolExecutor(max_workers=self.__executor_number) as executor:
            for ele in target_ele:
                ps_future = executor.submit(self.running_process, ele)
                future_list.append(ps_future)

            self.print_future_something(future_list=future_list)


    def open_and_run_as_list(self, target_ele: List[str]):
        """
        Initialize and activate the Future type objects to run with the procedures.
        What procedure?
            1. Initialize
            2. Assign tasks
            3. Activate to run target tasks
            4. Do something after executors done.
        :param target_ele:
        :return:
        """

        executor_pool = ThreadPoolExecutor(max_workers=self.__executor_number)
        future_list = [executor_pool.submit(self.running_process, ele) for ele in target_ele]
        self.print_future_something(future_list=future_list)


    def print_future_something(self, future_list: List[Future]):
        """
        Print something Future info.
        :param future_list:
        :return:
        """

        for future in future_list:
            print(f"Future result: {future.result()}")
            print(f"Future done: {future.done()}")
            print(f"Future cancel: {future.cancel()}")
            print(f"Future exception: {future.exception()}")
            # print(f"Future exception_info: {future.exception_info()}")
            print(f"Future running: {future.running()}")


if __name__ == '__main__':

    __executor_number = 5

    test = ThreadExecutorTest(executor_number=__executor_number)
    test.test_main()
