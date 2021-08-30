from pyocean.framework.task import BaseTask as _BaseTask, BaseQueueTask as _BaseQueueTask
from pyocean.framework.manager import (
    BaseManager as _BaseManager,
    BaseAsyncManager as _BaseAsyncManager,
    BaseSystem as _BaseSystem)
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.strategy import (
    RunnableStrategy as _RunnableStrategy,
    AsyncRunnableStrategy as _AsyncRunnableStrategy,
    Resultable as _Resultable)
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.mode import RunningMode as _RunningMode
from pyocean.api.decorator import ReTryMechanism as _ReTryMechanism
from pyocean.adapter.strategy import StrategyAdapter as _StrategyAdapter
from pyocean.persistence.interface import OceanPersistence as _OceanPersistence

from abc import ABC
from typing import Tuple, Dict, Optional, Union


Running_Strategy: Union[_RunnableStrategy, _AsyncRunnableStrategy] = None


class OceanManager(ABC, _BaseManager):

    def __init__(self, mode: _RunningMode, worker_num: int):
        super(OceanManager, self).__init__(mode=mode, worker_num=worker_num)

        self._initial_running_strategy()


    @property
    def running_timeout(self) -> int:
        return self._Worker_Timeout


    @running_timeout.setter
    def running_timeout(self, timeout: int) -> None:
        self._Worker_Timeout = timeout


    def start(self,
              task: _BaseTask,
              queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
              features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
              saving_mode: bool = False,
              init_args: Tuple = (), init_kwargs: Dict = {}) -> [_OceanResult]:

        __worker_run_time = 0
        __worker_run_finish = None

        while __worker_run_time < self.running_timeout + 1:
            try:
                self.pre_activate(queue_tasks=queue_tasks, features=features, *init_args, **init_kwargs)
                self.activate(task=task, saving_mode=saving_mode)
            except Exception as e:
                self.pre_stop(e=e)
                __worker_run_finish = False
            else:
                self.post_done()
                self.post_stop()
                __worker_run_finish = True
            finally:
                if __worker_run_finish is True:
                    break
                __worker_run_time += 1
        else:
            self.post_done()
            self.post_stop()


    def pre_activate(self,
                     queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                     features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                     *args, **kwargs) -> None:
        Running_Strategy.initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)


    def activate(self, task: _BaseTask, saving_mode: bool = False) -> None:
        if saving_mode is True:
            _kwargs = {"task": task}
            __worker_list = Running_Strategy.build_workers(function=self.run_task, **_kwargs)
        else:
            __worker_list = Running_Strategy.build_workers(function=task.function, *task.func_args, **task.func_kwargs)
        Running_Strategy.activate_workers(workers_list=__worker_list)


    @_ReTryMechanism.task
    def run_task(self, task: _BaseTask) -> [_OceanResult]:
        result = task.function(*task.func_args, **task.func_kwargs)
        return result


    def pre_stop(self, e: Exception) -> None:
        raise e


    def post_stop(self) -> None:
        Running_Strategy.close()


    def post_done(self) -> None:
        pass


    def get_result(self) -> [_OceanResult]:
        if isinstance(Running_Strategy, _Resultable):
            return Running_Strategy.get_result()
        else:
            return []



class OceanAsyncWorker(_BaseAsyncManager):

    _Initial_Object = None
    _Target_Function = None

    def __init__(self, mode: _RunningMode, worker_num: int):
        super(OceanAsyncWorker, self).__init__(mode=mode, worker_num=worker_num)

        self._initial_running_strategy()


    def _initial_running_strategy(self) -> None:
        pass


    @property
    def running_timeout(self) -> int:
        return self._Worker_Timeout


    @running_timeout.setter
    def running_timeout(self, timeout: int) -> None:
        self._Worker_Timeout = timeout


    def start(self,
              task: _BaseTask,
              queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
              features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
              saving_mode: bool = False,
              init_args: Tuple = (), init_kwargs: Dict = {}) -> None:

        __event_loop = Running_Strategy.get_event_loop()
        init_kwargs["event_loop"] = __event_loop
        __event_loop.run_until_complete(
            future=self.async_process(
                task=task,
                queue_tasks=queue_tasks,
                features=features,
                saving_mode=saving_mode,
                init_args=init_args, init_kwargs=init_kwargs
            ))
        self.post_stop()


    async def async_process(self,
                            task: _BaseTask,
                            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                            saving_mode: bool = False,
                            init_args: Tuple = (), init_kwargs: Dict = {}) -> [_OceanResult]:

        __worker_run_time = 0
        __worker_run_finish = None

        while __worker_run_time < self.running_timeout + 1:
            try:
                await self.pre_activate(queue_tasks=queue_tasks, features=features, *init_args, **init_kwargs)
                await self.activate(task=task, saving_mode=saving_mode)
            except Exception as e:
                await self.pre_stop(e=e)
                __worker_run_finish = False
            else:
                self.post_done()
                __worker_run_finish = True
            finally:
                if __worker_run_finish is True:
                    return self.get_result()
                __worker_run_time += 1
        else:
            self.post_done()
            return self.get_result()


    async def pre_activate(self,
                           queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                           features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                           *args, **kwargs) -> None:
        await Running_Strategy.initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)


    async def activate(self, task: _BaseTask, saving_mode: bool = False) -> None:
        if saving_mode is True:
            __kwargs = {"task": task}
            __worker_list = Running_Strategy.build_workers(function=self.run_task, **__kwargs)
        else:
            __worker_list = Running_Strategy.build_workers(function=task.function, *task.func_args, **task.func_kwargs)
        await Running_Strategy.activate_workers(workers_list=__worker_list)


    @_ReTryMechanism.async_task
    async def run_task(self, task: _BaseTask) -> [_OceanResult]:
        result = await task.function(*task.func_args, **task.func_kwargs)
        return result


    async def pre_stop(self, e: Exception) -> None:
        raise e


    def post_stop(self) -> None:
        Running_Strategy.close()


    def post_done(self) -> None:
        pass


    def get_result(self) -> [_OceanResult]:
        if isinstance(Running_Strategy, _Resultable):
            return Running_Strategy.get_result()
        else:
            return []



class OceanSimpleManager(OceanManager):

    def __init__(self, mode: _RunningMode, worker_num: int):
        super().__init__(mode=mode, worker_num=worker_num)


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = _StrategyAdapter(
            mode=self._mode,
            worker_num=self.worker_num)
        global Running_Strategy
        Running_Strategy = __running_strategy_adapter.get_simple_strategy()



class OceanPersistenceManager(OceanManager):

    def __init__(self, mode: _RunningMode, worker_num: int,
                 persistence_strategy: _OceanPersistence,
                 db_connection_num: int):
        self.persistence_strategy = persistence_strategy
        self.db_connection_num = db_connection_num
        super().__init__(mode=mode, worker_num=worker_num)


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = _StrategyAdapter(
            mode=self._mode,
            worker_num=self.worker_num)
        global Running_Strategy
        Running_Strategy = __running_strategy_adapter.get_persistence_strategy(
            persistence_strategy=self.persistence_strategy,
            db_connection_num=self.db_connection_num
        )



class OceanSimpleAsyncManager(OceanAsyncWorker):

    def __init__(self, mode: _RunningMode, worker_num: int):
        super().__init__(mode=mode, worker_num=worker_num)


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = _StrategyAdapter(
            mode=self._mode,
            worker_num=self.worker_num)
        global Running_Strategy
        Running_Strategy = __running_strategy_adapter.get_simple_strategy()



class OceanPersistenceAsyncManager(OceanAsyncWorker):

    def __init__(self, mode: _RunningMode, worker_num: int,
                 persistence_strategy: _OceanPersistence,
                 db_connection_num: int):
        self.persistence_strategy = persistence_strategy
        self.db_connection_num = db_connection_num
        super().__init__(mode=mode, worker_num=worker_num)


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = _StrategyAdapter(
            mode=self._mode,
            worker_num=self.worker_num)
        global Running_Strategy
        Running_Strategy = __running_strategy_adapter.get_persistence_strategy(
            persistence_strategy=self.persistence_strategy,
            db_connection_num=self.db_connection_num
        )



class OceanSystem(_BaseSystem):

    def run(self,
            task: _BaseTask,
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
            saving_mode: bool = False,
            timeout: int = 0) -> [_OceanResult]:

        if self._mode is _RunningMode.Asynchronous:
            __ocean_worker = OceanSimpleAsyncManager(mode=self._mode, worker_num=self._worker_num)
            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features, saving_mode=saving_mode)
            return __ocean_worker.get_result()
        else:
            __ocean_worker = OceanSimpleManager(mode=self._mode, worker_num=self._worker_num)
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
            __ocean_worker = OceanPersistenceAsyncManager(
                mode=self._mode,
                worker_num=self._worker_num,
                persistence_strategy=persistence_strategy,
                db_connection_num=db_connection_num)

            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, queue_tasks=queue_tasks, features=features, saving_mode=saving_mode)
            return __ocean_worker.get_result()
        else:
            __ocean_worker = OceanPersistenceManager(
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


