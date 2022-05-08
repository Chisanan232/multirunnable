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


Using Bounded Semaphore
------------------------

The usage of *Bounded Semaphore* is completely same as *Semaphore*.
You may get confused about why *Bounded Semaphore* exist if it already have *Semaphore*?
There is a small note about *Semaphore*: it could release over times with *Semaphore* and it doesn't raise any exceptions.
Let's see an example:

.. code-block:: python

    from multirunnable.adapter import Semaphore

    smp_adapter = Semaphore(mode=<RunningMode>, value=2, init=True)

    def lock_function():
        smp_adapter.acquire()
        smp_adapter.release()
        # all is fine, but here we want to test about release over times
        smp_adapter.release()    # It won't occur anything


It would raise nothing and the value setting of *Semaphore* would be added 1.
That might make sense here, but not in most. However, it would raise an exception
if it releases over times with *Bounded Semaphore*. That's the reason why
*Bounded Semaphore* exists and it guarantees that how many it acquires, how many
it must to release exactly.

So, you could modify the *Adapter* to be *Bounded Semaphore*:

.. code-block:: python

    from multirunnable.adapter import BoundedSemaphore

    bsmp_adapter = BoundedSemaphore(mode=<RunningMode>, value=2, init=True)

    def lock_function():
        bsmp_adapter.acquire()
        bsmp_adapter.release()
        bsmp_adapter.release()    # It raises an exception


Here doesn't demonstrate the usage about *Bounded Semaphore* because it's completely same as *Semaphore*.
Please refer to the demonstration of *Semaphore*.


Using Event with *Factory & Operator*
-------------------------------------

If you find a way to let each workers could run and communicate with each others, for example,
worker A wait for worker B to do something util worker B done some task or set flag, *Event* is
one of choices for you.

Beginning by importing modules:

.. code-block:: python

    from multirunnable.api import EventOperator
    from multirunnable.factory import EventFactory


Initial **Factory** and *Operator*:

.. code-block:: python

    _event = EventFactory()
    _event_opt = EventOperator()


We needs 2 workers to do different things to verify the communication feature of *Event*.
One worker is responsible of setting the event flag to be *True*, another one worker just
wait for the flag util to be *True*, start to run and reset the flag back to be *False*.

Let's demonstrate first one worker which would set the event flag to be *True*:

.. code-block:: python

    def wake_other_process():
        print(f"[WakeupProcess] It will keep producing something useless message.")
        while True:
            __sleep_time = random.randrange(1, 10)
            print(f"[WakeupProcess] It will sleep for {__sleep_time} seconds.")
            sleep(__sleep_time)
            _event_opt.set()


Following code is the worker which is waiting for the event flag to be *True* and reset it:

.. code-block:: python

    def go_sleep():
        print(f"[SleepProcess] It detects the message which be produced by ProducerThread.")
        while True:
            sleep(1)
            print("[SleepProcess] ConsumerThread waiting ...")
            _event_opt.wait()
            print("[SleepProcess] ConsumerThread wait up.")
            _event_opt.clear()


You need to run both workers with 2 different functions so that you should use function *SimpleExecutor.map_with_function*.
Its working is same as Python native function *map*, but it works with the collection of functions:

.. code-block:: python

    _exe = SimpleExecutor(mode=RunningMode.Concurrent, executors=1)
    _exe.map_with_function(
        functions=[cls.__wakeup_p.wake_other_process, cls.__sleep_p.go_sleep],
        features=_event
    )


Using Event with *Adapter*
---------------------------

About usage of **Event** as *Adapter* is completely same as *Factory* with *Operator*.
So we could only modify the instantiation like following code:

.. code-block:: python

    from multirunnable.adapter import Event

    _event_adapter = Event()


Using Condition with *Factory & Operator*
-----------------------------------------

*Condition* like a high-class *Lock* or *RLock*. It provides all features of *Lock* (or *RLock*) and some operations like *Event*.
So let's develop 2 workers to demonstrate *Condition* feature, one worker A save data to global list and notify other workers to run,
another worker B wait to get data util worker A has saved data and notified it.

Let's start to import modules:

.. code-block:: python

    from multirunnable import sleep
    from multirunnable.api import ConditionOperator
    from multirunnable.factory import ConditionFactory


Initial **Factory** and *Operator*:

.. code-block:: python

    _condition_factory = ConditionFactory()
    _condition_opt = ConditionOperator()


Initial a global list to save data:

.. code-block:: python

    _glist = []


Following code is worker A which would keep saving data to global list:

.. code-block:: python

    def send_process(*args):
        print(f"[Producer] It will keep producing something useless message.")
        while True:
            _sleep_time = random.randrange(1, 10)
            print(f"[Producer] It will sleep for {_sleep_time} seconds.")
            _glist.append(__sleep_time)
            sleep(_sleep_time)
            _condition_opt.acquire()
            _condition_opt.notify_all()
            _condition_opt.release()


Below is worker B which would wait for worker A util it has saved and notified:

.. code-block:: python

    def receive_process(*args):
        print(f"[Consumer] It detects the message which be produced by ProducerThread.")
        while True:
            _condition_opt.acquire()
            sleep(1)
            print("[Consumer] ConsumerThread waiting ...")
            _condition_opt.wait()
            _sleep_time = _glist[-1]
            print("[Consumer] ConsumerThread re-start.")
            print(f"[Consumer] ProducerThread sleep {_sleep_time} seconds.")
            _condition_opt.release()


Since it has *Lock* (or *RLock*) features, absolutely it would use by Python keyword *with*:

.. code-block:: python

    def send_process(*args):
        print(f"[Producer] It will keep producing something useless message.")
        while True:
            _sleep_time = random.randrange(1, 10)
            print(f"[Producer] It will sleep for {_sleep_time} seconds.")
            _glist.append(__sleep_time)
            sleep(_sleep_time)
            with _condition_opt:
                _condition_opt.notify_all()


    def receive_process(*args):
        print(f"[Consumer] It detects the message which be produced by ProducerThread.")
        while True:
            with _condition_opt:
                sleep(1)
                print("[Consumer] ConsumerThread waiting ...")
                _condition_opt.wait()
                _sleep_time = _glist[-1]
                print("[Consumer] ConsumerThread re-start.")
                print(f"[Consumer] ProducerThread sleep {_sleep_time} seconds.")


Using Condition with *Adapter*
-------------------------------

About usage of **Condition** as *Adapter* is completely same as *Factory* with *Operator*.
So we could only modify the instantiation like following code:

.. code-block:: python

    from multirunnable.adapter import Condition

    _condition_adapter = Condition()


Get context info
=================

content ...


Current worker
---------------

You can get the instance of current worker via *context* module:

.. code-block:: python

    >>> from multirunnable import set_mode, RunningMode
    >>> from multirunnable.adapter.context import context as adapter_context

    >>> set_mode(RunningMode.Parallel)
    >>> adapter_context.get_current_worker()
    <_MainProcess name='MainProcess' parent=None started>


Remember, you should set the *RunningMode* before you get the current worker because you use *adapter* to do it.

You also can get the instance of current worker via **context** module of runnable strategy sub-package:

.. code-block:: python

    >>> from multirunnable.parallel.context import context as process_context

    >>> process_context.get_current_worker()
    <_MainProcess name='MainProcess' parent=None started>

    >>> from multirunnable.concurrent.context import context as thread_context

    >>> thread_context.get_current_worker()
    <_MainThread(MainThread, started 4526204352)>


Current worker's name
----------------------

You also can get the worker name of current worker via *context* module:

.. code-block:: python

    >>> from multirunnable import set_mode, RunningMode
    >>> from multirunnable.adapter.context import context as adapter_context

    >>> set_mode(RunningMode.Parallel)
    >>> adapter_context.get_current_worker_name()
    'MainProcess'


Current worker's Identity
--------------------------

Besides getting the name of current worker, it can get the identity of current worker:

.. code-block:: python

    >>> from multirunnable import set_mode, RunningMode
    >>> from multirunnable.adapter.context import context as adapter_context

    >>> set_mode(RunningMode.Parallel)
    >>> adapter_context.get_current_worker_ident()
    '39164'


By the way, the ID of current worker is a PID if *RunningMode* is *Parallel*. So we also
could verify the identity of process via command *ps*:

.. code-block:: shell

    >>> ps aux | grep -E 'python'
    ...    # other process info
    helloworld        39164   0.0  0.1  4320992  12296 s012  S+   10:15AM   0:00.43 /helloworld/.pyenv/shims/versions/test/bin/python


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

