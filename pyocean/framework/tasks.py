from pyocean.framework.operator import BaseRunnableProcedure
from pyocean.framework.strategy import RunnableStrategy
from pyocean.framework.factory import RunnableTaskFactory, SimpleTaskFactory, PersistenceTaskFactory
from pyocean.persistence.interface import OceanPersistence

from abc import ABC, ABCMeta, abstractmethod



class RunnableTask(metaclass=ABCMeta):

    def __init__(self, factory: RunnableTaskFactory):
        self._factory: RunnableTaskFactory = factory


    @abstractmethod
    def generate(self) -> BaseRunnableProcedure:
        """
        Description:
            generate a running task.
        Note:
            This method unifies the all of object which be needed to initialize before developer to use. Obviously, it be
            implement via Facade Pattern. User just only need to focus the configurations (like how many number of
            process or thread to use, etc.) and implementation details (like persistence strategy implement of MySQL).
        :return:
        """
        pass


    @abstractmethod
    def running_procedure(self, strategy: RunnableStrategy) -> BaseRunnableProcedure:
        """
        Description:
            Return running builder object.
        :return:
        """
        pass



class AbstractedSimpleRunnableTask(RunnableTask, ABC):

    def __init__(self, factory: SimpleTaskFactory):
        super().__init__(factory)
        self._factory: SimpleTaskFactory = factory


    def generate(self) -> BaseRunnableProcedure:
        # Initial the running program strategy
        _running_strategy = self.running_strategy()
        # Initial the running procedure builder
        _running_builder = self.running_procedure(strategy=_running_strategy)
        return _running_builder


    @abstractmethod
    def running_strategy(self) -> RunnableStrategy:
        """
        Description:
            Return running strategy object.
        :return:
        """
        pass



class AbstractedPersistenceRunnableTask(RunnableTask, ABC):

    def __init__(self, factory: PersistenceTaskFactory):
        super().__init__(factory)
        self._factory: PersistenceTaskFactory = factory


    def generate(self) -> BaseRunnableProcedure:
        """
        Description:
            generate a running task.
        Note:
            This method unifies the all of object which be needed to initialize before developer to use. Obviously, it be
            implement via Facade Pattern. User just only need to focus the configurations (like how many number of
            process or thread to use, etc.) and implementation details (like persistence strategy implement of MySQL).
        :return:
        """
        # Initial the database connection building strategy
        _persistence_strategy = self.running_persistence()
        # Initial the running program strategy
        _running_strategy = self.running_strategy(persistence_strategy=_persistence_strategy)
        # Initial the running procedure builder
        _running_builder = self.running_procedure(strategy=_running_strategy)
        return _running_builder


    @abstractmethod
    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        """
        Description:
            Return running strategy object.
        :return:
        """
        pass


    @abstractmethod
    def running_persistence(self) -> OceanPersistence:
        """
        Description:
            Return persistence strategy object.
        :return:
        """
        pass



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

