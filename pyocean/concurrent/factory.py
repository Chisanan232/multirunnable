from ..framework.factory import RunningFactory, RunningTask, RunnableStrategy
from ..persistence.interface import OceanPersistence
from .strategy import MultiThreadingStrategy, CoroutineStrategy

from abc import ABC



class MultiThreadsFactory(RunningFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return MultiThreadingStrategy(threads_num=self._process_num,
                                      db_connection_pool_size=self._db_connection_num,
                                      persistence_strategy=persistence_strategy)



class CoroutineFactory(RunningFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return CoroutineStrategy(threads_num=self._process_num,
                                 db_connection_pool_size=self._db_connection_num,
                                 persistence_strategy=persistence_strategy)



class ConcurrentRunningTask(RunningTask):

    def build(self):
        pass

