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
Currently, it has 4 options could use, and they are Parallel, Concurrent, Greenlet and Asynchronous.

Here's an example to do the same thing with pyocean:

```python
from pyocean import OceanTask, OceanSystem, RunningMode
import random

Thread_Number = 5


def function(index):
    print(f"This is function with index {index}")


if __name__ == '__main__':
    # Initialize task object
    task = OceanTask(mode=RunningMode.Concurrent)
    task.set_function(function=function)
    task.set_func_kwargs(kwargs={"index": f"test_{random.randrange(10, 20)}"})

    # Initialize ocean-system and assign task
    system = OceanSystem(mode=RunningMode.Concurrent, worker_num=Thread_Number)
    system.run(task=task)
```

First, it must initialize an OceanTask to let it know target function and its arguments if it needs.
Second, choose one strategy mode you need, for example above, we use Concurrent.
Finally, run it.

How about Parallel? I want to let it be more fast. 
Only one thing you need to do: change the mode.

```python

... # Any code is the same

system = OceanSystem(mode=RunningMode.Parallel, worker_num=Thread_Number)

... # Any code is the same

```

Program still could run without any refactoring and doesn't need to modify anything.
