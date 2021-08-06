# Import package pyocean
from typing import List
import pathlib
import random
import time
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean import OceanTask, OceanSystem, RunningMode
from pyocean.concurrent import ConcurrentResult



class ExampleConcurrentClient:

    def target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        time.sleep(sleep_time)
        print("This function wake up.")
        return "Return Value"



class ExampleOceanSystem:

    __Thread_Number = 5

    __example = ExampleConcurrentClient()

    @classmethod
    def main_run(cls):
        # Initialize task object
        __task = OceanTask(mode=RunningMode.Concurrent)
        __task.set_function(function=cls.__example.target_function)
        __task.set_func_kwargs(kwargs={"index": f"test_{random.randrange(10,20)}"})

        # Initialize ocean-system and assign task
        __system = OceanSystem(mode=RunningMode.Concurrent, worker_num=cls.__Thread_Number)
        result: List[ConcurrentResult] = __system.run(task=__task, saving_mode=True)
        # result: List[ConcurrentResult] = __system.run(task=__task)
        print("Concurrent result: ", result)
        for r in result:
            print(f"+============ {r.worker_id} =============+")
            print("Result.pid: ", r.pid)
            print("Result.worker_id: ", r.worker_id)
            print("Result.state: ", r.state)
            print("Result.data: ", r.data)
            print("Result.exception: ", r.exception)
            print("+====================================+\n")



if __name__ == '__main__':

    print("This is system client: ")
    system = ExampleOceanSystem()
    system.main_run()
