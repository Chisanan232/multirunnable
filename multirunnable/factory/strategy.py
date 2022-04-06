from typing import Dict
from abc import ABCMeta

from ..framework.runnable.strategy import (
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    PoolRunnableStrategy as _PoolRunnableStrategy)
from .._import_utils import ImportMultiRunnable as _ImportMultiRunnable
from ..mode import RunningMode as _RunningMode



class BaseStrategyAdapter(metaclass=ABCMeta):

    def __init__(self, mode: _RunningMode):
        self._running_info: Dict[str, str] = mode.value
        self._module: str = self._running_info.get("strategy_module")



class ExecutorStrategyAdapter(BaseStrategyAdapter):

    def __init__(self, mode: _RunningMode, executors: int):
        super().__init__(mode=mode)
        self._executors_number = executors
        self.__strategy_cls_name: str = self._running_info.get("executor_strategy")


    def get_simple(self) -> _GeneralRunnableStrategy:
        __strategy_cls = _ImportMultiRunnable.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(executors=self._executors_number)
        # __strategy_instance = cast(Union[RunnableStrategy, AsyncRunnableStrategy], __strategy_instance)
        return __strategy_instance



class PoolStrategyAdapter(BaseStrategyAdapter):

    def __init__(self, mode: _RunningMode, pool_size: int):
        super().__init__(mode=mode)
        self._pool_size = pool_size
        self.__strategy_cls_name: str = self._running_info.get("pool_strategy")


    def get_simple(self) -> _PoolRunnableStrategy:
        __strategy_cls = _ImportMultiRunnable.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(pool_size=self._pool_size)
        return __strategy_instance

