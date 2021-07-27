# Import package pyocean
import pathlib
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean import GeventProcedure
from pyocean.worker import OceanSystem, OceanTask
from pyocean.api.mode import RunningMode
from pyocean.framework import SimpleRunnableTask
from pyocean.coroutine import GeventProcedure, MultiGreenletStrategy, GeventSimpleFactory

import gevent
import random
import time



class ExampleCoroutineClient:

    def target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        # time.sleep(sleep_time)
        gevent.sleep(sleep_time)
        print("This function wake up.")
        # return "Return Value"


    async def async_target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        time.sleep(sleep_time)
        print("This function wake up.")
        # return "Return Value"



class ExampleBuilderClient(ExampleCoroutineClient):

    def main_run_with_gevent(self):
        _builder = GeventProcedure(running_strategy=MultiGreenletStrategy(workers_num=1))
        _builder.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        # result = _builder.result
        # print(f"This is final result: {result}")



class ExampleFactoryClient(ExampleCoroutineClient):

    def main_run_with_gevent(self):
        __example_factory = GeventSimpleFactory(workers_number=3)
        __task = SimpleRunnableTask(factory=__example_factory)
        __directory = __task.generate()
        result = __directory.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        print(f"This is final result: {result}")



class ExampleOceanSystem:

    __Greenlet_Number = 4

    __example = ExampleCoroutineClient()

    @classmethod
    def main_run(cls):
        __task = OceanTask(mode=RunningMode.Greenlet)
        __task.set_function(function=cls.__example.target_function)\
            .set_func_kwargs(kwargs={"index": f"test_{random.randrange(10,20)}"})

        __system = OceanSystem(mode=RunningMode.Greenlet, worker_num=cls.__Greenlet_Number)
        __system.run(task=__task)



if __name__ == '__main__':

    # print("This is builder client: ")
    # __builder = ExampleBuilderClient()
    # __builder.main_run_with_gevent()

    # print("This is factory client: ")
    # __factory = ExampleFactoryClient()
    # print("+++++++++++++ Gevent part +++++++++++++")
    # __factory.main_run_with_gevent()

    print("This is system client: ")
    system = ExampleOceanSystem()
    system.main_run()
