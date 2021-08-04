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


from pyocean.api import RunningMode, FeatureMode, Feature
from pyocean.task import OceanTask, QueueTask
from pyocean.worker import (
    OceanSystem,
    OceanSimpleWorker, OceanPersistenceWorker,
    OceanAsyncWorker, OceanPersistenceAsyncWorker)
from pyocean.parallel import (
    ParallelProcedure,
    ParallelStrategy,
    MultiProcessingStrategy,
    MultiProcessingQueueType,
    ParallelResult,
    ParallelSimpleFactory,
    ParallelPersistenceFactory)
from pyocean.concurrent import (
    ConcurrentProcedure,
    MultiThreadingStrategy,
    MultiThreadingQueueType,
    ConcurrentResult,
    ConcurrentSimpleFactory,
    ConcurrentPersistenceFactory)
from pyocean.coroutine import (
    GeventProcedure,
    MultiGreenletStrategy,
    GeventQueueType,
    CoroutineResult,
    GeventSimpleFactory,
    GeventPersistenceFactory,
    AsynchronousProcedure,
    AsynchronousStrategy,
    AsynchronousQueueType,
    AsynchronousResult,
    AsynchronousSimpleFactory,
    AsynchronousPersistenceFactory)

