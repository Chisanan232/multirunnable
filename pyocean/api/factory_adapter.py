from pyocean.framework import RunnableStrategy, BaseRunnableProcedure
from pyocean.framework.factory import (
    SimpleTaskFactory,
    PersistenceFileTaskFactory,
    PersistenceDatabaseTaskFactory)
from pyocean.framework.strategy import RunnableStrategy, AsyncRunnableStrategy
from pyocean.api.mode import RunningMode
from pyocean.api.operator_adapter import OperatorAdapter
from pyocean.api.strategy_adapter import StrategyAdapter
from pyocean._import_utils import ImportPyocean

from abc import ABCMeta, abstractmethod
from typing import Dict

from pyocean.persistence import OceanPersistence
from pyocean.persistence.interface import OceanDao, OceanFao



class BaseFactoryAdapter(metaclass=ABCMeta):

    def __init__(self, mode: RunningMode):
        self._running_info: Dict[str, str] = mode.value
        self._module: str = self._running_info.get("factory_module")



class FactoryAdapter(BaseFactoryAdapter):

    def __init__(self, mode: RunningMode):
        super().__init__(mode)
        self.__simple_factory_cls_name: str = self._running_info.get("simple_factory")
        self.__persistence_database_factory_cls_name: str = self._running_info.get("persistence_database_factory")
        self.__persistence_file_factory_cls_name: str = self._running_info.get("persistence_file_factory")


    def get_simple_factory(self) -> SimpleTaskFactory:
        __factory_cls = ImportPyocean.get_class(
            pkg_path=self._module, cls_name=self.__simple_factory_cls_name)
        __factory_instance: SimpleTaskFactory = __factory_cls()
        return __factory_instance


    def get_persistence_database_factory(self) -> PersistenceDatabaseTaskFactory:
        __factory_cls = ImportPyocean.get_class(
            pkg_path=self._module, cls_name=self.__persistence_database_factory_cls_name)
        __factory_instance: PersistenceDatabaseTaskFactory = __factory_cls()
        return __factory_instance


    def get_persistence_file_factory(self) -> PersistenceFileTaskFactory:
        __factory_cls = ImportPyocean.get_class(
            pkg_path=self._module, cls_name=self.__persistence_file_factory_cls_name)
        __factory_instance: PersistenceFileTaskFactory = __factory_cls()
        return __factory_instance



class AdapterSimpleFactory(SimpleTaskFactory):

    def __init__(self, mode: RunningMode, workers_number: int):
        super().__init__(workers_number=workers_number)
        self.strategy = StrategyAdapter(mode=mode, worker_num=workers_number)
        self.running_strategy = self.strategy.get_simple_strategy()
        self.operator = OperatorAdapter(mode=mode, strategy=self.running_strategy)


    def running_procedure(self, running_strategy: RunnableStrategy) -> BaseRunnableProcedure:
        return self.operator.get_operator()


    def running_strategy(self) -> RunnableStrategy:
        return self.running_strategy



class AdapterPersistenceFileFactory(PersistenceFileTaskFactory):

    def __init__(self, mode: RunningMode, workers_number: int, db_connection_number: int):
        super().__init__(workers_number=workers_number,
                         db_connection_number=db_connection_number)
        self.strategy = StrategyAdapter(mode=mode, worker_num=workers_number)
        self.running_strategy = self.strategy.get_simple_strategy()
        self.operator = OperatorAdapter(mode=mode, strategy=self.running_strategy)


    def running_procedure(self, running_strategy: RunnableStrategy) -> BaseRunnableProcedure:
        return self.operator.get_operator()


    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return self.running_strategy


    def persistence_strategy(self) -> OceanPersistence:
        pass


    def fao(self) -> OceanFao:
        pass



class AdapterPersistenceDatabaseFactory(PersistenceDatabaseTaskFactory):

    def __init__(self, mode: RunningMode, workers_number: int, db_connection_number: int):
        super().__init__(workers_number=workers_number,
                         db_connection_number=db_connection_number)
        self.strategy = StrategyAdapter(mode=mode, worker_num=workers_number)
        self.running_strategy = self.strategy.get_persistence_strategy(persistence_strategy=persistence_strategy, db_connection_num=db_connection_number)
        self.operator = OperatorAdapter(mode=mode, strategy=self.running_strategy)


    def running_procedure(self, running_strategy: RunnableStrategy) -> BaseRunnableProcedure:
        return self.operator.get_operator()


    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return self.running_strategy


    def persistence_strategy(self) -> OceanPersistence:
        pass


    def dao(self, connection_strategy: OceanPersistence) -> OceanDao:
        pass

