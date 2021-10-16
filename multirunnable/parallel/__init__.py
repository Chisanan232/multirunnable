"""
https://github.com/tarantool/test-run/issues/265

Scenario:
The function '_target_function' cannot be work anymore in Python 3.9 up.

Code:
        @wraps(target)
        @ParallelStrategy.save_return_value
        def _target_function(*_args, **_kwargs):
            result_value = target(*_args, **_kwargs)
            return result_value

        return Process(target=_target_function, args=args, kwargs=kwargs)

Note:
In Python 3.9 up version, the package 'multiprocessing' only
receives target function which is pickleable. In other words,
it means that you couldn't set decorator  like 'classmethod' or
'staticmethod' at any function which targets to run Parallel.

Solution:
It needs to configure 'set_start_method' value to be 'fork' to
let it work around.
"""

from multiprocessing import set_start_method as set_multiprocessing_start_method
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
import logging

if PYTHON_MAJOR_VERSION == 3:
    if PYTHON_MINOR_VERSION >= 9:
        logging.info("Force 'multiprocessing' to use 'fork'.")
        set_multiprocessing_start_method('fork')
else:
    from ..exceptions import VersionError
    raise VersionError

from multirunnable.parallel.features import MultiProcessingQueueType, ProcessLock, ProcessCommunication
from multirunnable.parallel.strategy import ParallelStrategy, ProcessStrategy, ProcessPoolStrategy
from multirunnable.parallel.result import ParallelResult
