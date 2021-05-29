from pyocean.framework.builder import BaseRunnableBuilder

from typing import Union, Callable, Tuple, Dict, Iterable



class GeventBuilder(BaseRunnableBuilder):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = None) -> Union[object, None]:
        self.initial(fun_args=fun_args, fun_kwargs=fun_kwargs, tasks=tasks)
        # Build and run multiple processes
        self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)
        self.done()
        self.after_treatment()
        return None


    def initial(self,
                fun_args: Tuple[Union[object, Callable]] = (),
                fun_kwargs: Dict[str, Union[object, Callable]] = {},
                tasks: Iterable = None) -> None:
        self._Running_Strategy.init_multi_working(tasks=tasks, *fun_args, **fun_kwargs)


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



class AsynchronousBuilder(BaseRunnableBuilder):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = None) -> Union[object, None]:
        __event_loop = self._Running_Strategy.get_event_loop()
        __event_loop.run_until_complete(
            future=self._async_process(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs, tasks=tasks)
        )
        self.done()
        self.after_treatment()
        return None


    async def _async_process(self,
                             function: Callable,
                             fun_args: Tuple[Union[object, Callable]] = (),
                             fun_kwargs: Dict[str, Union[object, Callable]] = {},
                             tasks: Iterable = None):
        await self.initial(fun_args=fun_args, fun_kwargs=fun_kwargs, tasks=tasks)
        await self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)


    async def initial(self,
                      fun_args: Tuple[Union[object, Callable]] = (),
                      fun_kwargs: Dict[str, Union[object, Callable]] = {},
                      tasks: Iterable = None) -> None:
        await self._Running_Strategy.init_multi_working(tasks=tasks, *fun_args, **fun_kwargs)


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

