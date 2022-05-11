===============
Introduction
===============

About
======

Python is a high level program language, but it could implement different parallelism: *Parallel*, *Concurrent* and *Coroutine*.
No matter which way developers choose to use, they all have some rules:

    Initial multiple runnable objects -> Run them -> Join and Close them

About **runnable objects**, it means a object which would be configured target functions (sometimes, including its parameters).
Developers could initial multiple it and run them simultaneously. Like *threading.Thread* or *multiprocessing.Process*.
No matter Parallel, Concurrent or Coroutine, they're different, absolutely. But their usage-procedure are similar, too.
*MultiRunnable* target to integrate the usage-procedure and try to let developers to implement parallelism code easily and clearly
with different running strategy, event it still isn't a stable and entire package (It's release version is |release|) currently.


Comparison
===========

Now, it clears that Parallel, Concurrent or Coroutine are different but its usage-procedures are mostly the same.
Below are some demonstrations with them:

* Parallel - with '*multiprocessing*':

.. code-block:: python

    from multiprocessing import Process

    Process_Number = 5

    def function():
        print("This is test process function.")


    if __name__ == '__main__':

        # Initial runnable objects --- Processes
        process_list = [Process(target=function)for _ in range(Process_Number)]

        # Run runnable objects
        for p in process_list:
            p.start()

        # Close runnable objects
        for p in process_list:
            p.join()
            p.close()    # New in Python 3.7 up.


* Concurrent - with '*threading*':

.. code-block:: python

    import threading

    Thread_Number = 5

    def function():
        print("This is function content ...")


    if __name__ == '__main__':

        # Initial runnable objects --- Threads
        threads_list = [threading.Thread(target=function) for _ in range(Thread_Number)]

        # Run runnable objects
        for thread in threads_list:
            thread.start()

        # Close runnable objects
        for thread in threads_list:
            thread.join()
            thread.close()


* Coroutine - with '*gevent*' (Green Thread):

.. code-block:: python

    from gevent import Greenlet

    Green_Thread_Number = 5

    def function():
        print("This is function content ...")


    if __name__ == '__main__':

        # Initial runnable objects --- Green Threads
        greenlets_list = [Greenlet(function) for _ in range(Green_Thread_Number)]

        # Run runnable objects
        for _greenlet in greenlets_list:
            _greenlet.start()

        # Close runnable objects
        for _greenlet in greenlets_list:
            _greenlet.join()


* Coroutine - with '*asyncio*' (Asynchronous):

.. code-block:: python

    import asyncio

    async def function():
        print("This is function content ...")

    async def running_function():
        # Initial runnable objects --- Green Threads
        task = asyncio.create_task(function())
        await task


    if __name__ == '__main__':

        # Run runnable objects
        asyncio.run(running_function())


Above all are demonstrations with Python library (*multiprocessing*, *threading* and *asyncio* are native library).
It could observe that the usage-procedures of Parallel (*multiprocessing*), Concurrent (*threading*), Coroutine (*gevent*) are the same.
Though left one Coroutine (*asyncio*) doesn't need to close asynchronous tasks but it still needs to initial and run them.
So let's show an example parallelism code with *multirunnable*:

* Implement by '*multirunnable*':

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


Obviously, you could reach the same target with using *Executor.run* only.
However, that's Concurrent. How about Parallel or Coroutine? It's very easy, it just only change the value of option *mode*:

.. code-block:: python

    ... # Any code is the same
    # Change to Parallel!
    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=Workers_Number)
    ... # Any code is the same

or

.. code-block:: python

    ... # Any code is the same
    # Change to Coroutine with Green Thread!
    executor = SimpleExecutor(mode=RunningMode.GreenThread, executors=Workers_Number)
    ... # Any code is the same


It's also the same with Coroutine --- Asynchronous. But please remember that target function should be a **awaitable** function:

.. code-block:: python

    from multirunnable import SimpleExecutor, RunningMode, async_sleep
    import random

    Workers_Number = 5

    async def function(index):
        print(f"This is function with index {index}")
        async_sleep(3)


    if __name__ == '__main__':

        executor = SimpleExecutor(mode=RunningMode.Asynchronous, executors=Workers_Number)
        executor.run(function=function, args={"index": f"test_{random.randrange(1, 10)}"})


Simple Demonstration
======================

Install this package by pip:

.. code-block:: bash

    pip install multirunnable


Write a simple code to run it.

.. code-block:: bash

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

