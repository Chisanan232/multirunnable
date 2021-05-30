# Import package pyocean
import pathlib
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean.framework import BaseRunnableBuilder, RunnableStrategy, SimpleRunnableTask
from pyocean.parallel import ParallelBuilder, MultiProcessingStrategy, ParallelStrategy, ParallelSimpleFactory

import random
import time



class ExampleParallelFactory(ParallelSimpleFactory):

    def running_builder(self, running_strategy: ParallelStrategy) -> BaseRunnableBuilder:
        return ParallelBuilder(running_strategy=running_strategy)



class ExampleParallelClient:

    def target_function(self, index):
        print(f"This is 'target_function'. Parameter is index: {index}")
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        time.sleep(sleep_time)
        print("This function wake up.")
        return "Return Value"



class ExampleBuilderClient(ExampleParallelClient):

    def main_run(self):
        _builder = ParallelBuilder(running_strategy=MultiProcessingStrategy(workers_num=1))
        _builder.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        result = _builder.result
        print(f"This is final result: {result}")



class ExampleFactoryClient(ExampleParallelClient):

    def main_run(self):
        __example_factory = ExampleParallelFactory(workers_number=1)
        __task = SimpleRunnableTask(factory=__example_factory)
        __directory = __task.generate()
        result = __directory.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        print(f"This is final result: {result}")



if __name__ == '__main__':

    print("This is builder client: ")
    __builder = ExampleBuilderClient()
    __builder.main_run()

    print("This is factory client: ")
    __factory = ExampleFactoryClient()
    __factory.main_run()
