# Import package pyocean
import pathlib
import random
import time
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from multirunnable import OceanSystem, RunningMode
from multirunnable.api import EventOperator
from multirunnable.adapter import Event



class WakeupProcess:

    __event_opt = EventOperator()

    def wake_other_process(self, *args):
        print("[WakeupProcess] args: ", args)
        print(f"[WakeupProcess] It will keep producing something useless message.")
        while True:
            __sleep_time = random.randrange(1, 10)
            print(f"[WakeupProcess] It will sleep for {__sleep_time} seconds.")
            time.sleep(__sleep_time)
            self.__event_opt.set()



class SleepProcess:

    __event_opt = EventOperator()

    def go_sleep(self, *args):
        print("[SleepProcess] args: ", args)
        print(f"[SleepProcess] It detects the message which be produced by ProducerThread.")
        while True:
            time.sleep(1)
            print("[SleepProcess] ConsumerThread waiting ...")
            self.__event_opt.wait()
            print("[SleepProcess] ConsumerThread wait up.")
            self.__event_opt.clear()



class ExampleOceanSystem:

    __Process_Number = 1

    __wakeup_p = WakeupProcess()
    __sleep_p = SleepProcess()

    @classmethod
    def main_run(cls):
        # Initialize Event object
        __event = Event()

        # Initialize and run ocean-system
        __system = OceanSystem(mode=RunningMode.Concurrent, worker_num=cls.__Process_Number)
        __system.map_by_functions(
            functions=[cls.__wakeup_p.wake_other_process, cls.__sleep_p.go_sleep],
            features=__event)



if __name__ == '__main__':

    print("[MainProcess] This is system client: ")
    system = ExampleOceanSystem()
    system.main_run()
    print("[MainProcess] Finish. ")

