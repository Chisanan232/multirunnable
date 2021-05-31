from pyocean.framework.operator import RunnableOperator, BaseRunnableProcedure
from pyocean.framework.strategy import RunnableStrategy, Resultable
from pyocean.framework.features import BaseQueueType
from pyocean.api.types import OceanQueue

from typing import Tuple, Dict, Callable, Iterable, Union



class MultiRunnableOperator(RunnableOperator):

    @classmethod
    def run_with_lock(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Lock

        cls._checking_init(target_obj=Running_Lock)
        with Running_Lock:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def run_with_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Semaphore

        cls._checking_init(target_obj=Running_Semaphore)
        with Running_Semaphore:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def run_with_bounded_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Bounded_Semaphore

        cls._checking_init(target_obj=Running_Bounded_Semaphore)
        with Running_Bounded_Semaphore:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def get_queue(cls) -> OceanQueue:
        from pyocean.framework.strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    def get_one_value_of_queue(cls) -> object:
        from pyocean.framework.strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue.get()



class AsyncRunnableOperator(RunnableOperator):

    @classmethod
    async def run_with_lock(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Lock

        cls._checking_init(target_obj=Running_Lock)
        async with Running_Lock:
            value = await function(*arg, **kwarg)
        return value


    @classmethod
    async def run_with_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Semaphore

        cls._checking_init(target_obj=Running_Semaphore)
        async with Running_Semaphore:
            value = await function(*arg, **kwarg)
        return value


    @classmethod
    async def run_with_bounded_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Bounded_Semaphore

        cls._checking_init(target_obj=Running_Bounded_Semaphore)
        async with Running_Bounded_Semaphore:
            value = await function(*arg, **kwarg)
        return value


    @classmethod
    def get_queue(cls) -> OceanQueue:
        from pyocean.framework.strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    async def get_one_value_of_queue(cls) -> object:
        from pyocean.framework.strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return await Running_Queue.get()



class SimpleProcedure(BaseRunnableProcedure):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = None,
            queue_type: BaseQueueType = None, *args, **kwargs) -> Union[object, None]:
        self.initial(tasks=tasks, queue_type=queue_type)
        # Build and run multiple processes
        self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)
        self.done()
        self.after_treatment()
        return None


    def initial(self, tasks: Iterable = None, queue_type: BaseQueueType = None, *args, **kwargs) -> None:
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



class GeventProcedure(BaseRunnableProcedure):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = None,
            queue_type: BaseQueueType = None, *args, **kwargs) -> Union[object, None]:
        self.initial(tasks=tasks, queue_type=queue_type)
        # Build and run multiple processes
        self.start(function=function, fun_args=fun_args, fun_kwargs=fun_kwargs)
        self.done()
        self.after_treatment()
        return None


    def initial(self, tasks: Iterable = None, queue_type: BaseQueueType = None, *args, **kwargs) -> None:
        self._Running_Strategy.init_multi_working(tasks=tasks, queue_type=queue_type, *args, **kwargs)


    def start(self,
              function: Callable,
              fun_args: Tuple[Union[object, Callable]] = (),
              fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        __worker_list = self._Running_Strategy.build_multi_workers(function=function, *fun_args, *fun_kwargs)
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



class ParallelProcedure(BaseRunnableProcedure):

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
        return None


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



class AsynchronousProcedure(BaseRunnableProcedure):

    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = None,
            queue_type: BaseQueueType = None, *args, **kwargs) -> Union[object, None]:
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
                             tasks: Iterable = None,
                             queue_type: BaseQueueType = None):
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

