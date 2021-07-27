# Import package pyocean
import pathlib
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean.worker import OceanTask, OceanWorker, OceanSystem
from pyocean.api.mode import RunningMode
from pyocean.framework import SimpleRunnableTask
from pyocean.concurrent import ConcurrentProcedure, MultiThreadingStrategy, ConcurrentSimpleFactory

import random
import time



class ExampleConcurrentClient:

    def target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        time.sleep(sleep_time)
        print("This function wake up.")
        return "Return Value"



class ExampleBuilderClient(ExampleConcurrentClient):

    def main_run(self):
        _builder = ConcurrentProcedure(running_strategy=MultiThreadingStrategy(workers_num=2))
        _builder.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        # result = _builder.result
        # print(f"This is final result: {result}")



class ExampleFactoryClient(ExampleConcurrentClient):

    def main_run(self):
        __example_factory = ConcurrentSimpleFactory(workers_number=2)
        __task = SimpleRunnableTask(factory=__example_factory)
        __directory = __task.generate()
        result = __directory.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        print(f"This is final result: {result}")



class ExampleOceanSystem:

    __Thread_Number = 5

    __example = ExampleConcurrentClient()

    @classmethod
    def main_run(cls):
        # Initialize task object
        __task = OceanTask(mode=RunningMode.Concurrent)
        __task.set_function(function=cls.__example.target_function)\
            .set_func_kwargs(kwargs={"index": f"test_{random.randrange(10,20)}"})

        # Initialize ocean-system and assign task
        __system = OceanSystem(mode=RunningMode.Concurrent, worker_num=cls.__Thread_Number)
        __system.run(task=__task)



if __name__ == '__main__':

    # print("This is builder client: ")
    # __builder = ExampleBuilderClient()
    # __builder.main_run()

    # print("This is factory client: ")
    # __factory = ExampleFactoryClient()
    # __factory.main_run()

    print("This is system client: ")
    system = ExampleOceanSystem()
    system.main_run()
