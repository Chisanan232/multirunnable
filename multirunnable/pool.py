from abc import ABC
from typing import List, Tuple, Dict, Iterable, Callable, Optional, Union

from .framework import (
    BaseQueueTask as _BaseQueueTask,
    BasePool as _BasePool,
)
from .framework.runnable import (
    PoolRunnableStrategy as _PoolRunnableStrategy,
    Resultable as _Resultable,
    PoolResult as _PoolResult
)
from .framework.factory import (
    BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory,
    BaseList as _BaseList
)
from .mode import RunningMode as _RunningMode
from .factory.strategy import PoolStrategyAdapter as _PoolStrategyAdapter
from ._config import set_mode, get_current_mode
from ._utils import get_cls_name as _get_cls_name


_Pool_Runnable_Type = Union[_PoolRunnableStrategy, _Resultable]
Pool_Runnable_Strategy: _Pool_Runnable_Type = None


class Pool(ABC, _BasePool):

    NotSupportError = Exception("Asynchronous not support Pool strategy.")

    def __init__(self, pool_size: int):
        super(Pool, self).__init__(pool_size=pool_size)
        # self._initial_running_strategy()


    def __enter__(self):
        self.initial()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def initial(self, queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                *args, **kwargs):

        Pool_Runnable_Strategy.initialization(
            queue_tasks=queue_tasks, features=features, *args, **kwargs)


    def apply(self, tasks_size: int, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> None:
        Pool_Runnable_Strategy.apply(tasks_size=tasks_size, function=function, args=args, kwargs=kwargs)


    def async_apply(self, tasks_size: int, function: Callable, args: Tuple = (),
                    kwargs: Dict = {}, callback: Callable = None, error_callback: Callable = None) -> None:

        Pool_Runnable_Strategy.async_apply(
            tasks_size=tasks_size,
            function=function,
            args=args,
            kwargs=kwargs,
            callback=callback,
            error_callback=error_callback)


    def apply_with_iter(self, functions_iter: List[Callable], args_iter: List[Tuple] = None, kwargs_iter: List[Dict] = None) -> None:
        Pool_Runnable_Strategy.apply_with_iter(functions_iter=functions_iter, args_iter=args_iter, kwargs_iter=kwargs_iter)


    def async_apply_with_iter(self, functions_iter: List[Callable], args_iter: List[Tuple] = None,
                              kwargs_iter: List[Dict] = None, callback_iter: List[Callable] = None,
                              error_callback_iter: List[Callable] = None) -> None:

        Pool_Runnable_Strategy.async_apply_with_iter(
            functions_iter=functions_iter,
            args_iter=args_iter,
            kwargs_iter=kwargs_iter,
            callback_iter=callback_iter,
            error_callback_iter=error_callback_iter)


    def map(self, function: Callable, args_iter: Iterable = (), chunksize: int = None) -> None:
        Pool_Runnable_Strategy.map(function=function, args_iter=args_iter, chunksize=chunksize)


    def async_map(self, function: Callable, args_iter: Iterable = (), chunksize: int = None,
                  callback: Callable = None, error_callback: Callable = None) -> None:

        Pool_Runnable_Strategy.async_map(
            function=function,
            args_iter=args_iter,
            chunksize=chunksize,
            callback=callback,
            error_callback=error_callback)


    def map_by_args(self, function: Callable, args_iter: Iterable[Iterable] = (), chunksize: int = None) -> None:
        Pool_Runnable_Strategy.map_by_args(function=function, args_iter=args_iter, chunksize=chunksize)


    def async_map_by_args(self, function: Callable, args_iter: Iterable[Iterable] = (), chunksize: int = None,
                          callback: Callable = None, error_callback: Callable = None) -> None:

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


    def get_result(self) -> List[_PoolResult]:
        __result = Pool_Runnable_Strategy.get_result()
        return __result



class SimplePool(Pool):

    def __init__(self, pool_size: int, mode: _RunningMode = None):
        if mode is _RunningMode.Asynchronous:
            raise self.NotSupportError

        if mode is not None:
            if isinstance(mode, _RunningMode) is not True:
                raise TypeError("The option *mode* should be one of 'multirunnable.mode.RunningMode'.")

            set_mode(mode=mode)
            self._mode = mode
        else:
            self._mode = get_current_mode(force=True)

        super().__init__(pool_size=pool_size)
        self._initial_running_strategy()


    def __repr__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(" \
                               f"mode={self._mode}, " \
                               f"pool_size={self.pool_size})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = _PoolStrategyAdapter(
            mode=self._mode,
            pool_size=self.pool_size)

        global Pool_Runnable_Strategy
        Pool_Runnable_Strategy = __running_strategy_adapter.get_simple()



class AdapterPool(Pool):

    def __init__(self, strategy: _Pool_Runnable_Type = None):
        super().__init__(pool_size=strategy.pool_size)
        self.__strategy = strategy
        self._initial_running_strategy()


    def _initial_running_strategy(self) -> None:
        global Pool_Runnable_Strategy
        Pool_Runnable_Strategy = self.__strategy

