=======================
Overview
=======================

Python is a high level program language, but it's free to let anyone choose which running strategy you want to use (Parallel, Concurrent or Coroutine).
Below are some example for each strategy:

* Parallel - with '*multiprocessing*':

.. code-block:: python

    from multiprocessing import Process

    Process_Number = 5

    def function():
        print("This is test process function.")


    if __name__ == '__main__':

        process_list = [Process(target=function)for _ in range(Process_Number)]
        for p in process_list:
            p.start()

        for p in process_list:
            p.join()


* Concurrent - with '*threading*':

.. code-block:: python

    import threading

    Thread_Number = 5

    def function():
        print("This is function content ...")


    if __name__ == '__main__':

        threads_list = [threading.Thread(target=function) for _ in range(Thread_Number)]
        for thread in threads_list:
            thread.start()

        for thread in threads_list:
            thread.join()


* Coroutine - with '*gevent*' (Green Thread):

.. code-block:: python

    from gevent import Greenlet

    Green_Thread_Number = 5

    def function():
        print("This is function content ...")


    if __name__ == '__main__':

        greenlets_list = [Greenlet(function) for _ in range(Green_Thread_Number)]
        for _greenlet in greenlets_list:
            _greenlet.start()

        for _greenlet in greenlets_list:
            _greenlet.join()


* Coroutine - with '*asyncio*' (Asynchronous):

.. code-block:: python

    import asyncio

    async def function():
        print("This is function content ...")

    async def running_function():
        task = asyncio.create_task(function())
        await task


    if __name__ == '__main__':

        asyncio.run(running_function())


No matter which way you choose to implement, it's Python, it's easy.

However, you may change the way to do something for testing, for efficiency, for resource concern or something else.
You need to change to use parallel or coroutine but business logic has been done. The only way is refactoring code.
It's not a problem if it has full-fledged testing code (TDD); if not, it must be an ordeal.

Package '*multirunnable*' is a framework which could build a program with different running strategy by mode option.
Currently, it has 4 options could use: Parallel, Concurrent, GreenThread and Asynchronous.

Here's an example to do the same thing with it:

.. code-block:: python

    from multirunnable import SimpleExecutor, RunningMode
    import random
    import time

    Workers_Number = 5

    def function(index):
        print(f"This is function with index {index}")
        time.sleep(3)


    if __name__ == '__main__':

        executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=Workers_Number)
        executor.run(function=function, args={"index": f"test_{random.randrange(1, 10)}"})


How about Parallel? I want to let it be more fast.
Only one thing you need to do: change the mode.


.. code-block:: python

    ... # Any code is the same

    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=Workers_Number)

    ... # Any code is the same


Program still could run without any refactoring and doesn't need to modify anything.
Want change to use other way to run? Change the Running Mode, that's all.

::

    Parallel, Concurrent and GreenThread are in common but Asynchronous isn't.
    From above all, we could change the mode to run the code as the running strategy we configure.
    However, it only accepts 'awaitable' function to run asynchronously in Python.
    In the other word, you must remember add keyword 'async' before function which is the target to run with *multirunnable*.


=======================
Quickly Start
=======================

Install this package by pip:

    pip install multirunnable

Write a simple code to run it.

    >>> from multirunnable import SimpleExecutor, RunningMode
    >>> executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
    >>> def function(index):
    ...     print(f"This is function with index {index}")
    ...
    >>> executor.run(function=function, args={"index": f"test_param"})
    This is function with index test_param
    This is function with index test_param
    This is function with index test_param
    >>>

