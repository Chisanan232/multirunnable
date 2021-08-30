from pyocean.framework.task import BaseTask as _BaseTask, BaseQueueTask as _BaseQueueTask
from pyocean.framework.manager import BaseSystem as _BaseSystem
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.mode import RunningMode as _RunningMode
from pyocean.persistence.interface import OceanPersistence as _OceanPersistence
from pyocean.manager import (
    OceanSimpleManager as _OceanSimpleWorker,
    OceanPersistenceManager as _OceanPersistenceWorker,
    OceanSimpleAsyncManager as _OceanSimpleAsyncWorker,
    OceanPersistenceAsyncManager as _OceanPersistenceAsyncWorker)

from typing import Optional, Union



class OceanSystem(_BaseSystem):

    def run(self,
            task: _BaseTask,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
            saving_mode: bool = False,
            timeout: int = 0) -> [_OceanResult]:

        if self._mode is _RunningMode.Asynchronous:
            __ocean_worker = _OceanSimpleAsyncWorker(mode=self._mode, worker_num=self._worker_num)
            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features, saving_mode=saving_mode)
            return __ocean_worker.get_result()
        else:
            __ocean_worker = _OceanSimpleWorker(mode=self._mode, worker_num=self._worker_num)
            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features, saving_mode=saving_mode)
            return __ocean_worker.get_result()


    def run_and_save(self,
                     task: _BaseTask,
                     persistence_strategy: _OceanPersistence,
                     db_connection_num: int,
                     queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                     features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                     saving_mode: bool = False,
                     timeout: int = 0) -> [_OceanResult]:

        if self._mode is _RunningMode.Asynchronous:
            __ocean_worker = _OceanPersistenceAsyncWorker(
                mode=self._mode,
                worker_num=self._worker_num,
                persistence_strategy=persistence_strategy,
                db_connection_num=db_connection_num)

            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features, saving_mode=saving_mode)
            return __ocean_worker.get_result()
        else:
            __ocean_worker = _OceanPersistenceWorker(
                mode=self._mode,
                worker_num=self._worker_num,
                persistence_strategy=persistence_strategy,
                db_connection_num=db_connection_num)

            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features, saving_mode=saving_mode)
            return __ocean_worker.get_result()


    def dispatcher(self):
        pass


    def terminate(self):
        pass

