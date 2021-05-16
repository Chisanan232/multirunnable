from datetime import datetime
from typing import Callable, Iterable
import threading
import random
import time
import os



class TestThread(threading.Thread):

    def run(self):
        print(f"Thread: {threading.currentThread().getName()}.")



class ThreadFactory:

    def __init__(self, thread_number):
        self.__thread_num = thread_number


    def init(self, function: Callable):
        return [threading.Thread(target=function) for _ in range(self.__thread_num)]


    def init_new(self, function: Callable):
        thread_list = []
        for i in range(self.__thread_num):
            t = threading.Thread(target=function)
            thread_list.append(t)
            thread_list[i].start()
            # thread_list[i].run()


    def run_task(self, threads_list: Iterable[threading.Thread]):
        for thread in threads_list:
            thread.start()


class TargetClass:

    @classmethod
    def target_fun(cls):
        cls.thread_running_fun()


    @classmethod
    def thread_running_fun(cls):
        print(f"Thread: {threading.currentThread().getName()}.")



class ThreadStudy01:

    def __init__(self, thread_number):
        self.__thread_factory = ThreadFactory(thread_number=thread_number)

    def main(self):
        # # Method 1
        thread_list = self.__thread_factory.init(self.thread_running_fun)
        # thread_list = self.__thread_factory.init(TargetClass.target_fun)
        self.__thread_factory.run_task(threads_list=thread_list)

        # # Method 2
        # self.__thread_factory.init_new(function=self.thread_running_fun)


    def thread_running_fun(self):
        print(f"Thread: {threading.currentThread().getName()}.")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep {sleep_time} seconds ... - {threading.currentThread().getName()}")
        time.sleep(sleep_time)


    def test_main(self):
        test_threads_list = [TestThread() for _ in range(10)]
        for thread in test_threads_list:
            thread.start()

        for thread in test_threads_list:
            thread.join()



if __name__ == '__main__':

    __thread_number = 10
    study01 = ThreadStudy01(thread_number=__thread_number)
    study01.main()
    # study01.test_main()
