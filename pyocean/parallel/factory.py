from pyocean.framework import RunningFactory, RunningTask, RunnableStrategy
from pyocean.persistence.interface import OceanPersistence
from pyocean.parallel import MultiProcessingStrategy

from abc import ABC



class ParallelFactory(RunningFactory, ABC):

    def running_strategy(self, persistence_strategy: OceanPersistence) -> RunnableStrategy:
        return MultiProcessingStrategy(threads_num=self._process_num,
                                       db_connection_pool_size=self._db_connection_num,
                                       persistence_strategy=persistence_strategy)



class ParallelRunningTask(RunningTask):

    def build(self):
        pass

