import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable import RunningMode, SimpleExecutor
from multirunnable.api import async_retry
import multirunnable



class ExampleTargetFunction:

    async def async_target_function(self, *args, **kwargs) -> str:
        print("This is ExampleTargetFunction.async_target_function.")
        await multirunnable.async_sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        # raise Exception("Test for error")
        return "You are 87."


    @multirunnable.asynchronize
    def target_function(self, *args, **kwargs) -> str:
        """
        Comment:
            The feature 'multirunnable.asynchronize' still be under test.
        :param args:
        :param kwargs:
        :return:
        """
        print("This is ExampleTargetFunction.async_target_function.")
        await multirunnable.async_sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        # raise Exception("Test for error")
        return "You are 87."


    @async_retry
    async def async_target_fail_function(self, *args, **kwargs) -> None:
        print("This is ExampleParallelClient.target_function.")
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        print("It will raise exception after 3 seconds ...")
        await multirunnable.async_sleep(3)
        raise Exception("Test for error")


    @async_target_fail_function.initialization
    async def initial(self):
        print("This is testing initialization")


    @async_target_fail_function.done_handling
    async def done(self, result):
        print("This is testing done process")
        print("Get something result: ", result)


    @async_target_fail_function.final_handling
    async def final(self):
        print("This is final process")


    @async_target_fail_function.error_handling
    async def error(self, error):
        print("This is error process")
        print("Get something error: ", error)



class ExampleExecutor:

    __Executor_Number = 0

    __example = ExampleTargetFunction()

    def __init__(self, executors: int):
        self.__Executor_Number = executors


    def main_run(self):
        # # # # Initial Executor object
        __executor = SimpleExecutor(mode=RunningMode.Asynchronous, executors=self.__Executor_Number)

        # # # # Running the Executor
        # # # # Asynchronous version of generally running
        __executor.run(
            function=self.__example.async_target_function,
            # function=self.__example.target_function,
            args=("index_1", "index_2.2"))

        # # # # Asynchronous version of generally running which will raise exception
        # __executor.run(
        #     function=self.__example.async_target_fail_function,
        #     args=("index_1", "index_2.2"))

        # # # # Map running which will raise exception
        # __executor.map(
        #     function=self.__example.async_target_function,
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

        # # # # Function version of map running which will raise exception
        # __executor.map_with_function(
        #     functions=[self.__example.async_target_function, self.__example.async_target_function],
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

        # # # # Get result
        __result = __executor.result()
        print("Result: ", __result)



if __name__ == '__main__':

    print("This is executor client: ")
    __executor_number = 3
    o_executor = ExampleExecutor(executors=__executor_number)
    o_executor.main_run()

