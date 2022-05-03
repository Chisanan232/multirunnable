===============
Quickly Start
===============

content ...


Quickly build a parallelism
============================

Here is a function for argument *target* to build parallelism.

.. code-block:: python

    from multirunnable import sleep

    def target_func(*args, **kwargs):
        print("This is target function and it will sleep for 3 seconds ...")
        sleep(3)
        print("Wake up and finish.")
        return "Hello, Return"


content ...


Build by Executor
------------------

Build a parallelism with *multirunnable* is very simple.

First of all, import *multirunnable* modules:

.. code-block:: python

    from multirunnable import RunningMode, SimpleExecutor, sleep


Assume you want to build a parallelism with 3 executors (actually, you could use any number you want) by parallel.

Argument *mode* means which strategy you want to use, let's use *RunningMode.Parallel*.
Another argument *executors* means how many executors you want to activate to run.

So the instantiate with arguments should be like below:

.. code-block:: python

    _executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)


By the way, here is instantiation with concurrent:

.. code-block:: python

    _executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=3)


And instantiation with coroutine by green thread:

.. code-block:: python

    _executor = SimpleExecutor(mode=RunningMode.GreenThread, executors=3)


Now, you could try to run a parallelism with the target function easily:

.. code-block:: python

    _executor.run(function=target_func)


It absolutely isn't a problem if you want to pass parameters to target function or method:

.. code-block:: python

    _executor.run(function=target_func, args=("index_1", "index_2.2"))
    _executor.run(function=target_func, kwargs={"param_1": "index_1", "param_2": "index_2"})


How easy it is, isn't it? That's also easy to get its running result:

.. code-block:: python

    _result = p.get_result()
    print("Result: ", _result)


Build via Pool
---------------

About using *Pool*, it's also easy as *Executor*.

Begin by importing *multirunnable* modules, too:

.. code-block:: python

    from multirunnable import RunningMode, SimplePool


For example, you want to build a parallelism with 3 size of executors (also, you could use any number you want) by parallel via *Pool*.

Argument *mode* is same as the option *mode* of *Executor*, let's use *RunningMode.Parallel*, too.
Another argument *pool_size* means what size the *Pool* could temporary save the *workers*.

In *MultiRunnable* realm, *worker* may be a different runnable object with different strategy.
For example, *worker* is *Process* with *RunningMode.Parallel*; *worker* is *Thread* with *RunningMode.Concurrent*;
*worker* is *Greenlet* with *RunningMode.GreenThread*.

So the instantiate with arguments should be following code:

.. code-block:: python

    _pool = SimplePool(mode=RunningMode.Parallel, pool_size=5)


It's same as *Executor* if you want to use other strategy like concurrent or coroutine.

Now, let's run it via *Pool*:

.. code-block:: python

    with _pool as p:
        p.async_apply(function=target_func)


The way to get running result is same as *Executor*:

.. code-block:: python

    _result = p.get_result()
    print("Result: ", _result)


Running with Synchronizations
==============================

content ...


Lock
------

content ...


RLock
-------

content ...


Semaphore
-----------

content ...


Bounded Semaphore
-------------------

content ...


Event
-------

content ...


Condition
-----------

content ...


Context info in parallelism
============================

content ...

Current worker
---------------

content ...


Current worker's name
----------------------

content ...


Current worker's Identity
--------------------------

content ...


Current worker's parent
------------------------

content ...


Globally context info
----------------------

content ...


Persistence in parallelism
===========================

content ...


Operate with file
------------------

content ...


Operate with database
----------------------

content ...

