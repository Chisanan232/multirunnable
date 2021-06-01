from pyocean.framework.operator import BaseRunnableProcedure
from pyocean.framework.strategy import RunnableStrategy
from pyocean.framework.factory import SimpleTaskFactory, PersistenceTaskFactory
from pyocean.persistence.interface import OceanPersistence
from pyocean.concurrent.operator import ConcurrentProcedure
from pyocean.concurrent.strategy import MultiThreadingStrategy

from abc import ABC



class MultiThreadsSimpleFactory(SimpleTaskFactory, ABC):

    def running_procedure(self, running_strategy: RunnableStrategy) -> BaseRunnableProcedure:
        __procedure = ConcurrentProcedure(running_strategy=running_strategy)
        return __procedure


    def running_strategy(self) -> RunnableStrategy:
        return MultiThreadingStrategy(workers_num=self._process_num)



class MultiThreadsPersistenceFactory(PersistenceTaskFactory, ABC):

    def running_procedure(self, running_strategy: RunnableStrategy) -> BaseRunnableProcedure:
        __procedure = ConcurrentProcedure(running_strategy=running_strategy)
        return __procedure


    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return MultiThreadingStrategy(workers_num=self._process_num,
                                      db_connection_pool_size=self._db_connection_num,
                                      persistence_strategy=persistence_strategy)


