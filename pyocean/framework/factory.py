from pyocean.framework import BaseRunnableBuilder, RunnableStrategy
from pyocean.persistence.interface import OceanPersistence
from pyocean.persistence.database.access_object import BaseDao

from abc import ABC, ABCMeta, abstractmethod



class RunnableTaskFactory(metaclass=ABCMeta):

    def __init__(self, workers_number: int):
        self._process_num = workers_number


    @abstractmethod
    def running_builder(self, running_strategy: RunnableStrategy) -> BaseRunnableBuilder:
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
    def dao(self, connection_strategy: OceanPersistence) -> BaseDao:
        """
        Description: (is it used?)
            Generate DAO instance.
        :param connection_strategy:
        :return:
        """
        pass

