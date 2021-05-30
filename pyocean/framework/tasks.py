from pyocean.framework.factory import RunnableTaskFactory, SimpleTaskFactory, PersistenceTaskFactory
from pyocean.framework.strategy import RunnableStrategy
from pyocean.framework.builder import BaseRunnableBuilder
from pyocean.persistence.interface import OceanPersistence

from abc import ABC, ABCMeta, abstractmethod



class RunnableTask(metaclass=ABCMeta):

    def __init__(self, factory: RunnableTaskFactory):
        self._factory: RunnableTaskFactory = factory


    @abstractmethod
    def generate(self) -> BaseRunnableBuilder:
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
    def running_director(self, strategy: RunnableStrategy) -> BaseRunnableBuilder:
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


    def generate(self) -> BaseRunnableBuilder:
        # Initial the running program strategy
        _running_strategy = self.running_strategy()
        # Initial the running procedure builder
        _running_builder = self.running_director(strategy=_running_strategy)
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


    def generate(self) -> BaseRunnableBuilder:
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
        _running_builder = self.running_director(strategy=_running_strategy)
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

    def running_director(self, strategy: RunnableStrategy) -> BaseRunnableBuilder:
        _running_builder = self._factory.running_builder(running_strategy=strategy)
        return _running_builder


    def running_strategy(self) -> RunnableStrategy:
        _running_strategy = self._factory.running_strategy()
        return _running_strategy



class PersistenceRunnableTask(AbstractedPersistenceRunnableTask):

    def running_director(self, strategy: RunnableStrategy) -> BaseRunnableBuilder:
        _running_builder = self._factory.running_builder(running_strategy=strategy)
        return _running_builder


    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        _running_strategy = self._factory.running_strategy(persistence_strategy=persistence_strategy)
        return _running_strategy


    def running_persistence(self) -> OceanPersistence:
        _persistence_strategy = self._factory.persistence_strategy()
        return _persistence_strategy



class RunningTask:

    def __init__(self, process_number: int, db_connection_number: int, factory: RunnableTaskFactory):
        self._process_num: int = process_number
        self._db_connection_number: int = db_connection_number
        self._factory: RunnableTaskFactory = factory
        self._running_builder: BaseRunnableBuilder = None
        self._running_strategy: RunnableStrategy = None
        self._persistence_strategy: OceanPersistence = None


    def running_builder(self) -> BaseRunnableBuilder:
        """
        Description:
            Return running builder object.
        :return:
        """
        return self._running_builder


    def running_strategy(self) -> RunnableStrategy:
        """
        Description:
            Return running strategy object.
        :return:
        """
        return self._running_strategy


    def persistence(self) -> OceanPersistence:
        """
        Description:
            Return persistence strategy object.
        :return:
        """
        return self._persistence_strategy


    def generate(self) -> BaseRunnableBuilder:
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
        self._persistence_strategy = self._factory.persistence_strategy()
        # Initial the running program strategy
        self._running_strategy = self._factory.running_strategy(persistence_strategy=self._persistence_strategy)
        # Initial the running procedure builder
        self._running_builder = self._factory.running_builder(running_strategy=self._running_strategy)
        return self._running_builder
