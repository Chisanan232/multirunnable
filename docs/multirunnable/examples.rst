==========
Examples
==========

Some demonstrations of how to use some general modules and its APIs. It demonstrates 4 points and 2 features:

* 4 Points
    * *multirunnable.SimpleExecutor*
    * *multirunnable.SimplePool*
    * Executor or Pool with *multirunnable.persistence.database*
    * Executor or Pool with *multirunnable.persistence.file*

* 2 Features
    * Lock with Python decorators
    * Retry mechanism


4 Points
=========

Demonstrating the core module and APIs of *multirunnable*.

Simple Executor
----------------

An example shows how to use *multirunnable.SimpleExecutor*:

.. code-block:: python

    from multirunnable import RunningMode, SimpleExecutor
    import multirunnable as mr

    def target_function(self, *args, **kwargs) -> str:
        multirunnable.sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        return "Hello, Return"

    _executor_number = 3
    # # # # Initial Executor object
    _executor = SimpleExecutor(mode=RunningMode.Parallel, executors=_executor_number)
    # _executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=_executor_number)
    # _executor = SimpleExecutor(mode=RunningMode.GreenThread, executors=_executor_number)

    # # # # Running the Executor
    _executor.run(function=target_function, args=("index_1", "index_2.2"))


Simple Pool
------------

Using *multirunnable.SimplePool*:

.. code-block:: python

    from multirunnable import RunningMode, SimplePool, sleep, async_sleep
    import random

    def target_function(self, *args, **kwargs) -> str:
        sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        return "Hello, Return"

    # # # # Initial Pool object
    _pool = SimplePool(mode=RunningMode.Parallel, pool_size=self.__Pool_Size, tasks_size=self.__Task_Size)
    # _pool = SimplePool(mode=RunningMode.Concurrent, pool_size=self.__Pool_Size, tasks_size=self.__Task_Size)
    # _pool = SimplePool(mode=RunningMode.GreenThread, pool_size=self.__Pool_Size, tasks_size=self.__Task_Size)

    _result = None
    with _pool as p:
        # # # # Running Pool
        # p.apply(function=target_function, index=f"test_{random.randrange(10,20)}")
        p.async_apply(function=target_function, kwargs={"index": f"test_{random.randrange(10,20)}"})
        p.map(function=target_function, args_iter=("index_1", "index_2.2", "index_3"))
        # p.map_by_args(function=target_function, args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

        # # # # Get result
        # # # # You will get the result of 'map' only.
        _result = p.get_result()

    print("Result: ", _result)



Persistence - Database
-----------------------



Persistence - File
-------------------



Lock with Python decorators
----------------------------



Retry mechanism
-----------------

