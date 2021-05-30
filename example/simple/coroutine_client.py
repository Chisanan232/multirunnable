# Import package pyocean
import pathlib
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean.framework import BaseRunnableBuilder, RunnableStrategy, SimpleRunnableTask
from pyocean.coroutine import (GeventBuilder, GeventStrategy, GeventSimpleFactory,
                               AsynchronousBuilder, AsynchronousStrategy, AsynchronousSimpleFactory)
from pyocean.coroutine.strategy import CoroutineStrategy

import random
import time



class ExampleGeventFactory(GeventSimpleFactory):

    def running_builder(self, running_strategy: CoroutineStrategy) -> BaseRunnableBuilder:
        return GeventBuilder(running_strategy=running_strategy)



class ExampleAsyncFactory(AsynchronousSimpleFactory):

    def running_builder(self, running_strategy: CoroutineStrategy) -> BaseRunnableBuilder:
        return AsynchronousBuilder(running_strategy=running_strategy)



class ExampleCoroutineClient:

    def target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        time.sleep(sleep_time)
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
        _builder = GeventBuilder(running_strategy=GeventStrategy(workers_num=1))
        _builder.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        # result = _builder.result
        # print(f"This is final result: {result}")


    def main_run_with_async(self):
        _builder = AsynchronousBuilder(running_strategy=AsynchronousStrategy(workers_num=1))
        _builder.run(function=self.async_target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        # result = _builder.result
        # print(f"This is final result: {result}")



class ExampleFactoryClient(ExampleCoroutineClient):

    def main_run_with_gevent(self):
        __example_factory = ExampleGeventFactory(workers_number=1)
        __task = SimpleRunnableTask(factory=__example_factory)
        __directory = __task.generate()
        result = __directory.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        print(f"This is final result: {result}")


    def main_run_with_async(self):
        __example_factory = ExampleAsyncFactory(workers_number=1)
        __task = SimpleRunnableTask(factory=__example_factory)
        __directory = __task.generate()
        result = __directory.run(function=self.async_target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        print(f"This is final result: {result}")



if __name__ == '__main__':

    print("This is builder client: ")
    __builder = ExampleBuilderClient()
    # print("+++++++++++++ Gevent part +++++++++++++")
    # __builder.main_run_with_gevent()
    print("+++++++++++++ Async part +++++++++++++")
    # __builder.main_run_with_async()

    print("This is factory client: ")
    __factory = ExampleFactoryClient()
    # print("+++++++++++++ Gevent part +++++++++++++")
    # __factory.main_run_with_gevent()
    print("+++++++++++++ Async part +++++++++++++")
    __factory.main_run_with_async()
