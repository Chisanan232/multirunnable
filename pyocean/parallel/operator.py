from pyocean.framework.operator import BaseRunnableProcedure
from pyocean.framework.strategy import Resultable
from pyocean.framework.features import BaseQueueType
from pyocean.parallel.strategy import ParallelStrategy

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Callable, Iterable, Union
from multiprocessing import Manager
from multiprocessing.managers import Namespace



class MultiProcessesCommonObject(metaclass=ABCMeta):

    pass



class ParallelProcedure(BaseRunnableProcedure):

    _Manager: Manager = None
    _Namespace_Object: Namespace = None

    def __init__(self, running_strategy: ParallelStrategy):
        if isinstance(running_strategy, ParallelStrategy):
            super().__init__(running_strategy=running_strategy)
            self._Manager = Manager()
            self._Namespace_Object = self._Manager.Namespace()
        else:
            raise TypeError("ParallelBuilder should use ParallelStrategy type strategy.")


    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = None,
            queue_type: BaseQueueType = None, *args, **kwargs) -> Union[object, None]:
        self.initial(tasks=tasks,
                     queue_type=queue_type,
                     pool_initializer=kwargs.get("pool_initializer", None),
                     pool_initargs=kwargs.get("pool_initializer", None))
        # Build and run multiple processes
        self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)
        self.done()
        self.after_treatment()
        return self.result


    def initial(self, tasks: Iterable = None, queue_type: BaseQueueType = None, *args, **kwargs) -> None:
        if queue_type is not None:
            self._Running_Strategy.init_multi_working(tasks=tasks,
                                                      queue_type=queue_type,
                                                      pool_initializer=kwargs.get("pool_initializer", None),
                                                      pool_initargs=kwargs.get("pool_initargs", None))
        else:
            self._Running_Strategy.init_multi_working(tasks=tasks,
                                                      pool_initializer=kwargs.get("pool_initializer", None),
                                                      pool_initargs=kwargs.get("pool_initargs", None))

        # # Deprecated in the future
        # # Initial object as multiprocessing.NameSpace  (Useless code)
        # if fun_args:
        #     for arg in fun_args:
        #         if isinstance(arg, MultiProcessesCommonObject):
        #             # Just record or do something as namespace (?)
        #             print("Try to do something initial callable object to be namespace object.")
        #             namespace_obj = self.namespacing_object(obj=arg)
        #             arg_index = fun_args.index(arg)
        #             fun_args_list = list(fun_args)
        #             fun_args_list.pop(arg_index)
        #             fun_args_list.insert(arg_index, namespace_obj)
        #             fun_args = tuple(fun_args_list)
        # elif fun_kwargs:
        #     for key, value in fun_kwargs.items():
        #         if isinstance(value, MultiProcessesCommonObject):
        #             # Just record or do something as namespace (?)
        #             print("Try to do something initial callable object to be namespace object.")
        #             namespace_obj = self.namespacing_object(obj=value)
        #             fun_kwargs[key] = namespace_obj


    def start(self,
              function: Callable,
              fun_args: Tuple[Union[object, Callable]] = (),
              fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        __worker_list = self._Running_Strategy.build_multi_workers(function=function, args=fun_args, kwargs=fun_kwargs)
        self._Running_Strategy.activate_multi_workers(workers_list=__worker_list)


    def done(self) -> Union[object, None]:
        self._Running_Strategy.end_multi_working()
        if isinstance(self._Running_Strategy, Resultable):
            return self._Running_Strategy.get_multi_working_result()
        else:
            return None


    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass


    @property
    def result(self) -> Union[Iterable, None]:
        if isinstance(self._Running_Strategy, Resultable):
            return self._Running_Strategy.get_multi_working_result()
        else:
            return None
