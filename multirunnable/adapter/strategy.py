from multirunnable.framework.task import BasePersistenceTask as _BasePersistenceTask
from multirunnable.framework.strategy import (
    RunnableStrategy as _RunnableStrategy,
    GeneralRunnableStrategy as _GeneralRunnableStrategy,
    PoolRunnableStrategy as _PoolRunnableStrategy,
    AsyncRunnableStrategy as _AsyncRunnableStrategy)
from multirunnable.persistence.interface import OceanPersistence as _OceanPersistence
from multirunnable.mode import RunningMode as _RunningMode
from multirunnable._import_utils import ImportMultiRunnable as _ImportMultiRunnable

from abc import ABCMeta
from typing import Dict, Union, Type, cast



class BaseStrategyAdapter(metaclass=ABCMeta):

    def __init__(self, mode: _RunningMode):
        self._running_info: Dict[str, str] = mode.value
        self._module: str = self._running_info.get("strategy_module")



class StrategyAdapter(BaseStrategyAdapter):

    def __init__(self, mode: _RunningMode, worker_num: int):
        super().__init__(mode=mode)
        self._process_num = worker_num
        self.__strategy_cls_name: str = self._running_info.get("strategy")


    def get_simple_strategy(self) -> Union[_RunnableStrategy, _AsyncRunnableStrategy]:
        __strategy_cls = _ImportMultiRunnable.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(workers_num=self._process_num)
        # __strategy_instance = cast(Union[RunnableStrategy, AsyncRunnableStrategy], __strategy_instance)
        return __strategy_instance


    def get_persistence_strategy(self,
                                 persistence_strategy: _OceanPersistence,
                                 db_connection_num: int) -> Union[_RunnableStrategy, _AsyncRunnableStrategy]:
        __strategy_cls = _ImportMultiRunnable.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(
            workers_num=self._process_num,
            db_connection_pool_size=db_connection_num,
            persistence_strategy=persistence_strategy)
        return __strategy_instance



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


    def get_persistence(self, persistence: _BasePersistenceTask) -> _GeneralRunnableStrategy:
        __strategy_cls = _ImportMultiRunnable.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(
            executors=self._executors_number,
            persistence=persistence)
        return __strategy_instance



class PoolStrategyAdapter(BaseStrategyAdapter):

    def __init__(self, mode: _RunningMode, pool_size: int, tasks_size: int):
        super().__init__(mode=mode)
        self._pool_size = pool_size
        self._tasks_size = tasks_size
        self.__strategy_cls_name: str = self._running_info.get("pool_strategy")


    def get_simple(self) -> _PoolRunnableStrategy:
        __strategy_cls = _ImportMultiRunnable.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(pool_size=self._pool_size, tasks_size=self._tasks_size)
        return __strategy_instance


    def get_persistence(self, persistence: _BasePersistenceTask) -> _PoolRunnableStrategy:
        __strategy_cls = _ImportMultiRunnable.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(
            pool_size=self._pool_size,
            tasks_size=self._tasks_size,
            persistence=persistence)
        return __strategy_instance

