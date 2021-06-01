from pyocean.framework.operator import BaseRunnableProcedure
from pyocean.framework.strategy import Resultable
from pyocean.framework.features import BaseQueueType
from pyocean.concurrent.features import MultiThreadingQueueType

from typing import Union, Callable, Tuple, Dict, Iterable



class ConcurrentProcedure(BaseRunnableProcedure):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = [],
            queue_type: BaseQueueType = MultiThreadingQueueType.Queue, *args, **kwargs) -> Union[object, None]:
        self.initial(tasks=tasks, queue_type=queue_type)
        # Build and run multiple processes
        self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)
        self.done()
        self.after_treatment()
        return None


    def initial(self, tasks: Iterable = [], queue_type: BaseQueueType = MultiThreadingQueueType.Queue, *args, **kwargs) -> None:
        self._Running_Strategy.init_multi_working(tasks=tasks, queue_type=queue_type, *args, **kwargs)


    def start(self,
              function: Callable,
              fun_args: Tuple[Union[object, Callable]] = (),
              fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        __worker_list = self._Running_Strategy.build_multi_workers(function=function, args=fun_args, kwargs=fun_kwargs)
        self._Running_Strategy.activate_multi_workers(workers_list=__worker_list)


    def done(self) -> Union[object, None]:
        self._Running_Strategy.end_multi_working()
        return None


    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass


    @property
    def result(self) -> Union[Iterable, None]:
        if isinstance(self._Running_Strategy, Resultable):
            return self._Running_Strategy.get_multi_working_result()
        else:
            return None

