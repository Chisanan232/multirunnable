from pyocean.framework.operator import BaseRunnableProcedure
from pyocean.framework.strategy import RunnableStrategy
from pyocean.framework.factory import SimpleTaskFactory, PersistenceTaskFactory
from pyocean.persistence.interface import OceanPersistence
from pyocean.parallel.operator import ParallelProcedure
from pyocean.parallel.strategy import ParallelStrategy, MultiProcessingStrategy

from abc import ABC



class ParallelSimpleFactory(SimpleTaskFactory, ABC):

    def running_procedure(self, running_strategy: ParallelStrategy) -> BaseRunnableProcedure:
        __procedure = ParallelProcedure(running_strategy=running_strategy)
        return __procedure


    def running_strategy(self) -> RunnableStrategy:
        return MultiProcessingStrategy(workers_num=self._process_num)



class ParallelPersistenceFactory(PersistenceTaskFactory, ABC):

    def running_procedure(self, running_strategy: ParallelStrategy) -> BaseRunnableProcedure:
        __procedure = ParallelProcedure(running_strategy=running_strategy)
        return __procedure


    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return MultiProcessingStrategy(workers_num=self._process_num,
                                       db_connection_pool_size=self._db_connection_num,
                                       persistence_strategy=persistence_strategy)

