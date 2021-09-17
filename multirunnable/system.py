from pyocean.mode import RunningMode as _RunningMode
from pyocean.manager import (
    OceanSimpleManager as _OceanSimpleWorker,
    OceanPersistenceManager as _OceanPersistenceWorker,
    OceanSimpleAsyncManager as _OceanSimpleAsyncWorker,
    OceanPersistenceAsyncManager as _OceanPersistenceAsyncWorker)
from pyocean.framework.task import BaseTask as _BaseTask, BaseQueueTask as _BaseQueueTask
from pyocean.framework.system import BaseSystem as _BaseSystem
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.persistence.interface import OceanPersistence as _OceanPersistence

from typing import List, Iterable, Callable, Optional, Union



class OceanSystem(_BaseSystem):

    def __init__(self, mode, worker_num):
        super(OceanSystem, self).__init__(mode=mode, worker_num=worker_num)


    def run(self,
            task: _BaseTask,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
            timeout: int = 0) -> [_OceanResult]:

        if self._mode is _RunningMode.Asynchronous:
            __ocean_worker = _OceanSimpleAsyncWorker(mode=self._mode, worker_num=self._worker_num)
            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features)
            __result = __ocean_worker.get_result()
            __ocean_worker.post_stop()
            return __result
        else:
            __ocean_worker = _OceanSimpleWorker(mode=self._mode, worker_num=self._worker_num)
            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features)
            __result = __ocean_worker.get_result()
            __ocean_worker.post_stop()
            return __result


    def run_and_save(self,
                     task: _BaseTask,
                     persistence_strategy: _OceanPersistence,
                     db_connection_num: int,
                     queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                     features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                     timeout: int = 0) -> [_OceanResult]:

        if self._mode is _RunningMode.Asynchronous:
            __ocean_worker = _OceanPersistenceAsyncWorker(
                mode=self._mode,
                worker_num=self._worker_num,
                persistence_strategy=persistence_strategy,
                db_connection_num=db_connection_num)

            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features)
            __result = __ocean_worker.get_result()
            __ocean_worker.post_stop()
            return __result
        else:
            __ocean_worker = _OceanPersistenceWorker(
                mode=self._mode,
                worker_num=self._worker_num,
                persistence_strategy=persistence_strategy,
                db_connection_num=db_connection_num)

            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features)
            __result = __ocean_worker.get_result()
            __ocean_worker.post_stop()
            return __result


    def map_by_params(self,
                      function: Callable,
                      args_iter: Iterable = [],
                      queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                      features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None):
        # __manager = _OceanMapManager(mode=self._mode)
        # __manager.map_by_param(function=function, args_iter=args_iter, queue_tasks=queue_tasks, features=features)
        pass


    def map_by_functions(self,
                         functions: List[Callable],
                         args_iter: Iterable = [],
                         queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                         features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None):
        # __manager = _OceanMapManager(mode=self._mode)
        # __manager.map_by_function(functions=functions, args_iter=args_iter, queue_tasks=queue_tasks, features=features)
        pass


    def start_new_worker(self, target: Callable, *args, **kwargs):
        # __manager = _OceanMapManager(mode=self._mode)
        # __manager.start_new_worker(target=target, *args, **kwargs)
        pass

