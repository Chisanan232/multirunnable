from multirunnable.framework.api.operator import BaseRunnableProcedure, RunnableStrategy
from multirunnable.persistence.interface import OceanPersistence, OceanDao, OceanFao

from abc import ABCMeta, abstractmethod



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

    """
    Factory including Persistence strategy generator method.
    """

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



class PersistenceDatabaseTaskFactory(PersistenceTaskFactory):

    """
    Persistence strategy used by saving data into database and
    there is a generator method to generate DAO (Database Access Object).
    """

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



class PersistenceFileTaskFactory(PersistenceTaskFactory):

    """
    Persistence strategy used by saving data as target formatter
    file and there is a method generate FAO (File Access Object).
    """

    @abstractmethod
    def fao(self) -> OceanFao:
        """
        Description: (is it used?)
            Generate FAO instance.
        :return:
        """
        pass

