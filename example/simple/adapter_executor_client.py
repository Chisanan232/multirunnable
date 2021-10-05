import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_pyocean_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_pyocean_path)

# multirunnable package
from multirunnable import RunningMode, sleep
from multirunnable.executor import AdapterExecutor
from multirunnable.parallel import ProcessStrategy
from multirunnable.concurrent import ThreadStrategy
from multirunnable.coroutine import GreenThreadStrategy, AsynchronousStrategy



class ExampleTargetFunction:

    def target_function(self, *args, **kwargs) -> str:
        print("This is ExampleTargetFunction.target_function.")
        sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        # raise Exception("Test for error")
        return "You are 87."



class ExampleAdapterExecutor:

    __Executor_Number = 0

    __example = ExampleTargetFunction()

    def __init__(self, executors: int):
        self.__Executor_Number = executors


    def main_run(self):
        # # # # Initial Executor object
        __executor = AdapterExecutor(strategy=ProcessStrategy(executors=self.__Executor_Number))
        # __executor = AdapterExecutor(strategy=ThreadStrategy(executors=self.__Executor_Number))
        # __executor = AdapterExecutor(strategy=GreenThreadStrategy(executors=self.__Executor_Number))
        # __executor = AdapterExecutor(strategy=AsynchronousStrategy(executors=self.__Executor_Number))

        # # # # Running the Executor
        # # # # Generally running
        __executor.run(
            function=self.__example.target_function,
            args=("index_1", "index_2.2"))

        # # # # Generally running which will raise exception
        # __executor.run(
        #     function=self.__example.target_fail_function,
        #     args=("index_1", "index_2.2"))

        # # # # Map running which will raise exception
        # __executor.map(
        #     function=self.__example.target_function,
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

        # # # # Function version of map running which will raise exception
        # __executor.map_with_function(
        #     functions=[self.__example.target_function, self.__example.target_function],
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

        # # # # Get result
        __result = __executor.result()
        print("Result: ", __result)



if __name__ == '__main__':

    print("This is executor client: ")
    __executor_number = 3
    o_executor = ExampleAdapterExecutor(executors=__executor_number)
    o_executor.main_run()

