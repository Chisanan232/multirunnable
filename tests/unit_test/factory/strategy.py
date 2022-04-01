from multirunnable.concurrent.strategy import ThreadStrategy, ThreadPoolStrategy
from multirunnable.coroutine.strategy import GreenThreadStrategy, GreenThreadPoolStrategy, AsynchronousStrategy
from multirunnable.parallel.strategy import ProcessStrategy, ProcessPoolStrategy
from multirunnable.factory.strategy import ExecutorStrategyAdapter, PoolStrategyAdapter
from multirunnable.mode import RunningMode

from ...test_config import Worker_Size, Worker_Pool_Size, Task_Size


_Worker_Size = Worker_Size
_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size



class TestAdapterExecuteStrategy:

    def test_get_simple_with_parallel(self):
        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Parallel, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()
        assert isinstance(_strategy, ProcessStrategy) is True, "The type of strategy instance should be 'ProcessStrategy'."


    def test_get_simple_with_concurrent(self):
        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Concurrent, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()
        assert isinstance(_strategy, ThreadStrategy) is True, "The type of strategy instance should be 'ThreadStrategy'."


    def test_get_simple_with_coroutine(self):
        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.GreenThread, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()
        assert isinstance(_strategy, GreenThreadStrategy) is True, "The type of strategy instance should be 'GreenThreadStrategy'."


    def test_get_simple_with_asynchronous(self):
        _strategy_adapter = ExecutorStrategyAdapter(mode=RunningMode.Asynchronous, executors=_Worker_Size)
        _strategy = _strategy_adapter.get_simple()
        assert isinstance(_strategy, AsynchronousStrategy) is True, "The type of strategy instance should be 'AsynchronousStrategy'."



class TestAdapterPoolStrategy:

    def test_get_simple_with_parallel(self):
        _strategy_adapter = PoolStrategyAdapter(mode=RunningMode.Parallel, pool_size=_Worker_Pool_Size)
        _strategy = _strategy_adapter.get_simple()
        assert isinstance(_strategy, ProcessPoolStrategy) is True, "The type of strategy instance should be 'ProcessPoolStrategy'."


    def test_get_simple_with_concurrent(self):
        _strategy_adapter = PoolStrategyAdapter(mode=RunningMode.Concurrent, pool_size=_Worker_Pool_Size)
        _strategy = _strategy_adapter.get_simple()
        assert isinstance(_strategy, ThreadPoolStrategy) is True, "The type of strategy instance should be 'ThreadPoolStrategy'."


    def test_get_simple_with_coroutine(self):
        _strategy_adapter = PoolStrategyAdapter(mode=RunningMode.GreenThread, pool_size=_Worker_Pool_Size)
        _strategy = _strategy_adapter.get_simple()
        assert isinstance(_strategy, GreenThreadPoolStrategy) is True, "The type of strategy instance should be 'GreenThreadPoolStrategy'."

