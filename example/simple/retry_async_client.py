import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable.api import async_retry
import asyncio
import time


@async_retry.function
# @async_retry.function(timeout=3)
async def target_fail_function_with_default(*args, **kwargs) -> None:
    print("This is ExampleParallelClient.target_fail_function_with_default.")
    print("This is target function args: ", args)
    print("This is target function kwargs: ", kwargs)
    print("It will raise exception after 3 seconds ...")
    time.sleep(3)
    raise Exception("Test for error in 'target_fail_function_with_default'")


# @async_retry.function
@async_retry.function(timeout=3)
async def target_fail_function(*args, **kwargs) -> None:
    print("This is ExampleParallelClient.target_function.")
    print("This is target function args: ", args)
    print("This is target function kwargs: ", kwargs)
    print("It will raise exception after 3 seconds ...")
    time.sleep(3)
    raise Exception("Test for error")


@target_fail_function.initialization
async def initial(*args, **kwargs):
    print("This is testing initialization of target_fail_function")
    print(f"This is testing initialization args of target_fail_function: {args}")
    print(f"This is testing initialization kwargs of target_fail_function: {kwargs}")


@target_fail_function.done_handling
async def done(result):
    print("This is testing done process of target_fail_function")
    print("Get something result of target_fail_function: ", result)


@target_fail_function.final_handling
async def final():
    # print(f"This is final process and result: {result}")
    print(f"This is final process and result of target_fail_function")


@target_fail_function.error_handling
async def error(*args):
    print("This is error process of target_fail_function")
    print("Get something error of target_fail_function: ", args)



class AsyncRetryTest:

    @async_retry.bounded_function
    async def bounded_func_with_default(self, *args, **kwargs):
        print(f"[INFO] This is bounded function 'bounded_func_with_default' args: {args}")
        await self.another(param_1="index_1", param_2="index_2")
        raise Exception("Test for error in 'bounded_func_with_default'")


    @async_retry.bounded_function(timeout=3)
    async def bounded_func(self, *args, **kwargs):
        print(f"[INFO] This is bounded function args: {args}")
        await self.another(param_1="index_1", param_2="index_2")
        raise Exception("Test for error")


    async def another(self, *args, **kwargs):
        print("[DEBUG] This is another method.")
        print(f"[DEBUG] This is another arg: {args}")
        print(f"[DEBUG] This is another kwargs: {kwargs}")


    @bounded_func.error_handling
    async def _bounded_error(self, *args):
        print("This is error process of bounded_func")
        print("Get something error of bounded_func: ", args)


    # @async_retry.bounded_function(timeout=3)
    # @async_retry.function(timeout=3)
    # @classmethod
    # async def classmethod_func(cls, *args, **kwargs):
    #     print(f"[INFO] This is classmethod function args: {args}")
    #     raise Exception("Test for error of classmethod_func")
    #
    #
    # @classmethod_func.error_handling
    # @classmethod
    # async def _classmethod_error(cls, *args):
    #     print("This is error process of classmethod_func")
    #     print("Get something error of classmethod_func: ", args)


    # @async_retry.bounded_function(timeout=3)
    # @staticmethod
    # async def staticmethod_func(*args, **kwargs):
    #     print(f"[INFO] This is staticmethod function args: {args}")
    #     raise Exception("Test for error of staticmethod_func")
    #
    #
    # @staticmethod_func.error_handling
    # @staticmethod
    # async def _staticmethod_error(*args):
    #     print("This is error process of staticmethod_func")
    #     print("Get something error of staticmethod_func: ", args)


async def test_func():
    await target_fail_function()


if __name__ == '__main__':

    print("This is executor client: ")
    try:
        asyncio.run(target_fail_function_with_default())
    except Exception as e:
        print(f"[INFO in main] Got an exception: {e}")
    asyncio.run(target_fail_function())
    asyncio.run(test_func())

    _rt = AsyncRetryTest()
    try:
        asyncio.run(_rt.bounded_func_with_default())
    except Exception as e:
        print(f"[INFO in main] Got an exception: {e}")
    asyncio.run(_rt.bounded_func())

    # asyncio.run(AsyncRetryTest.classmethod_func())

    # asyncio.run(AsyncRetryTest.staticmethod_func())

