========
Usages
========

This package classifies the runnable unit to be Executor and Pool.
It also supports doing some operators with running multiple tasks simultaneously 
like Lock, Semaphore, Event, etc.

Run Executor or Pool with RunningMode
======================================

.. _Executor Usage:

*Executor*
------------

This object would operate with basic unit runnable object like Process or Thread by running strategy.

.. code-block:: python

    from multirunnable import SimpleExecutor, RunningMode

    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
    executor.run(function=<Your target function>, args=<The arguments of target function>)


.. _Pool Usage:

*Pool*
-------

This is Pool of runnable object with running strategy.

.. code-block:: python

    from multirunnable import SimplePool, RunningMode

    pool = SimplePool(mode=RunningMode.Parallel, pool_size=3, tasks_size=10)
    pool.async_apply(function=<Your target function>, args=<The arguments of target function>)



.. _Synchronize MultiRunnable Task --- Lock the performance:

Synchronize MultiRunnable Task --- Lock the performance
=========================================================

It could synchronize tasks of *multirunnable* objects with Lock, Semaphore, etc.

*Lock*
-------

With *multirunnable*, it should initial Lock objects before you use it.

.. code-block:: python

    from multirunnable import SimpleExecutor, RunningMode
    from multirunnable.adapter import Lock

    # Initial Lock object
    lock = Lock()

    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
    # Pass it into executor or pool via option *features*
    executor.run(function=<Your target function>, features=lock)


It could use the Lock object via object **LockOperator**.

.. code-block:: python

    from multirunnable.api import LockOperator
    import time

    lock = LockOperator()

    def lock_function():
        lock.acquire()
        print("Running process in lock and will sleep 2 seconds.")
        time.sleep(2)
        print(f"Wake up process and release lock.")
        lock.release()


or implement via Python keyword **with**:

.. code-block:: python

    from multirunnable.api import LockOperator
    import time

    lock = LockOperator()

    def lock_function():
        with lock:
            print("Running process in lock and will sleep 2 seconds.")
            time.sleep(2)
            print(f"Wake up process and release lock.")


Above implementations with Lock feature is equal to below:

.. code-block:: python

    import threading
    import time

    ... # Some logic

    lock = threading.Lock()

    print(f"Here is sample function running with lock.")
    lock.acquire()
    print(f"Process in lock and it will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")
    lock.release()

    ... # Some logic


Or with keyword **with**:

.. code-block:: python

    import threading
    import time

    ... # Some logic

    lock = threading.Lock()

    print(f"Here is sample function running with lock.")
    with lock:
        print(f"Process in lock and it will sleep 2 seconds.")
        time.sleep(2)
        print(f"Wake up process and release lock.")

    ... # Some logic


✨👀 **Using multirunnable features with Python decorator**

It also could use Lock via decorator **RunWith** (it's **AsyncRunWith** with Asynchronous).

.. code-block:: python

    from multirunnable.api import RunWith
    import time

    @RunWith.Lock
    def lock_function():
        print("Running process in lock and will sleep 2 seconds.")
        time.sleep(2)
        print(f"Wake up process and release lock.")


Only these features support decorator: **Lock**, **RLock**, **Semaphore**, **Bounded Semaphore**.

Why Lock with decorator?
~~~~~~~~~~~~~~~~~~~~~~~~~

Lock, Semaphore or something else features would deeply affect the performance of parallelism.
*MultiRunnable* require developers do as much as you can about ONLY lock the necessary section to
let parallelism stay at high performance. It also could remind others this function would run with
lock.


*Semaphore*
-------------

Semaphore could accept multiple runnable objects to run target function:

.. code-block:: python

    from multirunnable.api import RunWith
    import time

    @RunWith.Semaphore
    def lock_function():
        print("Running process in lock and will sleep 2 seconds.")
        time.sleep(2)
        print(f"Wake up process and release lock.")


Synchronize MultiRunnable Task --- Communicate with each others
================================================================

For features Event and Condition, they all don't support using with decorator. 
So it must use it via operator object.

*Event*
---------

.. code-block:: python

    from multirunnable import SimpleExecutor, RunningMode, sleep
    from multirunnable.api import EventOperator
    from multirunnable.adapter import Event
    import random


    class WakeupProcess:

        __event_opt = EventOperator()

        def wake_other_process(self, *args):
            print(f"[WakeupProcess] It will keep producing something useless message.")
            while True:
                __sleep_time = random.randrange(1, 10)
                print(f"[WakeupProcess] It will sleep for {__sleep_time} seconds.")
                sleep(__sleep_time)
                self.__event_opt.set()


    class SleepProcess:

        __event_opt = EventOperator()

        def go_sleep(self, *args):
            print(f"[SleepProcess] It detects the message which be produced by ProducerThread.")
            while True:
                sleep(1)
                print("[SleepProcess] ConsumerThread waiting ...")
                self.__event_opt.wait()
                print("[SleepProcess] ConsumerThread wait up.")
                self.__event_opt.clear()


    if __name__ == '__main__':

        __wakeup_p = WakeupProcess()
        __sleep_p = SleepProcess()

        # Initialize Event object
        __event = Event()

        # # # # Run without arguments
        executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
        executor.map_with_function(
            functions=[__wakeup_p.wake_other_process, __sleep_p.go_sleep],
            features=__event)


*Condition*
-------------

.. code-block:: python

    from multirunnable import SimpleExecutor, RunningMode, QueueTask, sleep
    from multirunnable.api import ConditionOperator, QueueOperator
    from multirunnable.adapter import Condition
    from multirunnable.concurrent import ThreadQueueType
    import random


    class ProducerProcess:
      __Queue_Name = "test_queue"

      def __init__(self):
        self.__condition_opt = ConditionOperator()
        self.__queue_opt = QueueOperator()

      def send_process(self, *args):
        print("[Producer] args: ", args)
        test_queue = self.__queue_opt.get_queue_with_name(name=self.__Queue_Name)
        print(f"[Producer] It will keep producing something useless message.")
        while True:
          __sleep_time = random.randrange(1, 10)
          print(f"[Producer] It will sleep for {__sleep_time} seconds.")
          test_queue.put(__sleep_time)
          sleep(__sleep_time)
          __condition = self.__condition_opt
          with __condition:
            self.__condition_opt.notify_all()


    class ConsumerProcess:
      __Queue_Name = "test_queue"

      def __init__(self):
        self.__condition_opt = ConditionOperator()
        self.__queue_opt = QueueOperator()

      def receive_process(self, *args):
        print("[Consumer] args: ", args)
        test_queue = self.__queue_opt.get_queue_with_name(name=self.__Queue_Name)
        print(f"[Consumer] It detects the message which be produced by ProducerThread.")
        while True:
          __condition = self.__condition_opt
          with __condition:
            sleep(1)
            print("[Consumer] ConsumerThread waiting ...")
            self.__condition_opt.wait()
            __sleep_time = test_queue.get()
            print("[Consumer] ConsumerThread re-start.")
            print(f"[Consumer] ProducerThread sleep {__sleep_time} seconds.")


    class ExampleOceanSystem:
      __Executor_Number = 1

      __producer_p = ProducerProcess()
      __consumer_p = ConsumerProcess()

      @classmethod
      def main_run(cls):
        # Initialize Condition object
        __condition = Condition()

        # Initialize Queue object
        __task = QueueTask()
        __task.name = "test_queue"
        __task.queue_type = ThreadQueueType.Queue
        __task.value = []

        # Initialize and run ocean-simple-executor
        __exe = SimpleExecutor(mode=RunningMode.Concurrent, executors=cls.__Executor_Number)
        # # # # Run without arguments
        __exe.map_with_function(
          functions=[cls.__producer_p.send_process, cls.__consumer_p.receive_process],
          queue_tasks=__task,
          features=__condition)


    if __name__ == '__main__':
      print("[MainProcess] This is system client: ")
      system = ExampleOceanSystem()
      system.main_run()
      print("[MainProcess] Finish. ")



Using Queue in MultiRunnable
=============================

The Queue in *multirunnable* classify to different type by running strategy.
For usage, it should do 2 things: initial and get.

*Queue*
---------

It must use Queue feature with object **QueueTask**. It could configure some info like name, type and value.
Name is a key of the queue object. Type means which one Queue object type you want to use.

For example, we want to set a Queue with name "test_queue", type is **multiprocessing.Queue**:

.. code-block:: python

    from multirunnable import QueueTask
    from multirunnable.parallel import ProcessQueueType

    test_queue_task = QueueTask()
    test_queue_task.name = "test_queue"
    test_queue_task.queue_type = ProcessQueueType.Queue
    test_queue_task.value = [f"value_{i}" for i in range(20)]


We could get the queue object via **QueueOperator**:

.. code-block:: python

    from multirunnable.api import QueueOperator

    queue = QueueOperator.get_queue_with_name(name="test_queue")


Also, we need to pass it by parameter '_queue_task_' before we use it.

.. code-block:: python

    from multirunnable import SimpleExecutor, RunningMode

    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
    executor.run(function=<Your target function>, queue_tasks=test_queue_task)



.. _Retry to run target function if it raises exception:

Retry to run target function if it raises exception
====================================================

*retry*
--------

It's possible that occurs unexpected something when running. Sometimes, it needs 
to catch that exceptions or errors to do some handling or it needs to do something
finally and keep going run. That's the reason why this feature exists.

It could use the feature via Python decorator **retry** (It's **async_retry** with Asynchronous).

.. code-block:: python

    from multirunnable.api import retry
    import multirunnable

    @retry
    def target_fail_function(*args, **kwargs):
        print("It will raise exception after 3 seconds ...")
        multirunnable.sleep(3)
        raise Exception("Test for error")


It absolutely could configure timeout time (Default value is 1).

.. code-block:: python

    from multirunnable.api import retry
    import multirunnable

    @retry(timeout=3)
    def target_fail_function(*args, **kwargs):
        print("It will raise exception after 3 seconds ...")
        multirunnable.sleep(3)
        raise Exception("Test for error")


It would be decorated as a 'retry' object after adds decorator on it. 
So we could add some features you need.

* Initialization

The function which should be run first before run target function.

.. code-block:: python

    @target_fail_function.initialization
    def initial():
        print("This is testing initialization")


* Done Handling

It will return value after run completely target function.

.. code-block:: python

    @target_fail_function.done_handling
    def done(result):
        print("This is testing done process")
        print("Get something result: ", result)


* Final Handling

It's the feature run something which MUST to do. For example, close IO.

.. code-block:: python

    @target_fail_function.final_handling
    def final():
        print("This is final process")


* Exception & Error - Handling

Target to handle every exception or error.

.. code-block:: python

    @target_fail_function.error_handling
    def error(error):
        print("This is error process")
        print("Get something error: ", error)


