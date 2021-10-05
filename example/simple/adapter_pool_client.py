import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable import RunningMode, sleep
from multirunnable.pool import AdapterPool
from multirunnable.parallel import ProcessPoolStrategy
from multirunnable.concurrent import ThreadPoolStrategy
from multirunnable.coroutine import GreenThreadPoolStrategy



class ExampleTargetFunction:

    def target_function(self, *args, **kwargs) -> str:
        print("This is ExampleTargetFunction.target_function.")
        sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        # raise Exception("Test for error")
        return "You are 87."



class ExampleAdapterPool:

    __Executor_Number = 0

    __Example_Target = ExampleTargetFunction()

    def __init__(self, executors: int):
        self.__Executor_Number = executors


    def main_run(self):
        # # # # Initial Executor object
        __pool = AdapterPool(strategy=ProcessPoolStrategy(pool_size=self.__Executor_Number, tasks_size=self.__Executor_Number))
        # __pool = AdapterPool(strategy=ThreadPoolStrategy(pool_size=self.__Executor_Number, tasks_size=self.__Executor_Number))
        # __pool = AdapterPool(strategy=GreenThreadPoolStrategy(pool_size=self.__Executor_Number, tasks_size=self.__Executor_Number))

        __result = None
        with __pool as pool:
            # # # # Running Pool
            # pool.apply(function=self.__Example_Target.target_function, index=f"test_{random.randrange(10,20)}")
            # pool.async_apply(function=self.__Example_Target.target_function, kwargs={"index": f"test_{random.randrange(10,20)}"})
            pool.map(function=self.__Example_Target.target_function, args_iter=("index_1", "index_2.2", "index_3"))
            # pool.map_by_args(function=self.__Example_Target.target_function, args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

            # # # # Get result
            __result = pool.get_result()

        print("Result: ", __result)



if __name__ == '__main__':

    print("This is pool client: ")
    __executor_number = 3
    o_executor = ExampleAdapterPool(executors=__executor_number)
    o_executor.main_run()

