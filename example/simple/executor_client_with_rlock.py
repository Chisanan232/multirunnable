import time
import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable import RunningMode, SimpleExecutor, sleep
from multirunnable.api import RLockOperator
from multirunnable.factory import RLockFactory



class ExampleTargetFunction:

    __rlock = RLockOperator()

    def target_function(self, *args, **kwargs) -> str:
        print("This is ExampleTargetFunction.target_function.")
        sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        sleep(2)
        self.__rlock.acquire()
        print("Lock Acquire 1 time")
        sleep(2)
        self.__rlock.acquire()
        print("Lock Acquire 2 time")
        sleep(2)
        self.__rlock.release()
        print("Lock Release 1 time")
        sleep(2)
        self.__rlock.release()
        print("Lock Release 2 time")
        return "You are 87."



class ExampleExecutor:

    __Executor_Number = 0

    __example = ExampleTargetFunction()

    def __init__(self, executors: int):
        self.__Executor_Number = executors


    def main_run(self):
        # Initialize Lock object
        __rlock = RLockFactory()

        # # # # Initial Executor object
        __executor = SimpleExecutor(mode=RunningMode.Parallel, executors=self.__Executor_Number)
        # __executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=self.__Executor_Number)
        # __executor = SimpleExecutor(mode=RunningMode.GreenThread, executors=self.__Executor_Number)

        # # # # Running the Executor
        # # # # Generally running
        __executor.run(
            function=self.__example.target_function,
            args=("index_1", "index_2.2"),
            features=__rlock)

        # # # # Map running which will raise exception
        # __executor.map(
        #     function=self.__example.target_function,
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)],
        #     features=__rlock)

        # # # # Function version of map running which will raise exception
        # __executor.map_with_function(
        #     functions=[self.__example.target_function, self.__example.target_function],
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)],
        #     features=__rlock)

        # # # # Get result
        __result = __executor.result()
        print("Result: ", __result)



if __name__ == '__main__':

    print("This is executor client: ")
    __executor_number = 3
    o_executor = ExampleExecutor(executors=__executor_number)
    o_executor.main_run()

