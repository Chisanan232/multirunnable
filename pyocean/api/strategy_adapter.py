from pyocean.framework.strategy import (
    RunnableStrategy,
    AsyncRunnableStrategy)
from pyocean.framework.features import BaseFeatureAdapterFactory
from pyocean.api.mode import RunningMode
from pyocean._import_utils import ImportPyocean

from abc import ABCMeta, abstractmethod
from typing import Dict, Union, cast



class BaseStrategyAdapter(metaclass=ABCMeta):

    def __init__(self, mode: RunningMode, worker_num: int, features_factory: BaseFeatureAdapterFactory = None):
        self._running_info: Dict[str, str] = mode.value
        self._module: str = self._running_info.get("strategy_module")
        self._process_num = worker_num
        self._features_factory = features_factory



class StrategyAdapter(BaseStrategyAdapter):

    def __init__(self, mode: RunningMode, worker_num: int, features_factory: BaseFeatureAdapterFactory = None):
        super().__init__(mode=mode, worker_num=worker_num, features_factory=features_factory)
        self.__strategy_cls_name: str = self._running_info.get("strategy")


    def get_simple_strategy(self) -> Union[RunnableStrategy, AsyncRunnableStrategy]:
        __strategy_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(workers_num=self._process_num, features_factory=self._features_factory)
        # __strategy_instance = cast(Union[RunnableStrategy, AsyncRunnableStrategy], __strategy_instance)
        return __strategy_instance


    def get_persistence_strategy(self, persistence_strategy, db_connection_num: int) -> Union[RunnableStrategy, AsyncRunnableStrategy]:
        __strategy_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(
            workers_num=self._process_num,
            features_factory=self._features_factory,
            db_connection_pool_size=db_connection_num,
            persistence_strategy=persistence_strategy)
        return __strategy_instance

