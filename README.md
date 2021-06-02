# pyocean
A Python framework integrates building program multi-worker with different running strategy.
It could very easily build a feature running multi-work simultaneously.

Python is a high level program language but it's free to let anyone choice which running strategy you want to use.
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

But it could implement concurrent feature more easier with pyocean:

```python
from pyocean.concurrent import ConcurrentProcedure, MultiThreadingStrategy
import random


Thread_Number = 5

def function(index):
    print(f"This is function with index {index}")


if __name__ == '__main__':

    _builder = ConcurrentProcedure(running_strategy=MultiThreadingStrategy(workers_num=Thread_Number))
    _builder.run(function=function, fun_kwargs={"index": f"test_{random.randrange(1, 10)}"})
```

Obviously, it just only 2 lines code to implement easy concurrent feature.
