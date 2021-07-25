from pyocean.framework.strategy import Resultable
from pyocean.framework.worker import BaseWorker, BaseTask, BaseSystem
from pyocean.framework.result import OceanResult
from pyocean.api.decorator import ReTryDecorator
from pyocean.api.mode import RunningMode, FeatureMode
from pyocean.api.features_adapter import QueueAdapter, LockAdapter, CommunicationAdapter
from pyocean.api.strategy_adapter import StrategyAdapter

from typing import List, Union, Callable, Dict, Tuple



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
        self._Fun_Kwargs = kwargs
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
        self._Init_Kwargs = kwargs
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



class FunctionObject:

    __Func = None
    __Func_Args = None
    __Func_Kwargs = None

    def function(self) -> Callable:
        return self.__Func


    def set_function(self, function: Callable) -> None:
        self.__Func = function


    def func_args(self):
        return self.__Func_Args


    def set_func_args(self, args: Tuple) -> None:
        self.__Func_Args = args


    def func_kwargs(self):
        return self.__Func_Kwargs


    def set_func_kwargs(self, kwargs: Dict) -> None:
        self.__Func_Kwargs = kwargs



class OceanWorker(BaseWorker):

    _Running_Strategy = None
    _Initial_Object = None
    _Target_Function = None

    _Queue = None
    _Lock = None
    _Communication = None

    def __init__(self, mode: RunningMode, worker_num: int):
        self._mode = mode

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

        __running_strategy_adapter = StrategyAdapter(mode=self._mode, worker_num=worker_num)
        self._Running_Strategy = __running_strategy_adapter.get_simple_strategy()


    @property
    def running_timeout(self) -> int:
        return self._Running_Timeout


    @running_timeout.setter
    def running_timeout(self, timeout: int) -> None:
        self._Running_Timeout = timeout


    def start(self, task: BaseTask) -> List[OceanResult]:
        __worker_run_time = 0
        __worker_run_finish = None

        while __worker_run_time < self.running_timeout:
            try:
                self.pre_start()
                self.activate(task=task)
            except Exception as e:
                self.pre_stop(e=e)
                __worker_run_finish = True
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


    def pre_start(self, *args, **kwargs):
        self._Running_Strategy.initialization(*args, **kwargs)


    def activate(self, task: BaseTask):
        __worker_list = self._Running_Strategy.build_workers(function=self.run, kwargs={"task": task})
        self._Running_Strategy.activate_workers(workers_list=__worker_list)


    @ReTryDecorator.task_retry_mechanism
    def run(self, task: BaseTask) -> List[OceanResult]:
        result = self.run_task(task=task)
        return result


    def run_task(self, task: BaseTask) -> List[OceanResult]:
        result = task.function(*task.func_args, **task.func_kwargs)
        return result


    def pre_stop(self, e: Exception):
        pass


    def post_stop(self):
        self._Running_Strategy.close()


    def post_done(self):
        pass


    def get_result(self) -> List[OceanResult]:
        if isinstance(self._Running_Strategy, Resultable):
            return self._Running_Strategy.get_result()
        else:
            return []



class OceanSystem(BaseSystem):

    def run(self, task: BaseTask):
        __ocean_worker = OceanWorker(mode=self._mode, worker_num=self._worker_num)
        __ocean_worker.start(task=task)


    def dispatcher(self):
        pass


    def terminate(self):
        pass


