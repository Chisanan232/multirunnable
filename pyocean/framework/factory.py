from .strategy import RunnableStrategy
from .builder import BaseBuilder
from ..persistence.interface import OceanPersistence
from ..persistence.database.access_object import BaseDao

from abc import ABCMeta, abstractmethod



class RunningFactory(metaclass=ABCMeta):

    def __init__(self, process_number: int, db_connection_number: int):
        self._process_num = process_number
        self._db_connection_num = db_connection_number


    @abstractmethod
    def running_builder(self, running_strategy: RunnableStrategy) -> BaseBuilder:
        """
        Description:
            Generate BaseBuilder type instance.
        :param running_strategy:
        :return:
        """
        pass


    @abstractmethod
    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        """
        Description:
            Generate RunnableStrategy type instance.
        :param persistence_strategy:
        :return:
        """
        pass


    @abstractmethod
    def persistence_strategy(self) -> OceanPersistence:
        """
        Description:
            Generate OceanPersistence type instance.
        :return:
        """
        pass


    @abstractmethod
    def dao(self, connection_strategy: OceanPersistence) -> BaseDao:
        """
        Description: (is it used?)
            Generate DAO instance.
        :param connection_strategy:
        :return:
        """
        pass



class RunningTask:

    def __init__(self, process_number: int, db_connection_number: int, factory: RunningFactory):
        self._process_num: int = process_number
        self._db_connection_number: int = db_connection_number
        self._factory: RunningFactory = factory
        self._running_builder: BaseBuilder = None
        self._running_strategy: RunnableStrategy = None
        self._persistence_strategy: OceanPersistence = None


    def running_builder(self) -> BaseBuilder:
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


    def generate(self) -> BaseBuilder:
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
