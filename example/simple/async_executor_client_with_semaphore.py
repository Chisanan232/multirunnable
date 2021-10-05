import time
import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
    sys.path.append(package_path)

# multirunnable package
from multirunnable import RunningMode, SimpleExecutor, async_sleep
from multirunnable.api import async_retry, AsyncRunWith
from multirunnable.adapter import Semaphore



class ExampleAsyncTargetFunction:

    async def async_target_function(self, *args, **kwargs) -> str:
        print("This is ExampleTargetFunction.async_target_function.")
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        # await async_sleep(3)
        await self.lock_function()
        # raise Exception("Test for error")
        return "You are 87."


    @async_retry
    @AsyncRunWith.Semaphore
    async def lock_function(self):
        print("This is testing process with Lock and sleep for 3 seconds.")
        await async_sleep(3)
        print("Wake up and raise an exception ...")
        raise RuntimeError("Test for error")


    @lock_function.initialization
    async def initial(self):
        print("This is testing initialization")


    @lock_function.done_handling
    async def done(self, result):
        print("This is testing done process")
        print("Get something result: ", result)


    @lock_function.final_handling
    async def final(self):
        print("This is final process")


    @lock_function.error_handling
    async def error(self, error):
        print("This is error process")
        print("Get something error: ", error)



class ExampleExecutor:

    __Executor_Number = 0

    __async_example = ExampleAsyncTargetFunction()

    def __init__(self, executors: int):
        self.__Executor_Number = executors


    def main_run(self):
        # Initialize Lock object
        __semaphore = Semaphore(value=2)

        # # # # Initial Executor object
        __executor = SimpleExecutor(mode=RunningMode.Asynchronous, executors=self.__Executor_Number)

        # # # # Running the Executor
        # # # # Asynchronous version of generally running
        __executor.run(
            function=self.__async_example.async_target_function,
            args=("index_1", "index_2.2"),
            features=__semaphore)

        # # # # Asynchronous version of generally running which will raise exception
        # __executor.run(
        #     function=self.__async_example.async_target_function,
        #     args=("index_1", "index_2.2"),
        #     features=__semaphore)

        # # # # Asynchronous version of map running which will raise exception
        # __executor.map(
        #     function=self.__async_example.async_target_function,
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)],
        #     features=__semaphore)

        # # # # Asynchronous version of function version of map running which will raise exception
        # __executor.map_with_function(
        #     functions=[self.__async_example.async_target_function, self.__async_example.async_target_function],
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)],
        #     features=__semaphore)

        # # # # Get result
        __result = __executor.result()
        print("Result: ", __result)



if __name__ == '__main__':

    print("This is executor client: ")
    __executor_number = 3
    o_executor = ExampleExecutor(executors=__executor_number)
    o_executor.main_run()

