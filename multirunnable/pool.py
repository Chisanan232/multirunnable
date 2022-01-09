from abc import ABC
from typing import List, Tuple, Dict, Iterable, Callable, Optional, Union

from .framework import (
    BaseList as _BaseList,
    BaseQueueTask as _BaseQueueTask,
    BasePool as _BasePool,
    BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory,
    PoolRunnableStrategy as _PoolRunnableStrategy,
    Resultable as _Resultable,
    MRResult as _MRResult
)
from .mode import RunningMode as _RunningMode
from .adapter.strategy import PoolStrategyAdapter as _PoolStrategyAdapter
from ._config import set_mode


_Pool_Runnable_Type = Union[_PoolRunnableStrategy, _Resultable]
Pool_Runnable_Strategy: _Pool_Runnable_Type = None


class Pool(ABC, _BasePool):

    NotSupportError = Exception("Asynchronous not support Pool strategy.")

    def __init__(self, mode: _RunningMode, pool_size: int):
        if mode is _RunningMode.Asynchronous:
            raise self.NotSupportError

        set_mode(mode=mode)

        super(Pool, self).__init__(mode=mode, pool_size=pool_size)
        # self._initial_running_strategy()


    def __enter__(self):
        self.initial()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def initial(self,
                queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                *args, **kwargs):
        Pool_Runnable_Strategy.initialization(
            queue_tasks=queue_tasks, features=features, *args, **kwargs)


    def apply(self, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> None:
        Pool_Runnable_Strategy.apply(function=function, args=args, kwargs=kwargs)


    def async_apply(self,
                    function: Callable,
                    args: Tuple = (),
                    kwargs: Dict = {},
                    callback: Callable = None,
                    error_callback: Callable = None) -> None:
        Pool_Runnable_Strategy.async_apply(
            function=function,
            args=args,
            kwargs=kwargs,
            callback=callback,
            error_callback=error_callback)


    def map(self, function: Callable, args_iter: Iterable = (), chunksize: int = None) -> None:
        Pool_Runnable_Strategy.map(function=function, args_iter=args_iter, chunksize=chunksize)


    def async_map(self,
                  function: Callable,
                  args_iter: Iterable = (),
                  chunksize: int = None,
                  callback: Callable = None,
                  error_callback: Callable = None) -> None:
        Pool_Runnable_Strategy.async_map(
            function=function,
            args_iter=args_iter,
            chunksize=chunksize,
            callback=callback,
            error_callback=error_callback)


    def map_by_args(self, function: Callable, args_iter: Iterable[Iterable] = (), chunksize: int = None) -> None:
        Pool_Runnable_Strategy.map_by_args(function=function, args_iter=args_iter, chunksize=chunksize)


    def async_map_by_args(self,
                          function: Callable,
                          args_iter: Iterable[Iterable] = (),
                          chunksize: int = None,
                          callback: Callable = None,
                          error_callback: Callable = None) -> None:
        Pool_Runnable_Strategy.async_map_by_args(
            function=function,
            args_iter=args_iter,
            chunksize=chunksize,
            callback=callback,
            error_callback=error_callback)


    def imap(self, function: Callable, args_iter: Iterable = (), chunksize: int = 1) -> None:
        Pool_Runnable_Strategy.imap(function=function, args_iter=args_iter, chunksize=chunksize)


    def imap_unordered(self, function: Callable, args_iter: Iterable = (), chunksize: int = 1) -> None:
        Pool_Runnable_Strategy.imap_unordered(function=function, args_iter=args_iter, chunksize=chunksize)


    def close(self) -> None:
        Pool_Runnable_Strategy.close()


    def terminal(self) -> None:
        Pool_Runnable_Strategy.terminal()


    def get_result(self) -> List[_MRResult]:
        __result = Pool_Runnable_Strategy.get_result()
        return __result



class SimplePool(Pool):

    def __init__(self, mode: _RunningMode, pool_size: int, tasks_size: int):
        super().__init__(mode=mode, pool_size=pool_size)
        self._tasks_size = tasks_size
        self._initial_running_strategy()


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = _PoolStrategyAdapter(
            mode=self._mode,
            pool_size=self.pool_size,
            tasks_size=self._tasks_size)

        global Pool_Runnable_Strategy
        Pool_Runnable_Strategy = __running_strategy_adapter.get_simple()



class AdapterPool(Pool):

    def __init__(self, strategy: _Pool_Runnable_Type = None):
        super().__init__(mode=None, pool_size=strategy.pool_size)
        self.__strategy = strategy
        self._initial_running_strategy()


    def _initial_running_strategy(self) -> None:
        global Pool_Runnable_Strategy
        Pool_Runnable_Strategy = self.__strategy

