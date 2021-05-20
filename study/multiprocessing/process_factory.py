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



class ProcessFactory:

    """
    Parallel
    """

    def __init__(self, process_number):
        self.__process_num = process_number


    def init(self):
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
