from pyocean.framework.factory import RunningFactory, RunningTask, RunnableStrategy
from pyocean.persistence.interface import OceanPersistence
from pyocean.concurrent.strategy import MultiThreadingStrategy

from abc import ABC



class MultiThreadsFactory(RunningFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return MultiThreadingStrategy(threads_num=self._process_num,
                                      db_connection_pool_size=self._db_connection_num,
                                      persistence_strategy=persistence_strategy)



class ConcurrentRunningTask(RunningTask):

    def build(self):
        pass

