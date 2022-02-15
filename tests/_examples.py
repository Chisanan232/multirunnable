from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from multirunnable.mode import RunningMode, FeatureMode
from multirunnable.factory.strategy import ExecutorStrategyAdapter, PoolStrategyAdapter

from typing import List
import asyncio

from .test_config import Worker_Size


_Worker_Size = Worker_Size


def run_multi_process(_function):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Parallel, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _run_with_multiple_workers(_strategy, _function)


def run_multi_threads(_function):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Concurrent, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _run_with_multiple_workers(_strategy, _function)


def run_multi_green_thread(_function):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.GreenThread, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _run_with_multiple_workers(_strategy, _function)


def run_async(_function, event_loop=None, _feature=None):

    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    async def __process():
        await _strategy.initialization(queue_tasks=None, features=_feature, event_loop=event_loop)
        _ps = [_strategy.generate_worker(_function) for _ in range(_Worker_Size)]
        await _strategy.activate_workers(_ps)

    if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION > 6:
        asyncio.run(__process())
    else:
        _event_loop = asyncio.get_event_loop()
        _event_loop.run_until_complete(__process())


def _run_with_multiple_workers(_strategy, _function):
    _ps = [_strategy.generate_worker(_function) for _ in range(_Worker_Size)]
    _strategy.activate_workers(_ps)
    _strategy.close(_ps)


def map_multi_process(_functions: List):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Parallel, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _map_with_multiple_workers(_strategy, _functions)


def map_multi_threads(_functions: List):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Concurrent, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _map_with_multiple_workers(_strategy, _functions)


def map_multi_green_thread(_functions: List):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.GreenThread, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()

    _map_with_multiple_workers(_strategy, _functions)


def map_async(_functions: List, _feature=None):
    _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
    _strategy = _strategy_adapter.get_simple()
    _strategy.map_with_function(functions=_functions, features=_feature)


def _map_with_multiple_workers(_strategy, _functions: List):
    _ps = [_strategy.generate_worker(_f) for _f in _functions]
    _strategy.activate_workers(_ps)
    _strategy.close(_ps)


