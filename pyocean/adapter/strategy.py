from pyocean.framework.strategy import (
    RunnableStrategy as _RunnableStrategy,
    AsyncRunnableStrategy as _AsyncRunnableStrategy,
    BaseMapStrategy as _BaseMapStrategy)
from pyocean.persistence.interface import OceanPersistence
from pyocean.mode import RunningMode as _RunningMode
from pyocean._import_utils import ImportPyocean as _ImportPyocean

from abc import ABCMeta
from typing import Dict, Union, cast



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
        __strategy_cls = _ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(workers_num=self._process_num)
        # __strategy_instance = cast(Union[RunnableStrategy, AsyncRunnableStrategy], __strategy_instance)
        return __strategy_instance


    def get_persistence_strategy(self,
                                 persistence_strategy: OceanPersistence,
                                 db_connection_num: int) -> Union[_RunnableStrategy, _AsyncRunnableStrategy]:
        __strategy_cls = _ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__strategy_cls_name)
        __strategy_instance = __strategy_cls(
            workers_num=self._process_num,
            db_connection_pool_size=db_connection_num,
            persistence_strategy=persistence_strategy)
        return __strategy_instance



class MapStrategyAdapter(BaseStrategyAdapter):

    def __init__(self, mode: _RunningMode):
        super().__init__(mode=mode)
        self.__map_strategy_cls_name: str = self._running_info.get("map_strategy")


    def get_map_strategy(self) -> Union[_BaseMapStrategy]:
        __strategy_cls = _ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__map_strategy_cls_name)
        __strategy_instance = __strategy_cls()
        return __strategy_instance

