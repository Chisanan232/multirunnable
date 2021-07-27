from pyocean.framework.strategy import Resultable
from pyocean.framework.operator import BaseRunnableProcedure

from typing import Union, Callable, Tuple, Dict, Iterable



class GeventProcedure(BaseRunnableProcedure):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            *args, **kwargs) -> Union[object, None]:
        self.initial()
        # Build and run multiple processes
        self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)
        self.done()
        self.after_treatment()
        return None


    def initial(self, *args, **kwargs) -> None:
        self._Running_Strategy.initialization(*args, **kwargs)


    def start(self,
              function: Callable,
              fun_args: Tuple[Union[object, Callable]] = (),
              fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        __worker_list = self._Running_Strategy.build_workers(function=function, *fun_args, **fun_kwargs)
        self._Running_Strategy.activate_workers(workers_list=__worker_list)


    def done(self) -> Union[object, None]:
        self._Running_Strategy.close()
        return None


    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass


    @property
    def result(self) -> Union[Iterable, None]:
        if isinstance(self._Running_Strategy, Resultable):
            return self._Running_Strategy.get_result()
        else:
            return None



class AsynchronousProcedure(BaseRunnableProcedure):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            *args, **kwargs) -> Union[object, None]:
        __event_loop = self._Running_Strategy.get_event_loop()
        __event_loop.run_until_complete(
            future=self._async_process(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)
        )
        self.done()
        self.after_treatment()
        return None


    async def _async_process(self,
                             function: Callable,
                             fun_args: Tuple[Union[object, Callable]] = (),
                             fun_kwargs: Dict[str, Union[object, Callable]] = {}):
        await self.initial()
        await self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)


    async def initial(self, *args, **kwargs) -> None:
        await self._Running_Strategy.initialization(*args, **kwargs)


    async def start(self,
                    function: Callable,
                    fun_args: Tuple[Union[object, Callable]] = (),
                    fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        __task_list = self._Running_Strategy.build_workers(function=function, *fun_args, **fun_kwargs)
        await self._Running_Strategy.activate_workers(workers_list=__task_list)


    def done(self) -> Union[object, None]:
        self._Running_Strategy.close()
        return None


    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass


    @property
    def result(self) -> Union[Iterable, None]:
        if isinstance(self._Running_Strategy, Resultable):
            return self._Running_Strategy.get_result()
        else:
            return None

