from .factory import RunningFactory
from .strategy import RunnableStrategy
from .builder import BaseRunnableBuilder
from ..persistence.interface import OceanPersistence

from abc import ABCMeta, abstractmethod



class RunningTask:

    def __init__(self, process_number: int, db_connection_number: int, factory: RunningFactory):
        self._process_num: int = process_number
        self._db_connection_number: int = db_connection_number
        self._factory: RunningFactory = factory
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
