from pyocean.framework.strategy import RunnableStrategy
from pyocean.api.types import OceanQueue
from pyocean.exceptions import GlobalObjectIsNoneError

from abc import ABCMeta, abstractmethod
from typing import Tuple, Dict, Callable, Iterable, Union



class RunnableOperator(metaclass=ABCMeta):

    @classmethod
    def _checking_init(cls, target_obj: object) -> bool:
        if target_obj is None:
            raise GlobalObjectIsNoneError
        return True


    @classmethod
    @abstractmethod
    def run_with_lock(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        pass


    @classmethod
    @abstractmethod
    def run_with_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        pass


    @classmethod
    @abstractmethod
    def run_with_bounded_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        pass


    @classmethod
    @abstractmethod
    def get_one_value_of_queue(cls) -> object:
        pass



class MultiRunnableOperator(RunnableOperator):

    @classmethod
    def run_with_lock(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from .strategy import Running_Lock

        cls._checking_init(target_obj=Running_Lock)
        with Running_Lock:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def run_with_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from .strategy import Running_Semaphore

        cls._checking_init(target_obj=Running_Semaphore)
        with Running_Semaphore:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def run_with_bounded_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from .strategy import Running_Bounded_Semaphore

        cls._checking_init(target_obj=Running_Bounded_Semaphore)
        with Running_Bounded_Semaphore:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def get_queue(cls) -> OceanQueue:
        from .strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    def get_one_value_of_queue(cls) -> object:
        from .strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue.get()



class AsyncRunnableOperator(RunnableOperator):

    @classmethod
    async def run_with_lock(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from .strategy import Running_Lock

        cls._checking_init(target_obj=Running_Lock)
        async with Running_Lock:
            value = await function(*arg, **kwarg)
        return value


    @classmethod
    async def run_with_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from .strategy import Running_Semaphore

        cls._checking_init(target_obj=Running_Semaphore)
        async with Running_Semaphore:
            value = await function(*arg, **kwarg)
        return value


    @classmethod
    async def run_with_bounded_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from .strategy import Running_Bounded_Semaphore

        cls._checking_init(target_obj=Running_Bounded_Semaphore)
        async with Running_Bounded_Semaphore:
            value = await function(*arg, **kwarg)
        return value


    @classmethod
    def get_queue(cls) -> OceanQueue:
        from .strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    async def get_one_value_of_queue(cls) -> object:
        from .strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return await Running_Queue.get()



class BaseRunnableBuilder(metaclass=ABCMeta):

    _Running_Strategy: RunnableStrategy = None

    def __init__(self, running_strategy: RunnableStrategy):
        if isinstance(running_strategy, RunnableStrategy):
            self._Running_Strategy = running_strategy
        else:
            raise TypeError("The strategy object should be 'RunnableStrategy' type. "
                            "Please import pyocean.framework.RunnableStrategy to build one.")


    @abstractmethod
    def run(self,
            function: Callable,
            fun_args: Tuple[Union[object, Callable]] = (),
            fun_kwargs: Dict[str, Union[object, Callable]] = {},
            tasks: Iterable = None) -> Union[object, None]:
        pass


    @abstractmethod
    def initial(self,
                fun_args: Tuple[Union[object, Callable]] = (),
                fun_kwargs: Dict[str, Union[object, Callable]] = {},
                tasks: Iterable = None) -> None:
        pass


    @abstractmethod
    def start(self,
              function: Callable,
              fun_args: Tuple[Union[object, Callable]] = (),
              fun_kwargs: Dict[str, Union[object, Callable]] = {}) -> None:
        pass


    @abstractmethod
    def done(self) -> Union[object, None]:
        pass


    @abstractmethod
    def after_treatment(self, *args, **kwargs) -> Union[object, None]:
        pass
