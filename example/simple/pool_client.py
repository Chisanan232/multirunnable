# Import package pyocean
import pathlib
import sys

import gevent

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from multirunnable import RunningMode, SimplePool



class ExampleTargetFunction:

    def target_function(self, *args, **kwargs) -> str:
        print("This is ExampleParallelClient.target_function in process.")
        # time.sleep(3)
        gevent.sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        # raise Exception("Test for error")
        return "You are 87."



class ExampleOceanPool:

    __Pool_Size = None
    __Task_Size = None
    __Example_Target = ExampleTargetFunction()

    def __init__(self, pool_size, task_size):
        self.__Pool_Size = pool_size
        self.__Task_Size = task_size


    def main_run(self):
        # # # # Initial Pool object
        __pool = SimplePool(mode=RunningMode.Parallel, pool_size=self.__Pool_Size, tasks_size=self.__Task_Size)
        # __pool = SimplePool(mode=RunningMode.Concurrent, pool_size=self.__Pool_Size, tasks_size=self.__Task_Size)
        # __pool = SimplePool(mode=RunningMode.GreenThread, pool_size=self.__Pool_Size, tasks_size=self.__Task_Size)

        # # # # Running Pool
        with __pool as pool:
            # pool.apply(function=cls.__example.target_function, index=f"test_{random.randrange(10,20)}")
            # pool.async_apply(function=cls.__example.target_function, kwargs={"index": f"test_{random.randrange(10,20)}"})
            # pool.map(function=cls.__example.target_function, args_iter=("index_1", "index_2.2", "index_3"))
            pool.map_by_args(function=self.__Example_Target.target_function, args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

        # # # # Get result
        __result = __pool.get_result()
        print("Result: ", __result)



if __name__ == '__main__':

    print("This is system client: ")
    o_pool = ExampleOceanPool(pool_size=3, task_size=10)
    o_pool.main_run()

