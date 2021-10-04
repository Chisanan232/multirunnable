# multirunnable

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Release](https://img.shields.io/github/release/Chisanan232/multirunnable.svg?label=Release&sort=semver)](https://github.com/Chisanan232/multirunnable/releases)
[![PyPI version](https://badge.fury.io/py/multirunnable.svg)](https://badge.fury.io/py/multirunnable)
[![Supported Versions](https://img.shields.io/pypi/pyversions/multirunnable.svg)](https://pypi.org/project/multirunnable)

A Python framework integrates building program which could run multiple tasks with different running strategy.

[Overview](#overview) | [Quickly Start](#quickly-start) | [Usage](#usage) | [Code Example](https://github.com/Chisanan232/multirunnable/tree/master/example)
<hr>

## Overview

Python is a high level program language, but it's free to let anyone choose which running strategy you want to use (Parallel, Concurrent or Coroutine). <br>
Below are some example for each strategy:

* Parallel - with '**_multiprocessing_**':

```python
from multiprocessing import Process

Process_Number = 5

def function():
    print("This is test process function.")


if __name__ == '__main__':

    __process_list = [Process(target=function)for _ in range(Process_Number)]
    for __p in __process_list:
        __p.start()

    for __p in __process_list:
        __p.join()
```

* Concurrent - with '**_threading_**':

```python
import threading

Thread_Number = 5

def function():
    print("This is function content ...")


if __name__ == '__main__':
    
    threads_list = [threading.Thread(target=function) for _ in range(Thread_Number)]
    for __thread in threads_list:
        __thread.start()
    
    for __thread in threads_list:
        __thread.join()
```

* Coroutine - with '**_gevent_**' (Green Thread):

```python
from gevent import Greenlet

Green_Thread_Number = 5

def function():
    print("This is function content ...")


if __name__ == '__main__':

    greenlets_list = [Greenlet(function) for _ in range(Green_Thread_Number)]
    for __greenlet in greenlets_list:
        __greenlet.start()

    for __greenlet in greenlets_list:
        __greenlet.join()
```

* Coroutine - with '**_asyncio_**' (Asynchronous):

```python
import asyncio

async def function():
    print("This is function content ...")

async def running_function():
    task = asyncio.create_task(function())
    await task


if __name__ == '__main__':

    asyncio.run(running_function())
```

No matter which way you choose to implement, it's Python, it's easy.

However, you may change the way to do something for testing, for efficiency, for resource concern or something else. 
You need to change to use parallel or coroutine but business logic has been done. The only way is refactoring code. 
It's not a problem if it has full-fledged testing code (TDD); if not, it must be an ordeal.

Package '_multirunnable_' is a framework which could build a program with different running strategy by mode option. 
Currently, it has 4 options could use: Parallel, Concurrent, GreenThread and Asynchronous.

Here's an example to do the same thing with it:

```python
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
```

How about Parallel? I want to let it be more fast. 
Only one thing you need to do: change the mode.

```python
... # Any code is the same

executor = SimpleExecutor(mode=RunningMode.Parallel, executors=Workers_Number)

... # Any code is the same
```

Program still could run without any refactoring and doesn't need to modify anything. <br>
Want change to use other way to run? Change the Running Mode, that's all. <br>

> ⚠️ **Parallel, Concurrent and GreenThread are in common but Asynchronous isn't.** <br>
From above all, we could change the mode to run the code as the running strategy we configure. 
However, it only accepts 'awaitable' function to run asynchronously in Python. 
In the other word, you must remember add keyword 'async' before function which is the target to run with _multirunnable_.


## Quickly Start

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


## Usage

This package classifies the runnable unit to be Executor and Pool.<br>
It also supports doing some operators with running multiple tasks simultaneously 
like Lock, Semaphore, Event, etc.

* Runnable Components
    * [Executor](#executor)
    * [Pool](#pool)
* Lock Features
    * [Lock](#lock)
    * [RLock](#rlock)
    * [Semaphore](#semaphore)
    * [Bounded Semaphore](#bounded-semaphore)
* Communication Features
    * [Event](#event)
    * [Condition](#condition)
* Queue
    * [Queue](#queue)
* Others
    * [Retry Mechanism](#retry-mechanism)

<br>

### Runnable Components
<hr>

* ### Executor

This is a basic unit for every running strategy.

* Parallel -> Process
* Concurrent -> Thread
* Green Thread -> Greenlet object
* Asynchronous -> Asynchronous task object

We could run an easy Parallel, Concurrent or Coroutine code with it.

```python
from multirunnable import SimpleExecutor, RunningMode

executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
executor.run(function=<Your target function>, args=<The arguments of target function>)
```

* ### Pool

This Pool concept is same as below:

* Parallel -> multiprocessing.Pool
* Concurrent -> multiprocessing.ThreadPool
* Green Thread -> gevent.pool.Pool
* Asynchronous -> Doesn't support this feature

```python
from multirunnable import SimplePool, RunningMode

pool = SimplePool(mode=RunningMode.Parallel, pool_size=3, tasks_size=10)
pool.async_apply(function=<Your target function>, args=<The arguments of target function>)
```

<br>

### Lock Features
<hr>

* ### Lock

With _multirunnable_, it should initial Lock objects before you use it.

```python
from multirunnable import SimpleExecutor, RunningMode
from multirunnable.adapter import Lock

# Initial Lock object
lock = Lock()

executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
# Pass into executor or pool via parameter 'features'
executor.run(function=<Your target function>, features=lock)
```

It could use the Lock object via **LockOperator**.

```python
from multirunnable.api import LockOperator
import time

lock = LockOperator()

def lock_function():
    lock.acquire()
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")
    lock.release()
```

Above code with Lock function is equal to below:

```python
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
```

Or with keyword **with**:

```python
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
```

✨👀 **Using features with Python decorator**

It also could use Lock via decorator **RunWith** (it's **AsyncRunWith** with Asynchronous).

```python
from multirunnable.api import RunWith
import time

@RunWith.Lock
def lock_function():
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")
```

Only below features support decorator: <br>
**Lock**, **Semaphore**, **Bounded Semaphore**.

* ### RLock

Lock only could acquire and release one time but RLock could acquire and release multiple times.

```python
from multirunnable.api import RLockOperator
import time

rlock = RLockOperator()

def lock_function():
    rlock.acquire()
    print("Acquire RLock 1 time")
    rlock.acquire()
    print("Acquire RLock 2 time")
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")
    rlock.release()
    print("Acquire Release 1 time")
    rlock.release()
    print("Acquire Release 2 time")
```

* ### Semaphore

Semaphore could accept multiple runnable unit in target function:

```python
from multirunnable.api import RunWith
import time

@RunWith.Semaphore
def lock_function():
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")
```

* ### Bounded Semaphore

It's mostly same as _Semaphore_.

<br>

### Communication Features
<hr>

For features Event and Condition, they all don't support using with decorator. 
So it must use it via operator object.

* ### Event

```python
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
```

* ### Condition

```python
from multirunnable import SimpleExecutor, RunningMode, QueueTask, sleep
from multirunnable.api import ConditionOperator, QueueOperator
from multirunnable.adapter import Condition
from multirunnable.concurrent import MultiThreadingQueueType
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
        __task.queue_type = MultiThreadingQueueType.Queue
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
```


<br>

### Queue
<hr>

The Queue in _multirunnable_ classify to different type by running strategy.
For usage, it should do 2 things: initial and get.

* ### Queue

It must use Queue feature with object **QueueTask**. It could configure some info like name, type and value.
Name is a key of the queue object. Type means which one Queue object type you want to use.

For example, we want to set a Queue with name "test_queue", type is **multiprocessing.Queue**:

```python
from multirunnable import QueueTask
from multirunnable.parallel import MultiProcessingQueueType

test_queue_task = QueueTask()
test_queue_task.name = "test_queue"
test_queue_task.queue_type = MultiProcessingQueueType.Queue
test_queue_task.value = [f"value_{i}" for i in range(20)]
```

We could get the queue object via **QueueOperator**:

```python
from multirunnable.api import QueueOperator

queue = QueueOperator.get_queue_with_name(name="test_queue")
```

Also, we need to pass it by parameter '_queue_task_' before we use it.

```python
from multirunnable import SimpleExecutor, RunningMode

executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
executor.run(function=<Your target function>, queue_tasks=test_queue_task)
```


<br>

### Others
<hr>

* ### Retry Mechanism

It's possible that occurs unexpected something when running. Sometimes, it needs 
to catch that exceptions or errors to do some handling, it even needs to do something
finally and keep going run the code. That's the reason this feature exists.

Below is the life cycle of runnable unit (worker):

![image](https://github.com/Chisanan232/multirunnable/blob/master/doc/imgs/MultiRunnable-Worker_work_flow.png)

It could use the feature via Python decorator **retry** (It's **async_retry** with Asynchronous).

```python
from multirunnable.api import retry
import multirunnable

@retry
def target_fail_function(*args, **kwargs):
    print("It will raise exception after 3 seconds ...")
    multirunnable.sleep(3)
    raise Exception("Test for error")
```

It absolutely could configure timeout time (Default value is 1).

```python
from multirunnable.api import retry
import multirunnable

@retry(timeout=3)
def target_fail_function(*args, **kwargs):
    print("It will raise exception after 3 seconds ...")
    multirunnable.sleep(3)
    raise Exception("Test for error")
```

It would be decorated as a 'retry' object after adds decorator on it. 
So we could add some features you need.

* Initialization 

The function which should be run first before run target function. <br>
Default implementation is doing nothing.<br>
The usage is decorating as target function annotation name and call **.initialization** method.

```python
@target_fail_function.initialization
def initial():
    print("This is testing initialization")
```

* Done Handling

It will return value after run completely target function. This feature argument 
receives the result. You could do some result-handling here to reach your own target, 
and it will return it out. <br>
Default implementation is doing nothing, just return the result it gets.<br>
The usage is decorating as target function annotation name and call **.done_handling** method.

```python
@target_fail_function.done_handling
def done(result):
    print("This is testing done process")
    print("Get something result: ", result)
```

* Final Handling

It's the feature run something which MUST to do. For example, close IO.  <br>
Default implementation is doing nothing. <br>
The usage is decorating as target function annotation name and call **.final_handling** method.

```python
@target_fail_function.final_handling
def final():
    print("This is final process")
```

* Exception & Error - Handling 

Target to handle every exception or error. So the function argument absolutely receives exception or error. <br>
Default implementation is raising any exception or error it gets. <br>
The usage is decorating as target function annotation name and call **.error_handling** method.

```python
@target_fail_function.error_handling
def error(error):
    print("This is error process")
    print("Get something error: ", error)
```

