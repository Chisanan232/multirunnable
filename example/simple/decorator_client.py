# Import package pyocean
import pathlib
import random
import time
import sys

import gevent
import asyncio

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean import RunningMode
import pyocean
import time



@pyocean.multi_processes(processes=2)
def target_function_with_parallel(*args, **kwargs) -> str:
    print("This is ExampleParallelClient.target_function in process.")
    time.sleep(3)
    print("This is target function args: ", args)
    print("This is target function kwargs: ", kwargs)
    # raise Exception("Test for error")
    return "You are 87."


@pyocean.multi_threads(threads=2)
def target_function_with_concurrent(*args, **kwargs) -> str:
    print("This is ExampleParallelClient.target_function in process.")
    time.sleep(3)
    print("This is target function args: ", args)
    print("This is target function kwargs: ", kwargs)
    # raise Exception("Test for error")
    return "You are 87."


@pyocean.multi_green_threads(gthreads=2)
def target_function_with_green_thread(*args, **kwargs) -> str:
    print("This is ExampleParallelClient.target_function in process.")
    gevent.sleep(3)
    print("This is target function args: ", args)
    print("This is target function kwargs: ", kwargs)
    # raise Exception("Test for error")
    return "You are 87."


# @pyocean.multi_executors(mode=RunningMode.Parallel, executors=5)
# @pyocean.multi_executors(mode=RunningMode.Concurrent, executors=5)
@pyocean.multi_executors(mode=RunningMode.GreenThread, executors=5)
def target_function_with_ex_decorator(*args, **kwargs) -> str:
    print("This is ExampleParallelClient.target_function in process.")
    # time.sleep(3)
    gevent.sleep(3)
    print("This is target function args: ", args)
    print("This is target function kwargs: ", kwargs)
    # raise Exception("Test for error")
    return "You are 87."


@pyocean.multi_executors(mode=RunningMode.Asynchronous, executors=5)
async def async_target_function_with_ex_decorator(*args, **kwargs) -> str:
    print("This is ExampleParallelClient.target_function in process.")
    await asyncio.sleep(3)
    print("This is target function args: ", args)
    print("This is target function kwargs: ", kwargs)
    # raise Exception("Test for error")
    return "You are 87."



if __name__ == '__main__':

    print("This is client with decorator: ")
    # target_function_with_parallel("test_1")
    # target_function_with_concurrent(1, 2, 3)
    # target_function_with_green_thread("1", 3)
    # result = target_function_with_ex_decorator(1, 2, 3, 4, 5, ["l_1", "l_2", "l_3"])
    result = async_target_function_with_ex_decorator(1, 2, 3, 4, 5, ["l_1", "l_2", "l_3"])
    print("Result: ", result)
