"""
Set the customized Python package to Python Interpreter Environment Variable Path  so that we could import it if we need.
"""

from logging import getLogger
import getpass
import pathlib
import sys

# # Import pyocean package
__package_pyocean_path = str(pathlib.Path(__file__).parent.absolute())
sys.path.append(__package_pyocean_path)

# # Configure logging setting
__user = getpass.getuser()
PYOCEAN_LOGGER = getLogger(__user)


from pyocean.mode import RunningMode, FeatureMode
from pyocean.task import OceanTask, QueueTask
from pyocean.worker import (
    OceanSystem,
    OceanSimpleWorker, OceanPersistenceWorker,
    OceanSimpleAsyncWorker, OceanPersistenceAsyncWorker)
from pyocean.parallel import MultiProcessingStrategy, MultiProcessingQueueType, ParallelResult
from pyocean.concurrent import MultiThreadingStrategy, MultiThreadingQueueType, ConcurrentResult
from pyocean.coroutine import (
    MultiGreenletStrategy,
    GeventQueueType,
    CoroutineResult,
    AsynchronousStrategy,
    AsynchronousQueueType,
    AsynchronousResult)

