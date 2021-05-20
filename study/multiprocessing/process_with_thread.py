from package_multiprocessing.pool import Pool, AsyncResult
from package_multiprocessing import Manager
from threading import Thread, currentThread
from package_greenlet import greenlet, getcurrent as get_current_greenlet
from typing import List, Callable, Iterable, Union
from datetime import datetime
import asyncio
import aiohttp
import random
import psutil
import time
import os



class TestCommon:

    A = "a"

    def __str__(self):
        return "TestCommon"

    def __repr__(self):
        return "TestCommon"

    def test_fun(self):
        print("This is common object.")



class ProcessFactory:

    """
    Parallel
    """

    def __init__(self, process_number):
        self.__process_num = process_number


    def init(self):
        __manager = Manager()
        __common_object = __manager.Namespace()
        test_common_cls = TestCommon
        test_common_obj = TestCommon()
        print(f"test_common_cls is Callable type: {isinstance(test_common_cls, Callable)}")
        print(f"test_common_cls is object type: {isinstance(test_common_cls, object)}")
        print(f"test_common_obj is Callable type: {isinstance(test_common_obj, Callable)}")
        print(f"test_common_obj is object type: {isinstance(test_common_obj, object)}")
        print(f"__common_object: {__common_object}")
        print(f"TestCommon(): {test_common_obj}")
        setattr(__common_object, str(test_common_obj), test_common_obj)
        tco = getattr(__common_object, str(test_common_obj))
        print(f"__common_object: {__common_object}")
        print(f"tco: {tco}")
        print(f"Is tco a type of class TestCommon: {isinstance(tco, TestCommon)}")
        return Pool(processes=self.__process_num)


    def assign_task(self, pool: Pool, function):
        return [pool.apply_async(func=function) for _ in range(self.__process_num)]


    def run_task(self, pool_list: List[AsyncResult]):
        for pool in pool_list:
            running_result = pool.get()
            running_successful = pool.successful()
            print(f"Process running result: {running_result} \n Runnig state: {running_successful}")



class ThreadFactory:

    """
    Concurrent
    """

    def __init__(self, thread_number):
        self.__thread_num = thread_number


    def init(self, function: Callable):
        return [Thread(target=function) for _ in range(self.__thread_num)]


    def run_task(self, threads_list: Iterable[Thread]):
        for thread in threads_list:
            # thread.run()
            thread.start()



class GreenletFactory:

    """
    Concurrent with greenlet
    """

    def __init__(self, greenlet_number):
        self.__greenlet_num = greenlet_number


    def init(self, function: Callable):
        return [greenlet(run=function) for _ in range(self.__greenlet_num)]


    def run_task(self, greenlet_list: List[greenlet]):
        for gl in greenlet_list:
            gl.switch()



class AsyncFactory:

    """
    Coroutine wit asynchronous

    Note:
        For this condition for multiprocessing running strategy, it will raise an exception like below:

        Traceback (most recent call last):
          File "./MultiThread_Crawler_Framework/study/multiprocess/process_with_thread.py", line 227, in <module>
            process_with_thread.main()
          File "./MultiThread_Crawler_Framework/study/multiprocess/process_with_thread.py", line 164, in main
            self.__process_factory.run_task(pool_list=running_process_pool)
          File "./MultiThread_Crawler_Framework/study/multiprocess/process_with_thread.py", line 36, in run_task
            running_result = pool.get()
          File "/anaconda3/lib/python3.7/multiprocessing/pool.py", line 657, in get
            raise self._value
          File "/anaconda3/lib/python3.7/multiprocessing/pool.py", line 431, in _handle_tasks
            put(task)
          File "/anaconda3/lib/python3.7/multiprocessing/connection.py", line 206, in send
            self._send_bytes(_ForkingPickler.dumps(obj))
          File "/anaconda3/lib/python3.7/multiprocessing/reduction.py", line 51, in dumps
            cls(buf, protocol).dump(obj)
        AttributeError: Can't pickle local object 'WeakSet.__init__.<locals>._remove'

        This issue be pending currently  because I have no idea why it occur here.

    """

    def __init__(self, thread_number, event_loop):
        self.__thread_num = thread_number
        self.__loop = event_loop


    async def run_task(self):
        # # Method 1.
        tasks = [self.__loop.create_task(self.task_component(index)) for index in range(self.__thread_num)]
        # # Method 2.
        # tasks = [asyncio.create_task(self.task_component(index)) for index in range(self.__thread_num)]
        # # Method 3.
        # tasks = []
        # for index in range(self.__thread_num):
        #     task = None
        #     try:
        #         task = self.__loop.create_task(self.task_component(index))
        #         tasks.append(task)
        #     except Exception as e:
        #         print(f"Catch the exception! Exception: {e}")
        #         print("Will cancel the Coroutine ...")
        #         task.cancel()
        #         print("Cancel the Coroutine successfully.")
        #     else:
        #         print(f"Activate the coroutine successfully without any exception.")
        #         # print(f"Try to get the result: {task.result()}")

        print("+=+=+=+ Will wait for all coroutine task scheduler finish and it will keep go ahead to running left "
              "tasks. +=+=+=+")
        finished, unfinished = await asyncio.wait(tasks)
        print(f"Finished: {finished}. \nUnfinished: {unfinished}.")
        for finish in finished:
            event_loop = finish.get_loop()
            exception = finish.exception()
            done_flag = finish.done()
            result_flag = finish.result()
            # if result_flag == "Greenlet-8":
            #     finish.set_result(result={"test": "test_1"})
            #     result_flag = finish.result()
            print(f"+----------------------------------------------------+ \n"
                  f"This is something report for the coroutine done: \n"
                  f"event loop: {event_loop} \n"
                  f"exception: {exception} \n"
                  f"done_flag: {done_flag} \n"
                  f"result_flag: {result_flag} \n"
                  f"+----------------------------------------------------+")


    async def task_component(self,  index):
        print(f"This is task {index} - name as Greenlet-{index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds ... - Greenlet-{index}")
        await asyncio.sleep(sleep_time)
        if index == 7:
            # print(f"Wake up to go ahead! - Greenlet-{index}")
            raise Exception("This exception be raise for lucky number.")
        else:
            print(f"Wake up to go ahead! - Greenlet-{index}")
            return f"Greenlet-{index}"


class MultiProcessWithThread:

    def __init__(self, process_num, thread_num):
        self.__process_num = process_num
        self.__thread_num = thread_num
        self.__process_factory = ProcessFactory(process_number=process_num)
        self.__thread_factory = ThreadFactory(thread_number=thread_num)
        self.__greenlet_factory = GreenletFactory(greenlet_number=thread_num)
        self.__event_loop = asyncio.get_event_loop()
        self.__async_factory = AsyncFactory(thread_number=thread_num, event_loop=self.__event_loop)


    def main(self):
        print(f"Time: {datetime.now()} - This is Main Thread - PID: {os.getpid()}. PPID: {os.getppid()}")
        process_pool = self.__process_factory.init()
        running_process_pool = self.__process_factory.assign_task(pool=process_pool, function=self.process_running_fun)
        self.__process_factory.run_task(pool_list=running_process_pool)


    def process_running_fun(self):
        print(f"Time: {datetime.now()} - This is Process code - PID: {os.getpid()}. PPID: {os.getppid()}")
        # # Thread Factory
        # thread_list = self.thread_factory.init(function=self.thread_running_fun)
        # self.thread_factory.run_task(threads_list=thread_list)

        # # Greenlet Factory
        # greenlet_list = self.greenlet_factory.init(function=self.greenlet_running_fun)
        # self.greenlet_factory.run_task(greenlet_list=greenlet_list)

        # # Async Factory
        # # Method 1.
        try:
            self.__event_loop.run_until_complete(self.__async_factory.run_task())
        except Exception as e:
            print(f"Test for catch the coroutine exception.")
            print(f"exception: {e}")

        # # Method 2.
        # tasks = [asyncio.create_task(self.__async_factory.task_component(index)) for index in range(self.__thread_num)]
        # tasks = [asyncio.sleep(index) for index in range(self.__thread_num)]
        # for task in tasks:
        #     asyncio.run_coroutine_threadsafe(task, self.__event_loop)


    def thread_running_fun(self, print_resource: bool = False):
        if print_resource is True:
            print(f"Time: {datetime.now()} - This is Thread code - PID: {os.getpid()}. Thread: {currentThread().getName()}. \n {self.print_resource()}")
        else:
            print(f"Time: {datetime.now()} - This is Thread code - PID: {os.getpid()}. Thread: {currentThread().getName()}.")


    def greenlet_running_fun(self, print_resource: bool = False):
        if print_resource is True:
            print(f"This is Greenlet code - PID: {os.getppid()}. \n {self.print_resource()} ")
        else:
            print(f"This is Greenlet code - PID: {os.getppid()}. Greenlet: {get_current_greenlet()}. Greenlet ID: {id(get_current_greenlet())}.")


    def print_resource(self):
        cpu_percent = psutil.cpu_percent()
        cpu_state = psutil.cpu_stats()
        vir_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        return f"+-----------------------------+\n" \
               f"PID: {os.getpid()}. PPID: {os.getppid()} \n" \
               f"CPU percent: {cpu_percent} % \n" \
               f"CPU state: {cpu_state} \n" \
               f"Virtual Memory: {vir_memory} \n" \
               f"Swap Memory: {swap_memory} \n" \
               f"+-----------------------------+ \n"


if __name__ == '__main__':

    __process_number = 2
    __thread_number = 10

    process_with_thread = MultiProcessWithThread(process_num=__process_number, thread_num=__thread_number)
    # # For main code
    process_with_thread.main()
    # # For debugging
    # process_with_thread.process_running_fun()
