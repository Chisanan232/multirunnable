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

In *multirunnable* realm, it has 2 ways to use *synchronization* object. One is usage with 2 objects: **Factory** and **Operator**,
another one is usage with **Adapter**.

* *Factory & Operator*

    If you're building a parallelism with big software architecture, this way would be a good choice for you.
    It divides the logic into 2 parts: generating synchronization instance and operating with the synchronization instance.
    Hence you could implement them in different function, class or method.


* *Adapter*

    If you're building a simple parallelism, this way would be better for you.
    It integrates all the features or APIs of *Factory* & *Operator* into itself.
    Therefore you could do anything with it.


Using Lock with *Factory & Operator*
-------------------------------------

We should import the modules from 2 different sub-packages *factory* and *api* to use *Lock* with **Factory & Operator**:

.. code-block:: python

    from multirunnable import SimpleExecutor, RunningMode, sleep
    from multirunnable.factory import LockFactory
    from multirunnable.api import LockOperator


Initial **Factory**:

.. code-block:: python

    lock_factory = LockFactory()


It could operate the *Lock* object via **Operator**:

.. code-block:: python

    lock_opt = LockOperator()

    def lock_function():
        lock_opt.acquire()
        print("Running process in lock and will sleep 2 seconds.")
        sleep(2)
        print(f"Wake up process and release lock.")
        lock_opt.release()


or you also could use it via Python keyword *with*:

.. code-block:: python

    lock_opt = LockOperator()

    def lock_function():
        with lock_opt:
            print("Running process in lock and will sleep 2 seconds.")
            sleep(2)
            print(f"Wake up process and release lock.")


Finally, please don't forget pass the Lock Factory by argument *features* (it's same in *Executor* or *Pool*):

.. code-block:: python

    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
    executor.run(function=lock_function, features=lock_factory)


Using Lock with *Adapter*
---------------------------

It's only import 1 module if you use **Adapter**:

.. code-block:: python

    from multirunnable import SimpleExecutor, RunningMode, sleep
    from multirunnable.adapter import Lock


You would need to set option *init* to be *True* when you instantiates **Lock**.
It would initial anything you need.

.. code-block:: python

    lock_adapter = Lock(mode=RunningMode.Parallel, init=True)


So, you could operate it directly (absolutely, you also can use it via Python keyword *with*):

.. code-block:: python

    def lock_function():
        lock_adapter.acquire()
        print("This is ExampleTargetFunction.target_function.")
        sleep(3)
        lock_adapter.release()


Furthermore, you don't need to pass it  by argument *features*:

.. code-block:: python

    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
    executor.run(function=lock_function)


Using RLock with *Factory & Operator*
-------------------------------------

content ...


Using RLock with *Adapter*
---------------------------

content ...


Using Semaphore with *Factory & Operator*
-----------------------------------------

content ...


Using Semaphore with *Adapter*
-------------------------------

content ...


Using Bounded Semaphore with *Factory & Operator*
-------------------------------------------------

content ...


Using Bounded Semaphore with *Adapter*
---------------------------------------

content ...


Using Event with *Factory & Operator*
-------------------------------------

content ...


Using Event with *Adapter*
---------------------------

content ...


Using Condition with *Factory & Operator*
-----------------------------------------

content ...


Using Condition with *Adapter*
-------------------------------

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

