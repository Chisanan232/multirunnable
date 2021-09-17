import pathlib
import time
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

from multirunnable import SimpleExecutor, RunningMode
from multirunnable.api import RunWith
from multirunnable.adapter import Lock

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
