from pyocean.framework import SimpleTaskFactory, PersistenceTaskFactory, RunnableStrategy
from pyocean.persistence.interface import OceanPersistence
from pyocean.parallel.strategy import MultiProcessingStrategy

from abc import ABC



class ParallelSimpleFactory(SimpleTaskFactory, ABC):

    def running_strategy(self) -> RunnableStrategy:
        return MultiProcessingStrategy(workers_num=self._process_num)



class ParallelPersistenceFactory(PersistenceTaskFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return MultiProcessingStrategy(workers_num=self._process_num,
                                       db_connection_pool_size=self._db_connection_num,
                                       persistence_strategy=persistence_strategy)

