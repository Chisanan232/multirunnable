from pyocean.framework.strategy import Resultable
from pyocean.framework.operator import BaseRunnableProcedure
from pyocean.framework.features import BaseQueueType
from pyocean.coroutine.features import GeventQueueType, AsynchronousQueueType

from typing import Union, Callable, Tuple, Dict, Iterable



class GeventProcedure(BaseRunnableProcedure):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = [],
            queue_type: BaseQueueType = GeventQueueType.Queue, *args, **kwargs) -> Union[object, None]:
        self.initial(tasks=tasks, queue_type=queue_type)
        # Build and run multiple processes
        self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)
        self.done()
        self.after_treatment()
        return None


    def initial(self, tasks: Iterable = [], queue_type: BaseQueueType = GeventQueueType.Queue, *args, **kwargs) -> None:
        self._Running_Strategy.init_multi_working(tasks=tasks, queue_type=queue_type, *args, **kwargs)


    def start(self,
              function: Callable,
              fun_args: Tuple[Union[object, Callable]] = (),
              fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        __worker_list = self._Running_Strategy.build_multi_workers(function=function, *fun_args, **fun_kwargs)
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



class AsynchronousProcedure(BaseRunnableProcedure):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = [],
            queue_type: BaseQueueType = AsynchronousQueueType.Queue, *args, **kwargs) -> Union[object, None]:
        __event_loop = self._Running_Strategy.get_event_loop()
        __event_loop.run_until_complete(
            future=self._async_process(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs,
                                       tasks=tasks, queue_type=queue_type)
        )
        self.done()
        self.after_treatment()
        return None


    async def _async_process(self,
                             function: Callable,
                             fun_args: Tuple[Union[object, Callable]] = (),
                             fun_kwargs: Dict[str, Union[object, Callable]] = {},
                             tasks: Iterable = [],
                             queue_type: BaseQueueType = AsynchronousQueueType.Queue):
        await self.initial(tasks=tasks, queue_type=queue_type)
        await self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)


    async def initial(self, tasks: Iterable = None, queue_type: BaseQueueType = None, *args, **kwargs) -> None:
        await self._Running_Strategy.init_multi_working(tasks=tasks, queue_type=queue_type, *args, **kwargs)


    async def start(self,
                    function: Callable,
                    fun_args: Tuple[Union[object, Callable]] = (),
                    fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        __task_list = self._Running_Strategy.build_multi_workers(function=function, *fun_args, **fun_kwargs)
        await self._Running_Strategy.activate_multi_workers(workers_list=__task_list)


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

