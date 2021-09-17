from datetime import datetime
import asyncio
import random
import os


class AsyncFactory:

    def __init__(self, thread_number, event_loop):
        self.__thread_num = thread_number
        self.__loop = event_loop


    async def run_task(self, params):
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
            done_flag = finish.close()
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
        print(f"This is task {index} - name as Async-{index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds ... - Async-{index}")
        await asyncio.sleep(sleep_time)
        if index == 7:
            # print(f"Wake up to go ahead! - Greenlet-{index}")
            raise Exception("This exception be raise for lucky number.")
        else:
            print(f"Wake up to go ahead! - Async-{index}")
            return f"Async-{index}"



class MainCode:

    def __init__(self, thread_num):
        self.__thread_num = thread_num
        self.__event_loop = asyncio.get_event_loop()
        self.__async_factory = AsyncFactory(thread_number=thread_num, event_loop=self.__event_loop)


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
            self.__event_loop.run_until_complete(future=self.__async_factory.run_task())
        except Exception as e:
            print(f"Test for catch the coroutine exception.")
            print(f"exception: {e}")

        # # Method 2.
        # tasks = [asyncio.create_task(self.__async_factory.task_component(index)) for index in range(self.__thread_num)]
        # tasks = [asyncio.sleep(index) for index in range(self.__thread_num)]
        # for task in tasks:
        #     asyncio.run_coroutine_threadsafe(task, self.__event_loop)


if __name__ == '__main__':

    __thread_number = 10

    main = MainCode(thread_num=__thread_number)
    main.process_running_fun()
