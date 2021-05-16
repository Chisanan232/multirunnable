from multiprocessing.pool import ThreadPool, ApplyResult
from typing import List
import os



class TestPool:

    __Threads_List: List[ApplyResult] = []

    @classmethod
    def run(cls):
        __number = 5
        thread_pool = ThreadPool(processes=__number, initializer=cls.multi_working_init, initargs=(1, ))
        for n in range(__number):
            params = {"index": n}
            thread = thread_pool.apply_async(func=cls.main_run, kwds=params)
            cls.__Threads_List.append(thread)

        for t in cls.__Threads_List:
            __result = t.get()
            __successful = t.successful()
            print(f"Result: {__result}")
            print(f"Successful: {__successful}")

        thread_pool.close()
        thread_pool.join()


    @classmethod
    def multi_working_init(cls, index):
        print("Initialize something ...")
        print("Initial parameter: ", index)


    @classmethod
    def main_run(cls, index):
        print(f"Target function to run ! - {index}, pid: {os.getpid()}")


if __name__ == '__main__':

    TestPool.run()
