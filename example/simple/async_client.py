# Import package pyocean
import pathlib
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean import AsynchronousProcedure
from pyocean.framework import BaseRunnableProcedure, RunnableStrategy, SimpleRunnableTask
from pyocean.coroutine import AsynchronousStrategy, AsynchronousSimpleFactory
from pyocean.coroutine.strategy import CoroutineStrategy

import random
import time



class ExampleCoroutineClient:

    async def async_target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        time.sleep(sleep_time)
        print("This function wake up.")
        # return "Return Value"



class ExampleBuilderClient(ExampleCoroutineClient):

    def main_run_with_async(self):
        _builder = AsynchronousProcedure(running_strategy=AsynchronousStrategy(workers_num=1))
        _builder.run(function=self.async_target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        # result = _builder.result
        # print(f"This is final result: {result}")



class ExampleFactoryClient(ExampleCoroutineClient):

    def main_run_with_async(self):
        __example_factory = AsynchronousSimpleFactory(workers_number=1)
        __task = SimpleRunnableTask(factory=__example_factory)
        __directory = __task.generate()
        result = __directory.run(function=self.async_target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        print(f"This is final result: {result}")



if __name__ == '__main__':

    print("This is builder client: ")
    __builder = ExampleBuilderClient()
    __builder.main_run_with_async()

    print("This is factory client: ")
    __factory = ExampleFactoryClient()
    # __factory.main_run_with_async()
