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

from multiprocessing import set_start_method as set_multiprocessing_start_method, get_start_method
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from platform import system as runtime_os
import logging
import re

if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) >= (3, 9):
    logging.info("Force 'multiprocessing' to use 'fork'.")
    if re.search(re.escape(runtime_os()), "Windows", re.IGNORECASE) is not None:
        # multiprocessing usage in Windows OS:
        # https://docs.python.org/3/library/multiprocessing.html#multiprocessing.get_all_start_methods
        # The key point is 'On Windows only 'spawn' is available.'. This is the reason why
        # this condition determine exists.
        set_multiprocessing_start_method('spawn', force=True)
    else:
        set_multiprocessing_start_method('fork', force=True)

from .context import context
from .strategy import ParallelStrategy, ProcessStrategy, ProcessPoolStrategy
from .synchronization import ProcessLock, ProcessCommunication
from .queue import Queue, SimpleQueue
from .result import ParallelResult
