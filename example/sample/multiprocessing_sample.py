# Import package pyocean
import pathlib
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

from pyocean.parallel import ParallelProcedure, MultiProcessingStrategy
import random


def function(index):
    print(f"This isfunction with index {index}")
    return "Return Value"


_builder = ParallelProcedure(running_strategy=MultiProcessingStrategy(workers_num=3))
_builder.run(function=function, fun_kwargs={"index": f"test_{random.randrange(1, 10)}"})
result = _builder.result
print(f"This is final result: {result}")
