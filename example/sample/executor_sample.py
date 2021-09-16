# Import package pyocean
import pathlib
import random
import time
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

from pyocean import SimpleExecutor, RunningMode


def function(index):
    print(f"This isfunction with index {index}")
    time.sleep(3)
    return "Return Value"


executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
executor.run(function=function, args={"index": f"test_{random.randrange(1, 10)}"})
result = executor.result()
print(f"This is final result: {result}")
