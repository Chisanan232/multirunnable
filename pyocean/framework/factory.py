from pyocean.framework import BaseRunnableProcedure, RunnableStrategy
from pyocean.persistence.interface import OceanPersistence, OceanDao

from abc import ABC, ABCMeta, abstractmethod



class RunnableTaskFactory(metaclass=ABCMeta):

    def __init__(self, workers_number: int):
        self._process_num = workers_number


    @abstractmethod
    def running_procedure(self, running_strategy: RunnableStrategy) -> BaseRunnableProcedure:
        """
        Description:
            Generate BaseBuilder type instance.
        :param running_strategy:
        :return:
        """
        pass



class SimpleTaskFactory(RunnableTaskFactory):

    @abstractmethod
    def running_strategy(self) -> RunnableStrategy:
        """
        Description:
            Generate RunnableStrategy type instance.
        :return:
        """
        pass



class PersistenceTaskFactory(RunnableTaskFactory):

    def __init__(self, workers_number: int, db_connection_number: int):
        super().__init__(workers_number)
        self._db_connection_num = db_connection_number

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
    def dao(self, connection_strategy: OceanPersistence) -> OceanDao:
        """
        Description: (is it used?)
            Generate DAO instance.
        :param connection_strategy:
        :return:
        """
        pass

