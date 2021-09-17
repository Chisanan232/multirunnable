# Import package pyocean
import pathlib
import random
import time
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from multirunnable import OceanSystem, RunningMode, QueueTask
from multirunnable.api import ConditionOperator, QueueOperator
from multirunnable.adapter import Condition
from multirunnable.parallel import MultiProcessingQueueType



class ProducerProcess:

    __Queue_Name = "test_queue"

    def __init__(self):
        self.__condition_opt = ConditionOperator()
        self.__queue_opt = QueueOperator()


    def send_process(self, *args):
        print("[Producer] args: ", args)
        test_queue = self.__queue_opt.get_queue_with_name(name=self.__Queue_Name)
        print(f"[Producer] It will keep producing something useless message.")
        while True:
            __sleep_time = random.randrange(1, 10)
            print(f"[Producer] It will sleep for {__sleep_time} seconds.")
            test_queue.put(__sleep_time)
            time.sleep(__sleep_time)
            # # # # # 1. Method
            # self.__condition_opt.acquire()
            # self.__condition_opt.notify_all()
            # self.__condition_opt.release()

            # # # # # 2. Method
            __condition = self.__condition_opt
            with __condition:
                self.__condition_opt.notify_all()



class ConsumerProcess:

    __Queue_Name = "test_queue"

    def __init__(self):
        self.__condition_opt = ConditionOperator()
        self.__queue_opt = QueueOperator()


    def receive_process(self, *args):
        print("[Consumer] args: ", args)
        test_queue = self.__queue_opt.get_queue_with_name(name=self.__Queue_Name)
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
                time.sleep(1)
                print("[Consumer] ConsumerThread waiting ...")
                self.__condition_opt.wait()
                __sleep_time = test_queue.get()
                print("[Consumer] ConsumerThread re-start.")
                print(f"[Consumer] ProducerThread sleep {__sleep_time} seconds.")



class ExampleOceanSystem:

    __Process_Number = 1

    __producer_p = ProducerProcess()
    __consumer_p = ConsumerProcess()

    @classmethod
    def main_run(cls):
        # Initialize Event object
        __condition = Condition()

        # Initialize Queue object
        __task = QueueTask()
        __task.name = "test_queue"
        __task.queue_type = MultiProcessingQueueType.Queue
        __task.value = []

        # Initialize and run ocean-system
        __system = OceanSystem(mode=RunningMode.Concurrent, worker_num=cls.__Process_Number)
        __system.map_by_functions(
            functions=[cls.__producer_p.send_process, cls.__consumer_p.receive_process],
            queue_tasks=__task,
            features=__condition)



if __name__ == '__main__':

    print("[MainProcess] This is system client: ")
    system = ExampleOceanSystem()
    system.main_run()
    print("[MainProcess] Finish. ")

