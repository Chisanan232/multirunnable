from pyocean.framework.operator import BaseRunnableProcedure
from pyocean.framework.tasks import AbstractedSimpleRunnableTask, AbstractedPersistenceRunnableTask
from pyocean.framework.strategy import RunnableStrategy
from pyocean.persistence.interface import OceanPersistence



class SimpleRunnableTask(AbstractedSimpleRunnableTask):

    def running_procedure(self, strategy: RunnableStrategy) -> BaseRunnableProcedure:
        _running_procedure = self._factory.running_procedure(running_strategy=strategy)
        return _running_procedure


    def running_strategy(self) -> RunnableStrategy:
        _running_strategy = self._factory.running_strategy()
        return _running_strategy



class PersistenceRunnableTask(AbstractedPersistenceRunnableTask):

    def running_procedure(self, strategy: RunnableStrategy) -> BaseRunnableProcedure:
        _running_procedure = self._factory.running_procedure(running_strategy=strategy)
        return _running_procedure


    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        _running_strategy = self._factory.running_strategy(persistence_strategy=persistence_strategy)
        return _running_strategy


    def running_persistence(self) -> OceanPersistence:
        _persistence_strategy = self._factory.persistence_strategy()
        return _persistence_strategy

