import requests
import random
import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable import RunningMode, SimplePool, sleep, async_sleep



class ExampleTargetFunction:

    def crawl_function(self, *args, **kwargs) -> int:
        response = requests.get("https://www.youtube.com")
        return response.status_code



class ExamplePool:

    __Pool_Size = None
    __Task_Size = None
    __Example_Target = ExampleTargetFunction()

    def __init__(self, pool_size, task_size):
        self.__Pool_Size = pool_size
        self.__Task_Size = task_size


    def main_run(self):
        # # # # Initial Pool object
        __pool = SimplePool(mode=RunningMode.Parallel, pool_size=self.__Pool_Size)
        # __pool = SimplePool(mode=RunningMode.Concurrent, pool_size=self.__Pool_Size)
        # __pool = SimplePool(mode=RunningMode.GreenThread, pool_size=self.__Pool_Size)

        __result = None
        with __pool as pool:
            # # # # Running Pool
            # pool.apply(function=self.__Example_Target.target_function, tasks_size=self.__Pool_Size)
            pool.async_apply(function=self.__Example_Target.crawl_function, kwargs={"sleep_time": random.randrange(10, 20)}, tasks_size=self.__Pool_Size)
            pool.map(function=self.__Example_Target.crawl_function, args_iter=(1, 2, 3))
            # pool.map_by_args(function=self.__Example_Target.target_function, args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

            # # # # Get result
            __result = pool.get_result()

        print("Result: ", __result)



if __name__ == '__main__':

    print("This is system client: ")
    o_pool = ExamplePool(pool_size=3, task_size=10)
    o_pool.main_run()

