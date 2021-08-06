# Import package pyocean
from typing import List
import pathlib
import gevent
import random
import time
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean import OceanSystem, OceanTask, RunningMode
from pyocean.coroutine import CoroutineResult



class ExampleCoroutineClient:

    def target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        # time.sleep(sleep_time)
        gevent.sleep(sleep_time)
        print("This function wake up.")
        return "Coroutine Return Value"


    async def async_target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        time.sleep(sleep_time)
        print("This function wake up.")
        # return "Return Value"



class ExampleOceanSystem:

    __Greenlet_Number = 4

    __example = ExampleCoroutineClient()

    @classmethod
    def main_run(cls):
        __task = OceanTask(mode=RunningMode.Greenlet)
        __task.set_function(function=cls.__example.target_function)\
            .set_func_kwargs(kwargs={"index": f"test_{random.randrange(10,20)}"})

        __system = OceanSystem(mode=RunningMode.Greenlet, worker_num=cls.__Greenlet_Number)
        result: List[CoroutineResult] = __system.run(task=__task)
        print("Coroutine result: ", result)
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
