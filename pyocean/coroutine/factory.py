from pyocean.framework.factory import RunningFactory, RunningTask, RunnableStrategy
from pyocean.persistence.interface import OceanPersistence
from pyocean.coroutine.strategy import GeventStrategy, AsynchronousStrategy

from abc import ABC



class GeventFactory(RunningFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return GeventStrategy(threads_num=self._process_num,
                              db_connection_pool_size=self._db_connection_num,
                              persistence_strategy=persistence_strategy)



class AsynchronousFactory(RunningFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return AsynchronousStrategy(threads_num=self._process_num,
                                    db_connection_pool_size=self._db_connection_num,
                                    persistence_strategy=persistence_strategy)



class CoroutineRunningTask(RunningTask):

    def build(self):
        pass

