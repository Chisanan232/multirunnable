# pyocean

A Python framework integrates building program multi-worker with different running strategy.
It could very easily build a feature running multi-work simultaneously.

Python is a high level program language, but it's free to let anyone choose which running strategy you want to use.
For example, if you want a concurrent feature, it should be like below:

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

Or you also could implement threading.Thread run method:

```python
import threading


Thread_Number = 5

class SampleThread(threading.Thread):

    def run(self):
        print("This is function content which be run in the same time.")


if __name__ == '__main__':
    
    thread_list = [SampleThread() for _ in range(Thread_Number)]
    for __thread in thread_list:
        __thread.start()

    for __thread in thread_list:
        __thread.join()
```

No matter which way you choose to implement, it's Python, it's easy.

However, you may change the way to do something for testing, for efficiency, for resource concern or something else. 
You need to change to use parallel or coroutine but business logic has been done. The only way is refactoring code. 
It's not a problem if it has full-fledged testing code (TDD); if not, it must be an ordeal.

Package 'pyocean' is a framework to build a program with different running strategy by mode option. 
Currently, it has 4 options could use: Parallel, Concurrent, Greenlet and Asynchronous.

Here's an example to do the same thing with pyocean:

```python
from pyocean import SimpleExecutor, RunningMode
import random
import time

Thread_Number = 5

def function(index):
    print(f"This is function with index {index}")
    time.sleep(3)


if __name__ == '__main__':
    
    executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=Thread_Number)
    executor.run(function=function, args={"index": f"test_{random.randrange(1, 10)}"})

```

How about Parallel? I want to let it be more fast. 
Only one thing you need to do: change the mode.

```python

... # Any code is the same

executor = SimpleExecutor(mode=RunningMode.Parallel, executors=Thread_Number)

... # Any code is the same

```

Program still could run without any refactoring and doesn't need to modify anything.


## Lock & Semaphore

For Lock feature, the native library threading should call acquire and release to control how it runs like this:

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

It also could use wih keyword "with":

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

With pyocean, it requires everyone should wrap the logic which needs to be run with lock to be a function,
and you just add a decorator on it.

```python
from pyocean.api import RunWith
import time

@RunWith.Lock
def lock_function():
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")

```

So is semaphore:

```python
from pyocean.api import RunWith
import time

@RunWith.Semaphore
def lock_function():
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")

```

Please remember: you still need to initial lock or semaphore object before you use it.

```python
from pyocean import SimpleExecutor, RunningMode
from pyocean.api import RunWith
from pyocean.adapter import Lock
import time

Thread_Number = 5

@RunWith.Lock
def lock_function():
    print("This is testing process with Lock and sleep for 3 seconds.")
    time.sleep(3)


if __name__ == '__main__':
    
        # Initialize Lock object
        __lock = Lock()

        # # # # Initial Executor object
        __executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=Thread_Number)

        # # # # Running the Executor
        __executor.run(
            function=lock_function,
            features=__lock)

```

