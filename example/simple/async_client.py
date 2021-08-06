# Import package pyocean
from typing import List
import pathlib
import asyncio
import random
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean import OceanSystem, OceanTask, RunningMode
from pyocean.coroutine import AsynchronousResult



class ExampleCoroutineClient:

    async def async_target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        # time.sleep(sleep_time)
        await asyncio.sleep(sleep_time)
        print("This function wake up.")
        return "Return Async Value"



class ExampleOceanSystem:

    __Async_Number = 5

    __example = ExampleCoroutineClient()

    @classmethod
    def main_run(cls):
        __task = OceanTask(mode=RunningMode.Asynchronous)
        __task.set_function(function=cls.__example.async_target_function)
        __task.set_func_kwargs(kwargs={"index": f"test_{random.randrange(10,20)}"})

        __system = OceanSystem(mode=RunningMode.Asynchronous, worker_num=cls.__Async_Number)
        result: List[AsynchronousResult] = __system.run(task=__task, saving_mode=True)
        print("Async result: ", result)
        for r in result:
            print(f"+============ {r.worker_id} =============+")
            print("Result.pid: ", r.pid)
            print("Result.worker_id: ", r.worker_id)
            print("Result.state: ", r.state)
            print("Result.event_loop: ", r.event_loop)
            print("Result.data: ", r.data)
            print("Result.exception: ", r.exception)
            print("+====================================+\n")



if __name__ == '__main__':

    print("This is system client: ")
    system = ExampleOceanSystem()
    system.main_run()
