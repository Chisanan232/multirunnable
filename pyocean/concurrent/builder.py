from pyocean.framework.strategy import Resultable
from pyocean.framework.builder import BaseBuilder

from typing import Union, Callable, Tuple, Dict, Iterable

from deprecated.sphinx import deprecated



class ConcurrentBuilder(BaseBuilder):

    """
    Note:
        Unify all concurrency running strategy (like multithreading, greenlet) to use this builder to build a concurrent program.
    """

    __Running_Result = None

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
        __worker_list = self._Running_Strategy.build_multi_workers(function=function, args=fun_args, kwargs=fun_kwargs)
        self._Running_Strategy.activate_multi_workers(workers_list=__worker_list)


    def done(self) -> None:
        self._Running_Strategy.end_multi_working()
        if isinstance(self._Running_Strategy, Resultable):
            self.__Running_Result = self._Running_Strategy.get_multi_working_result()


    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass


    @property
    def result(self) -> Union[Iterable, None]:
        return self.__Running_Result



class ThreadsBuilder(BaseBuilder):

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
        __worker_list = self._Running_Strategy.build_multi_workers(function=function, args=fun_args, kwargs=fun_kwargs)
        self._Running_Strategy.activate_multi_workers(workers_list=__worker_list)


    def done(self) -> Union[object, None]:
        self._Running_Strategy.end_multi_working()
        return None


    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass



@deprecated(version="0.8", reason="Move the class into module 'coroutine'")
class GreenletBuilder(BaseBuilder):

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
        __worker_list = self._Running_Strategy.build_multi_workers(function=function, args=fun_args, kwargs=fun_kwargs)
        self._Running_Strategy.activate_multi_workers(workers_list=__worker_list)


    def done(self) -> Union[object, None]:
        self._Running_Strategy.end_multi_working()
        return None


    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass



@deprecated(version="0.8", reason="Move the class into module 'coroutine'")
class CoroutineBuilder(BaseBuilder):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = None) -> Union[object, None]:
        pass


    def initial(self,
                fun_args: Tuple[Union[object, Callable]] = (),
                fun_kwargs: Dict[str, Union[object, Callable]] = {},
                tasks: Iterable = None) -> None:
        pass


    def start(self,
              function: Callable,
              fun_args: Tuple[Union[object, Callable]] = (),
              fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        pass


    def done(self) -> Union[object, None]:
        pass


    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass

