===============
Quickly Start
===============

content ...


Build a parallelism
====================

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

The usage of *RLock* is very similar with *Lock*, but the former one could acquire again and the latter one couldn't.
In the other words, it could acquire or release lock again and again but it doesn't occur deadlock.

Let's import module first:

.. code-block:: python

    from multirunnable.factory import RLockFactory
    from multirunnable.api import RLockOperator


Initial **Factory**:

.. code-block:: python

    rlock_factory = RLockFactory()


It could operate the *RLock* object via **Operator**. Please note that it acquire and release twice:

.. code-block:: python

    rlock_opt = RLockOperator()

    def lock_function():
        rlock_opt.acquire()
        print("Acquire RLock first time.")
        rlock_opt.acquire()
        print("Acquire RLock second time and will sleep 2 seconds.")
        sleep(2)
        print(f"Release RLock first time.")
        rlock_opt.release()
        print(f"Release RLock second time and wake up process.")
        rlock_opt.release()


Modify to implement with Python keyword *with*:

.. code-block:: python

    rlock_opt = RLockOperator()

    def lock_function():
        with rlock_opt:
            print("Acquire RLock first time.")

            with rlock_opt:
                print("Acquire RLock second time and will sleep 2 seconds.")
                sleep(2)
                print(f"Release RLock first time.")

            print(f"Release RLock second time and wake up process.")


However, following code is a better usage with *RLock*:

.. code-block:: python

    rlock_opt = RLockOperator()

    def lock_function_a():
        with rlock_opt:
            print("Acquire RLock at Function A.")
            sleep(2)    # It could do something which should be managed by RLock
            print(f"Release RLock at Function A and wake up process.")

    def lock_function_b():
        with rlock_opt:
            print("Acquire RLock at Function B.")
            sleep(2)    # It could do something which should be managed by RLock
            print(f"Release RLock at Function B and wake up process.")


If you have multiple tasks (in generally, it's a function or method) to do which needs to be managed by lock,
*RLock* would be the better choice for you.


Using RLock with *Adapter*
---------------------------

The usage of *RLock Adapter* is also very similar with *Lock Adapter*.

Import module:

.. code-block:: python

    from multirunnable.adapter import RLock


Instantiates **RLock** with option *init* as *True*. It would initial anything you need.

.. code-block:: python

    rlock_adapter = RLock(mode=<RunningMode>, init=True)


So, you could operate it directly (absolutely, you also can use it via Python keyword *with*):

.. code-block:: python

    def lock_function():
        with rlock_adapter:
            print("Acquire RLock first time.")

            with rlock_adapter:
                print("Acquire RLock second time and will sleep 2 seconds.")
                sleep(2)
                print(f"Release RLock first time.")

            print(f"Release RLock second time and wake up process.")


Using Semaphore with *Factory & Operator*
-----------------------------------------

The usage of *Lock*, *RLock* or *Semaphore* are very close between each others. Actually,
you could detect that by the APIs of them.

The most different between *Lock* and *Semaphore* is former one accept ONLY ONE worker runs at the same time,
but the latter one could accept MULTIPLE workers run simultaneously.

Let's import module first:

.. code-block:: python

    from multirunnable.factory import SemaphoreFactory
    from multirunnable.api import SemaphoreOperator


Initial **Factory**. Remember, you should set the count how many workers it should accept to run simultaneously by argument *value*:

.. code-block:: python

    smp_factory = SemaphoreFactory(value=2)


It could operate the *Semaphore* object via **Operator**. Please note that it could accept multiple workers:

.. code-block:: python

    smp_opt = SemaphoreOperator()

    def lock_function():
        smp_opt.acquire()
        print("Acquire Semaphore.")
        sleep(2)
        print(f"Release Semaphore.")
        smp_opt.release()


Modify to implement with Python keyword *with*:

.. code-block:: python

    smp_opt = SemaphoreOperator()

    def lock_function():
        with smp_opt:
            print("Acquire Semaphore.")
            sleep(2)
            print(f"Release Semaphore.")


Using Semaphore with *Adapter*
-------------------------------

Import module:

.. code-block:: python

    from multirunnable.adapter import Semaphore


Instantiates **Semaphore** with option *init* as *True*, absolutely also with option *value*.

.. code-block:: python

    smp_adapter = Semaphore(mode=<RunningMode>, value=2, init=True)


So, you could operate it directly (absolutely, you also can use it via Python keyword *with*):

.. code-block:: python

    def lock_function():
        with smp_adapter:
            print("Acquire Semaphore.")
            sleep(2)
            print(f"Release Semaphore.")


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


Get context info
=================

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

