from pyocean.framework.worker import BaseTask, BaseWorker, BaseAsyncWorker, BaseSystem
from pyocean.framework.strategy import RunnableStrategy, AsyncRunnableStrategy, Resultable
from pyocean.framework.result import OceanResult
from pyocean.api.mode import RunningMode, FeatureMode
from pyocean.api.decorator import ReTryMechanism
from pyocean.api.features_adapter import QueueAdapter, LockAdapter, CommunicationAdapter
from pyocean.api.strategy_adapter import StrategyAdapter

from typing import List, Tuple, Dict, Callable, Union



class OceanTask(BaseTask):

    @property
    def function(self) -> Callable:
        return self._Function


    def set_function(self, function: Callable) -> BaseTask:
        self._Function = function
        return self


    @property
    def func_args(self) -> Tuple:
        return self._Fun_Args


    def set_func_args(self, args: Tuple) -> BaseTask:
        self._Fun_Args = args
        return self


    @property
    def func_kwargs(self) -> Dict:
        return self._Fun_Kwargs


    def set_func_kwargs(self, kwargs: Dict) -> BaseTask:
        for key, value in kwargs.items():
            self._Fun_Kwargs[key] = value
        return self


    @property
    def initialization(self) -> Callable:
        return self._Initialization


    def set_initialization(self, init: Callable) -> BaseTask:
        self._Initialization = init
        return self


    @property
    def init_args(self) -> Tuple:
        return self._Init_Args


    def set_init_args(self, args: Tuple) -> BaseTask:
        self._Init_Args = args
        return self


    @property
    def init_kwargs(self) -> Dict:
        return self._Init_Kwargs


    def set_init_kwargs(self, kwargs: Dict) -> BaseTask:
        for key, value in kwargs.items():
            self._Init_Kwargs[key] = value
        return self


    @property
    def group(self) -> str:
        return self._Group


    def set_group(self, group: str) -> BaseTask:
        self._Group = group
        return self


    @property
    def done_handler(self) -> Callable:
        return self._Done_Handler


    def set_done_handler(self, hdlr: Callable) -> BaseTask:
        self._Done_Handler = hdlr
        return self


    @property
    def error_handler(self) -> Callable:
        return self._Error_Handler


    def set_error_handler(self, hdlr: Callable) -> BaseTask:
        self._Error_Handler = hdlr
        return self


    @property
    def running_timeout(self) -> int:
        return self._Running_Timeout


    def set_running_timeout(self, timeout: int) -> BaseTask:
        self._Running_Timeout = timeout
        return self


Running_Strategy: Union[RunnableStrategy, AsyncRunnableStrategy] = None


class OceanWorker(BaseWorker):

    _Queue = None
    _Lock = None
    _Communication = None

    def __init__(self, mode: RunningMode, worker_num: int):
        self._mode = mode
        self.worker_num = worker_num

        self._initial_running_strategy()

        __feature_mode = None
        if self._mode is RunningMode.Parallel:
            __feature_mode = FeatureMode.MultiProcessing
        elif self._mode is RunningMode.Concurrent:
            __feature_mode = FeatureMode.MultiThreading
        elif self._mode is RunningMode.Greenlet:
            __feature_mode = FeatureMode.MultiGreenlet
        elif self._mode is RunningMode.Asynchronous:
            __feature_mode = FeatureMode.Asynchronous

        self._Queue = QueueAdapter(mode=__feature_mode)
        self._Lock = LockAdapter(mode=__feature_mode)
        self._Communication = CommunicationAdapter(mode=__feature_mode)


    @property
    def running_timeout(self) -> int:
        return self._Worker_Timeout


    @running_timeout.setter
    def running_timeout(self, timeout: int) -> None:
        self._Worker_Timeout = timeout


    def start(self, task: BaseTask, saving_mode: bool = False,
              init_args: Tuple = (), init_kwargs: Dict = {}) -> List[OceanResult]:
        __worker_run_time = 0
        __worker_run_finish = None

        while __worker_run_time < self.running_timeout + 1:
            try:
                self.pre_activate(*init_args, **init_kwargs)
                self.activate(task=task, saving_mode=saving_mode)
            except Exception as e:
                self.pre_stop(e=e)
                __worker_run_finish = False
            else:
                self.post_done()
                __worker_run_finish = True
            finally:
                self.post_stop()
                if __worker_run_finish is True:
                    return self.get_result()
                __worker_run_time += 1
        else:
            self.post_done()
            self.post_stop()
            return self.get_result()


    def pre_activate(self, *args, **kwargs) -> None:
        Running_Strategy.initialization(*args, **kwargs)


    def activate(self, task: BaseTask, saving_mode: bool = False) -> None:
        if saving_mode is True:
            _kwargs = {"task": task}
            __worker_list = Running_Strategy.build_workers(function=self.run_task, **_kwargs)
        else:
            __worker_list = Running_Strategy.build_workers(function=task.function, *task.func_args, **task.func_kwargs)
        Running_Strategy.activate_workers(workers_list=__worker_list)


    @ReTryMechanism.task
    def run_task(self, task: BaseTask) -> List[OceanResult]:
        result = task.function(*task.func_args, **task.func_kwargs)
        return result


    def pre_stop(self, e: Exception) -> None:
        raise e


    def post_stop(self) -> None:
        Running_Strategy.close()


    def post_done(self) -> None:
        pass


    def get_result(self) -> List[OceanResult]:
        if isinstance(Running_Strategy, Resultable):
            return Running_Strategy.get_result()
        else:
            return []



class OceanAsyncWorker(BaseAsyncWorker):

    _Initial_Object = None
    _Target_Function = None

    _Queue = None
    _Lock = None
    _Communication = None

    def __init__(self, mode: RunningMode, worker_num: int):
        self._mode = mode
        self.worker_num = worker_num

        self._initial_running_strategy()

        __feature_mode = None
        if self._mode is RunningMode.Parallel:
            __feature_mode = FeatureMode.MultiProcessing
        elif self._mode is RunningMode.Concurrent:
            __feature_mode = FeatureMode.MultiThreading
        elif self._mode is RunningMode.Greenlet:
            __feature_mode = FeatureMode.MultiGreenlet
        elif self._mode is RunningMode.Asynchronous:
            __feature_mode = FeatureMode.Asynchronous

        self._Queue = QueueAdapter(mode=__feature_mode)
        self._Lock = LockAdapter(mode=__feature_mode)
        self._Communication = CommunicationAdapter(mode=__feature_mode)


    def _initial_running_strategy(self) -> None:
        pass


    @property
    def running_timeout(self) -> int:
        return self._Worker_Timeout


    @running_timeout.setter
    def running_timeout(self, timeout: int) -> None:
        self._Worker_Timeout = timeout


    def start(self, task: BaseTask, saving_mode: bool = False,
              init_args: Tuple = (), init_kwargs: Dict = {}) -> None:
        __event_loop = Running_Strategy.get_event_loop()
        __event_loop.run_until_complete(
            future=self.async_process(
                task=task, saving_mode=saving_mode,
                init_args=init_args, init_kwargs=init_kwargs)
        )
        self.post_stop()


    async def async_process(self, task: BaseTask, saving_mode: bool = False,
                            init_args: Tuple = (), init_kwargs: Dict = {}) -> List[OceanResult]:
        __worker_run_time = 0
        __worker_run_finish = None

        while __worker_run_time < self.running_timeout + 1:
            try:
                await self.pre_activate(*init_args, **init_kwargs)
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


    async def pre_activate(self, *args, **kwargs) -> None:
        await Running_Strategy.initialization(*args, **kwargs)


    async def activate(self, task: BaseTask, saving_mode: bool = False) -> None:
        if saving_mode is True:
            __kwargs = {"task": task}
            __worker_list = Running_Strategy.build_workers(function=self.run_task, **__kwargs)
        else:
            __worker_list = Running_Strategy.build_workers(function=task.function, *task.func_args, **task.func_kwargs)
        await Running_Strategy.activate_workers(workers_list=__worker_list)


    @ReTryMechanism.async_task
    async def run_task(self, task: BaseTask) -> List[OceanResult]:
        result = await task.function(*task.func_args, **task.func_kwargs)
        return result


    async def pre_stop(self, e: Exception) -> None:
        pass


    def post_stop(self) -> None:
        Running_Strategy.close()


    def post_done(self) -> None:
        pass


    def get_result(self) -> List[OceanResult]:
        if isinstance(Running_Strategy, Resultable):
            return Running_Strategy.get_result()
        else:
            return []



class OceanSimpleWorker(OceanWorker):

    def __init__(self, mode: RunningMode, worker_num: int):
        super().__init__(mode, worker_num)


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = StrategyAdapter(mode=self._mode, worker_num=self.worker_num)
        global Running_Strategy
        Running_Strategy = __running_strategy_adapter.get_simple_strategy()



class OceanPersistenceWorker(OceanWorker):

    def __init__(self, mode: RunningMode, worker_num: int, persistence_strategy, db_connection_num):
        super().__init__(mode, worker_num)

        __running_strategy_adapter = StrategyAdapter(mode=self._mode, worker_num=worker_num)
        self._Running_Strategy = __running_strategy_adapter.get_persistence_strategy(
            persistence_strategy=persistence_strategy, db_connection_num=db_connection_num)



class OceanSimpleAsyncWorker(OceanAsyncWorker):

    def __init__(self, mode: RunningMode, worker_num: int):
        super().__init__(mode, worker_num)


    def _initial_running_strategy(self) -> None:
        __running_strategy_adapter = StrategyAdapter(mode=self._mode, worker_num=self.worker_num)
        global Running_Strategy
        Running_Strategy = __running_strategy_adapter.get_simple_strategy()



class OceanPersistenceAsyncWorker(OceanAsyncWorker):

    def __init__(self, mode: RunningMode, worker_num: int, persistence_strategy, db_connection_num):
        super().__init__(mode, worker_num)

        __running_strategy_adapter = StrategyAdapter(mode=self._mode, worker_num=worker_num)
        self._Running_Strategy = __running_strategy_adapter.get_persistence_strategy(
            persistence_strategy=persistence_strategy, db_connection_num=db_connection_num)



class OceanSystem(BaseSystem):

    def run(self, task: BaseTask, saving_mode: bool = False, timeout: int = 0):
        if self._mode is RunningMode.Asynchronous:
            __ocean_worker = OceanSimpleAsyncWorker(
                mode=self._mode, worker_num=self._worker_num)
            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, saving_mode=saving_mode)
        else:
            __ocean_worker = OceanSimpleWorker(
                mode=self._mode, worker_num=self._worker_num)
            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, saving_mode=saving_mode)


    def run_and_save(self, task: BaseTask, persistence_strategy, db_connection_num, saving_mode: bool = False, timeout: int = 0):
        if self._mode is RunningMode.Asynchronous:
            __ocean_worker = OceanPersistenceAsyncWorker(
                mode=self._mode, worker_num=self._worker_num,
                persistence_strategy=persistence_strategy,
                db_connection_num=db_connection_num)
            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, saving_mode=saving_mode)
        else:
            __ocean_worker = OceanPersistenceWorker(
                mode=self._mode, worker_num=self._worker_num,
                persistence_strategy=persistence_strategy,
                db_connection_num=db_connection_num)
            __ocean_worker.running_timeout = timeout
            __ocean_worker.start(task=task, saving_mode=saving_mode)


    def dispatcher(self):
        pass


    def terminate(self):
        pass


