from pyocean.framework.task import BaseTask as _BaseTask, BaseQueueTask as _BaseQueueTask
from pyocean.framework.manager import (
    BaseManager as _BaseManager,
    BaseAsyncManager as _BaseAsyncManager,
    BaseMapManager as _BaseMapManager)
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.strategy import (
    RunnableStrategy as _RunnableStrategy,
    AsyncRunnableStrategy as _AsyncRunnableStrategy,
    Resultable as _Resultable)
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.mode import RunningMode as _RunningMode
from pyocean.api.decorator import ReTryMechanism as _ReTryMechanism
from pyocean.adapter.strategy import (
    StrategyAdapter as _StrategyAdapter,
    MapStrategyAdapter as _MapStrategyAdapter)
from pyocean.persistence.interface import OceanPersistence as _OceanPersistence

from abc import ABC
from typing import Tuple, Dict, Optional, Union, List, Callable as CallableType, Iterable as IterableType
from types import MethodType, FunctionType
from collections import Iterable, Callable
from multipledispatch import dispatch
import inspect


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



class OceanMapManager(_BaseMapManager):

    ParameterCannotBeNoneError = TypeError("It should not pass 'None' value parameter(s).")
    InvalidParameterBePass = TypeError("The parameters data type is invalid. It should all be tuple or dict.")

    def __init__(self, mode: _RunningMode):
        __running_strategy_adapter = _MapStrategyAdapter(mode=mode)
        self.running_strategy = __running_strategy_adapter.get_map_strategy()


    def map_by_param(self,
                     function: CallableType,
                     args_iter: IterableType = [],
                     queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                     features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        __checksum = self.__chk_args_content(args_iter=args_iter)

        self.running_strategy.initialization(queue_tasks=queue_tasks, features=features)

        __workers_list = []
        for args in args_iter:
            __worker = self.__generate_worker(function, args)
            __workers_list.append(__worker)

        self.running_strategy.activate_worker(workers=__workers_list)
        self.running_strategy.close_worker(workers=__workers_list)


    def map_by_function(self,
                        functions: IterableType[Callable],
                        args_iter: IterableType = [],
                        queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                        features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        self.__chk_function_and_args(functions=functions, args_iter=args_iter)

        self.running_strategy.initialization(queue_tasks=queue_tasks, features=features)

        __workers_list = []
        if args_iter is None or args_iter == []:
            args_iter = [() for _ in range(len(list(functions)))]

        for fun, args in zip(functions, args_iter):
            print("CallableType: ", type(fun) is CallableType)
            print("MethodType: ", type(fun) is MethodType)
            print("FunctionType: ", type(fun) is FunctionType)
            print("args: ", args)
            __worker = self.__generate_worker(fun, args)
            __workers_list.append(__worker)

        self.running_strategy.activate_worker(__workers_list)
        self.running_strategy.close_worker(__workers_list)


    def __chk_args_content(self, args_iter: IterableType) -> List[Union[type, bool]]:
        """
        Description:
            The arguments only receive iterator of element which is
            tuple or dictionary object
        :param args_iter:
        :return:
        """

        if args_iter is None:
            raise self.ParameterCannotBeNoneError

        checksum = map(lambda ele: type(ele) if (type(ele) is tuple or type(ele) is dict) else False, args_iter)
        if False in checksum:
            raise self.InvalidParameterBePass
        return list(checksum)


    @dispatch(MethodType, tuple)
    def __generate_worker(self, function, args):
        __worker = self.running_strategy.generate_worker(target=function, *args)
        return __worker


    @dispatch(MethodType, dict)
    def ___generate_worker(self, function, args):
        __worker = self.running_strategy.generate_worker(target=function, **args)
        return __worker


    def __chk_function_and_args(self, functions: IterableType[Callable], args_iter: IterableType):
        if functions is None or args_iter is None:
            raise self.ParameterCannotBeNoneError

        self.__chk_args_content(args_iter=args_iter)
        self.__chk_fun_signature_and_param(functions=functions, args_iter=args_iter)


    def __chk_fun_signature_and_param(self, functions: IterableType[Callable], args_iter: IterableType) -> bool:
        for fun, args in zip(functions, args_iter):
            __fun_signature = inspect.signature(fun)
            __fun_parameter = __fun_signature.parameters
            if args != () and args != {} and len(__fun_parameter.keys()) != len(args):
                raise ValueError("The signature and parameter aren't mapping.")
        return True


    def start_new_worker(self, target: Callable, *args, **kwargs):
        self.running_strategy.start_new_worker(target=target, *args, **kwargs)

