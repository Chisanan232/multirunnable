import random
import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable import SimpleExecutor, RunningMode, QueueTask, sleep, async_sleep
from multirunnable.api import ConditionOperator, ConditionAsyncOperator, QueueOperator
from multirunnable.factory import ConditionFactory
from multirunnable.parallel import Queue as Process_Queue
from multirunnable.concurrent import Thread_Queue
from multirunnable.coroutine import Greenlet_Queue, Async_Queue


glist = []


class ProducerProcess:

    __Queue_Name = "test_queue"

    def __init__(self):
        self.__condition_opt = ConditionOperator()
        self.__async_condition_opt = ConditionAsyncOperator()
        self.__queue_opt = QueueOperator()


    def send_process(self, *args):
        print("[Producer] args: ", args)
        # test_queue = self.__queue_opt.get_queue_with_name(name=self.__Queue_Name)
        print(f"[Producer] It will keep producing something useless message.")
        while True:
            __sleep_time = random.randrange(1, 10)
            print(f"[Producer] It will sleep for {__sleep_time} seconds.")
            # test_queue.put(__sleep_time)
            glist.append(__sleep_time)
            sleep(__sleep_time)
            # # # # # 1. Method
            # self.__condition_opt.acquire()
            # self.__condition_opt.notify_all()
            # self.__condition_opt.release()

            # # # # # 2. Method
            __condition = self.__condition_opt
            with __condition:
                self.__condition_opt.notify_all()


    async def async_send_process(self, *args):
        print("[Producer] args: ", args)
        test_queue = self.__queue_opt.get_queue_with_name(name=self.__Queue_Name)
        print(f"[Producer] It will keep producing something useless message.")
        while True:
            # # Method 1
            # __sleep_time = random.randrange(1, 10)
            # print(f"[Producer] It will sleep for {__sleep_time} seconds.")
            # await test_queue.put(__sleep_time)
            # await asyncio.sleep(__sleep_time)
            # __condition = self.__async_condition_opt
            # await __condition.acquire()
            # __condition.notify_all()
            # __condition.release()

            # # Method 2
            __sleep_time = random.randrange(1, 10)
            print(f"[Producer] It will sleep for {__sleep_time} seconds.")
            await test_queue.put(__sleep_time)
            await async_sleep(__sleep_time)
            __condition = self.__async_condition_opt
            async with __condition:
                self.__condition_opt.notify_all()



class ConsumerProcess:

    __Queue_Name = "test_queue"

    def __init__(self):
        self.__condition_opt = ConditionOperator()
        self.__async_condition_opt = ConditionAsyncOperator()
        self.__queue_opt = QueueOperator()


    def receive_process(self, *args):
        print("[Consumer] args: ", args)
        # test_queue = self.__queue_opt.get_queue_with_name(name=self.__Queue_Name)
        print(f"[Consumer] It detects the message which be produced by ProducerThread.")
        while True:
            # # # # 1. Method
            # self.__condition_opt.acquire()
            # time.sleep(1)
            # print("[Consumer] ConsumerThread waiting ...")
            # self.__condition_opt.wait()
            # __sleep_time = test_queue.get()
            # print("[Consumer] ConsumerThread re-start.")
            # print(f"[Consumer] ProducerThread sleep {__sleep_time} seconds.")
            # self.__condition_opt.release()

            # # # # 2. Method
            __condition = self.__condition_opt
            with __condition:
                sleep(1)
                print("[Consumer] ConsumerThread waiting ...")
                self.__condition_opt.wait()
                # __sleep_time = test_queue.get()
                __sleep_time = glist[-1]
                print("[Consumer] ConsumerThread re-start.")
                print(f"[Consumer] ProducerThread sleep {__sleep_time} seconds.")


    async def async_receive_process(self, *args):
        print("[Consumer] args: ", args)
        test_queue = self.__queue_opt.get_queue_with_name(name=self.__Queue_Name)
        print(f"[Consumer] It detects the message which be produced by ProducerThread.")
        while True:
            __condition = self.__async_condition_opt
            # # Method 1
            # await __condition.acquire()
            # await asyncio.sleep(1)
            # print("[Consumer] ConsumerThread waiting ...")
            # await __condition.wait()
            # __sleep_time = await test_queue.get()
            # print("[Consumer] ConsumerThread re-start.")
            # print(f"[Consumer] ProducerThread sleep {__sleep_time} seconds.")
            # __condition.release()

            # # Method 2
            async with __condition:
                await async_sleep(1)
                print("[Consumer] ConsumerThread waiting ...")
                await __condition.wait()
                __sleep_time = await test_queue.get()
                print("[Consumer] ConsumerThread re-start.")
                print(f"[Consumer] ProducerThread sleep {__sleep_time} seconds.")



class ExampleExecutor:

    __Executor_Number = 1

    __producer_p = ProducerProcess()
    __consumer_p = ConsumerProcess()

    @classmethod
    def main_run(cls):
        # Initialize Condition object
        __condition = ConditionFactory()

        # Initialize Queue object
        # __task = QueueTask()
        # __task.name = "test_queue"
        # # __task.queue_type =Process_Queue()
        # __task.queue_type = Thread_Queue()
        # # __task.queue_type = Async_Queue()
        # __task.value = []

        # Initialize and run ocean-simple-executor
        # __exe = SimpleExecutor(mode=RunningMode.Parallel, executors=cls.__Executor_Number)
        __exe = SimpleExecutor(mode=RunningMode.Concurrent, executors=cls.__Executor_Number)
        # __exe = SimpleExecutor(mode=RunningMode.GreenThread, executors=cls.__Executor_Number)
        # __exe = SimpleExecutor(mode=RunningMode.Asynchronous, executors=cls.__Executor_Number)

        # # # # Run without arguments
        __exe.map_with_function(
            functions=[cls.__producer_p.send_process, cls.__consumer_p.receive_process],
            # queue_tasks=__task,
            features=__condition)

        # # # # Asynchronous version of running without arguments
        # __exe.map_with_function(
        #     functions=[cls.__producer_p.async_send_process, cls.__consumer_p.async_receive_process],
        #     queue_tasks=__task,
        #     features=__condition)



if __name__ == '__main__':

    print("[MainProcess] This is system client: ")
    system = ExampleExecutor()
    system.main_run()
    print("[MainProcess] Finish. ")

