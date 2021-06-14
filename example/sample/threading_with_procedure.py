# Import package pyocean
import pathlib
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

from pyocean.concurrent import ConcurrentProcedure, MultiThreadingStrategy
import random


Thread_Number = 5


def function(index):
    print(f"This is function with index {index}")


if __name__ == '__main__':

    _builder = ConcurrentProcedure(running_strategy=MultiThreadingStrategy(workers_num=Thread_Number))
    _builder.run(function=function, fun_kwargs={"index": f"test_{random.randrange(1, 10)}"})
