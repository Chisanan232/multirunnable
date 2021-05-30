from pyocean.framework import SimpleTaskFactory, PersistenceTaskFactory, RunnableStrategy
from pyocean.persistence.interface import OceanPersistence
from pyocean.concurrent.strategy import MultiThreadingStrategy

from abc import ABC



class MultiThreadsSimpleFactory(SimpleTaskFactory, ABC):

    def running_strategy(self) -> RunnableStrategy:
        return MultiThreadingStrategy(workers_num=self._process_num)



class MultiThreadsPersistenceFactory(PersistenceTaskFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return MultiThreadingStrategy(workers_num=self._process_num,
                                      db_connection_pool_size=self._db_connection_num,
                                      persistence_strategy=persistence_strategy)


