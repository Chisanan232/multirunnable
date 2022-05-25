import requests
import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable import RunningMode, SimpleExecutor, async_sleep
from multirunnable.api import async_retry



class ExampleTargetFunction:

    @async_retry.bounded_function
    async def crawl_process(self, *args, **kwargs) -> int:
        response = requests.get("https://www.youtube.com")
        await async_sleep(3)
        return response.status_code


    @crawl_process.initialization
    async def initial(self):
        print("This is testing initialization")


    @crawl_process.done_handling
    async def done(self, result):
        print("This is testing done process")
        print("Get something result: ", result)


    @crawl_process.final_handling
    async def final(self):
        print("This is final process")


    @crawl_process.error_handling
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
        # # # # Generally running
        __executor.run(function=self.__example.crawl_process)

        # # # # Get result
        __result = __executor.result()
        print("Result: ", __result)



if __name__ == '__main__':

    print("This is executor client: ")
    __executor_number = 3
    o_executor = ExampleExecutor(executors=__executor_number)
    o_executor.main_run()

