from pyocean.framework.operator import BaseRunnableProcedure
from pyocean.framework.strategy import Resultable
from pyocean.parallel.strategy import ParallelStrategy

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Callable, Iterable, Union



class MultiProcessesCommonObject(metaclass=ABCMeta):

    pass



class ParallelProcedure(BaseRunnableProcedure):

    def __init__(self, running_strategy: ParallelStrategy):
        if isinstance(running_strategy, ParallelStrategy):
            super().__init__(running_strategy=running_strategy)
        else:
            raise TypeError("ParallelBuilder should use ParallelStrategy type strategy.")


    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            *args, **kwargs) -> Union[object, None]:
        self.initial(
            pool_initializer=kwargs.get("pool_initializer", None),
            pool_initargs=kwargs.get("pool_initializer", None))
        # Build and run multiple processes
        self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)
        self.done()
        self.after_treatment()
        return self.result


    def initial(self, *args, **kwargs) -> None:
        self._Running_Strategy.initialization(
            pool_initializer=kwargs.get("pool_initializer", None),
            pool_initargs=kwargs.get("pool_initargs", None))


    def start(self,
              function: Callable,
              fun_args: Tuple[Union[object, Callable]] = (),
              fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        __worker_list = self._Running_Strategy.build_workers(function=function, *fun_args, **fun_kwargs)
        self._Running_Strategy.activate_workers(workers_list=__worker_list)


    def done(self) -> Union[object, None]:
        self._Running_Strategy.close()
        if isinstance(self._Running_Strategy, Resultable):
            return self._Running_Strategy.get_result()
        else:
            return None


    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass


    @property
    def result(self) -> Union[Iterable, None]:
        if isinstance(self._Running_Strategy, Resultable):
            return self._Running_Strategy.get_result()
        else:
            return None

