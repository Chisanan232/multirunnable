from pyocean.framework import SimpleTaskFactory, PersistenceTaskFactory, RunnableStrategy
from pyocean.persistence.interface import OceanPersistence
from pyocean.coroutine.strategy import GeventStrategy, AsynchronousStrategy

from abc import ABC



class GeventSimpleFactory(SimpleTaskFactory, ABC):

    def running_strategy(self) -> RunnableStrategy:
        return GeventStrategy(workers_num=self._process_num)



class GeventPersistenceFactory(PersistenceTaskFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return GeventStrategy(workers_num=self._process_num,
                              db_connection_pool_size=self._db_connection_num,
                              persistence_strategy=persistence_strategy)



class AsynchronousSimpleFactory(SimpleTaskFactory, ABC):

    def running_strategy(self) -> RunnableStrategy:
        return AsynchronousStrategy(workers_num=self._process_num)



class AsynchronousPersistenceFactory(PersistenceTaskFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return AsynchronousStrategy(workers_num=self._process_num,
                                    db_connection_pool_size=self._db_connection_num,
                                    persistence_strategy=persistence_strategy)

