# Import package pyocean
from typing import List
import pathlib
import random
import time
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean.framework import SimpleRunnableTask
from pyocean import ParallelProcedure, OceanSystem, OceanTask
from pyocean.api import RunningMode, ReTryMechanism
from pyocean.parallel import MultiProcessingStrategy, ParallelSimpleFactory, ParallelResult



class ExampleParallelClient:

    # def target_function(self, index):
    #     print(f"This is 'target_function'. Parameter is index: {index}")
    #     sleep_time = random.randrange(1, 10)
    #     print(f"Will sleep for {sleep_time} seconds.")
    #     time.sleep(sleep_time)
    #     print("This function wake up.")
    #     return "Return Value"


    def target_function(self, *args, **kwargs) -> str:
        print("This is ExampleParallelClient.target_function in process.")
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        # raise Exception("Test for error")
        return "You are 87."


    def target_function_with_task(self, task):
        print(f"This is 'target_function'. task is: {task}")
        print(f"task.function is: {task.function}")
        print(f"task.func_kwargs is: {task.func_kwargs}")
        task.function(**task.func_kwargs)
        sleep_time = random.randrange(1, 10)
        print(f"Will sleep for {sleep_time} seconds.")
        time.sleep(sleep_time)
        print("This function wake up.")
        return "Return Value"



class ExampleBuilderClient(ExampleParallelClient):

    def main_run(self):
        _builder = ParallelProcedure(running_strategy=MultiProcessingStrategy(workers_num=1))
        _builder.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        result = _builder.result
        print(f"This is final result: {result}")



class ExampleFactoryClient(ExampleParallelClient):

    def main_run(self):
        __example_factory = ParallelSimpleFactory(workers_number=1)
        __task = SimpleRunnableTask(factory=__example_factory)
        __directory = __task.generate()
        result = __directory.run(function=self.target_function, fun_kwargs={"index": f"test_{random.randrange(10,20)}"})
        print(f"This is final result: {result}")



class WishWorker:

    def __init__(self, worker_num: int):
        from multiprocessing import Manager

        self.worker_num = worker_num

        # # # Original
        # self.__strategy = MultiProcessingStrategy(workers_num=self.worker_num)
        global Strategy
        Strategy = MultiProcessingStrategy(workers_num=self.worker_num)

        # # # Try to fix this issue ...
        # __manager = Manager()
        # __namespace = __manager.Namespace()
        # __namespace.Running_Strategy = MultiProcessingStrategy(workers_num=self.worker_num)
        # self.__strategy = __namespace.Running_Strategy


    @ReTryMechanism.task
    def target_task_with_decorator(self, task) -> str:
        print("This is target_task_with_decorator function in process.")
        # print("This is target function task: ", task)
        # return "You are 87 task."
        return task.function(*task.func_args, **task.func_kwargs)


    def run(self, task):
        # self.__strategy.initialization()
        # # workers_list = __strategy.build_workers(function=cls.target_func_with_decorator, *__task.func_args, **__task.func_kwargs)
        # # __task.set_func_kwargs(kwargs={"task": __task})
        # # workers_list = __strategy.build_workers(function=cls.target_task_with_decorator, *__task.func_args, **__task.func_kwargs)
        # __kwargs = {"task": task}
        # workers_list = self.__strategy.build_workers(function=self.target_task_with_decorator, **__kwargs)
        # self.__strategy.activate_workers(workers_list=workers_list)
        # self.__strategy.close()

        Strategy.initialization()
        __kwargs = {"task": task}
        workers_list = Strategy.build_workers(function=self.target_task_with_decorator, **__kwargs)
        Strategy.activate_workers(workers_list=workers_list)
        Strategy.close()


    def run_without_self(self, task):
        __strategy = MultiProcessingStrategy(workers_num=self.worker_num)
        __strategy.initialization()
        # workers_list = __strategy.build_workers(function=cls.target_func_with_decorator, *__task.func_args, **__task.func_kwargs)
        # __task.set_func_kwargs(kwargs={"task": __task})
        # workers_list = __strategy.build_workers(function=cls.target_task_with_decorator, *__task.func_args, **__task.func_kwargs)
        __kwargs = {"task": task}
        workers_list = __strategy.build_workers(function=self.target_task_with_decorator, **__kwargs)
        __strategy.activate_workers(workers_list=workers_list)
        __strategy.close()



class ExampleOceanSystem:

    __Process_Number = 1

    __example = ExampleParallelClient()

    @classmethod
    def main_run(cls):
        # Initialize task object
        print("Initial task instance.")
        __task = OceanTask(mode=RunningMode.Parallel)
        __task.set_function(function=cls.__example.target_function)
        __task.set_func_kwargs(kwargs={"index": f"test_{random.randrange(10,20)}"})

        # Initialize ocean-system and assign task
        print("Initial system instance.")
        __system = OceanSystem(mode=RunningMode.Parallel, worker_num=cls.__Process_Number)
        print("Start running ...")
        result: List[ParallelResult] = __system.run(task=__task, saving_mode=True)
        # result: List[ParallelResult] = __system.run(task=__task)
        print("Parallel result: ", result)
        for r in result:
            print("Result.pid: ", r.pid)
            print("Result.worker_id: ", r.worker_id)
            print("Result.state: ", r.state)
            print("Result.data: ", r.data)
            print("Result.exception: ", r.exception)


    @ReTryMechanism.task
    def target_task_with_decorator(self, task) -> str:
        print("This is target_task_with_decorator function in process.")
        # print("This is target function task: ", task)
        # return "You are 87 task."
        return task.function(*task.func_args, **task.func_kwargs)


    @ReTryMechanism.function
    def target_func_with_decorator(self, *args, **kwargs) -> str:
        print("This is target running function in process.")
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        return "You are 87."


    @classmethod
    def main_debug(cls):

        from multiprocessing import Pool

        # __task = SharedTask()
        __task = OceanTask(mode=RunningMode.Parallel)
        __task.set_function(function=cls.__example.target_function)
        __task.set_func_args(args=())
        __task.set_func_kwargs(kwargs={"param1": 1, "param2": "this is kwargs"})

        __pool = Pool(processes=cls.__Process_Number)

        # # # # Pool.apply_async
        # __process_pool = []
        # for _ in range(self.worker_num):
        #     # __process = __pool.apply_async(func=self.target_func_with_decorator, *__fun_args, **__fun_kwargs)
        #     __process = __pool.apply_async(
        #         func=self.target_task_with_decorator,
        #         args=(), kwds={"task": task},
        #         callback=None, error_callback=None)
        #     # __process = __pool.apply_async(func=Decorator_Func, args=__fun_args, kwds=__fun_kwargs)
        #     __process_pool.append(__process)

        # for __process in __process_pool:
        #     result = __process.get()
        #     successful = __process.successful()
        #     print("Function successful: ", successful)
        #     print("Function result: ", result)

        # # # # Pool.map_async
        __task_list = [__task.func_kwargs.values() for _ in range(cls.__Process_Number)]
        print("task list: ", __task_list)
        print("task func_args: ", __task.func_args)
        print("task func_kwargs: ", __task.func_kwargs)
        # __process = __pool.map_async(cls.target_task_with_decorator, __task_list)
        __process = __pool.map_async(cls.target_func_with_decorator, __task_list)
        # __process = __pool.map_async(self.run, __task_list)
        # __process = __pool.map_async(self.test_func, {"task": task})
        # # # # Pool.starmap_async
        # __process = __pool.starmap_async(self.target_task_with_decorator, [(task, )])
        result = __process.get()
        print("Function result: ", result)

        __pool.close()
        __pool.close()


    @classmethod
    def main_wish_worker(cls):
        __task = OceanTask(mode=RunningMode.Parallel)
        __task.set_function(function=cls.__example.target_function)
        __task.set_func_args(args=())

        __worker = WishWorker(worker_num=cls.__Process_Number)
        __worker.run(task=__task)


    @classmethod
    def main_test(cls, task=None):

        # __task = OceanTask(mode=RunningMode.Parallel)
        # __task.set_function(function=cls.__example.target_function)
        # __task.set_func_args(args=())
        # # __task.set_func_kwargs(kwargs={"param1": 1, "param2": "this is kwargs"})

        __strategy = MultiProcessingStrategy(workers_num=cls.__Process_Number)
        __strategy.initialization()
        # workers_list = __strategy.build_workers(function=cls.target_func_with_decorator, *__task.func_args, **__task.func_kwargs)
        # __task.set_func_kwargs(kwargs={"task": __task})
        # workers_list = __strategy.build_workers(function=cls.target_task_with_decorator, *__task.func_args, **__task.func_kwargs)
        __kwargs = {"task": task}
        workers_list = __strategy.build_workers(function=cls.target_task_with_decorator, **__kwargs)
        __strategy.activate_workers(workers_list=workers_list)
        __strategy.close()


    @classmethod
    def out_main_test(cls):
        __task = OceanTask(mode=RunningMode.Parallel)
        __task.set_function(function=cls.__example.target_function)
        __task.set_func_args(args=())
        # __task.set_func_kwargs(kwargs={"param1": 1, "param2": "this is kwargs"})
        __task.set_func_kwargs(kwargs={"task": __task})

        cls.main_test(task=__task)



if __name__ == '__main__':

    # print("This is builder client: ")
    # __builder = ExampleBuilderClient()
    # __builder.main_run()

    # print("This is factory client: ")
    # __factory = ExampleFactoryClient()
    # __factory.main_run()

    print("This is system client: ")
    system = ExampleOceanSystem()

    # # # Call multiprocessing API
    system.main_run()
    # system.main_debug()

    # # # Run via RunningStrategy
    # system.main_test()
    # system.out_main_test()

    # system.main_wish_worker()
