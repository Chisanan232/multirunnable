from .strategy import RunnableStrategy
from ..exceptions import GlobalObjectIsNoneError

from abc import ABCMeta, abstractmethod
from typing import Tuple, Dict, Callable, Iterable, Union
from multiprocessing import Manager, Queue as ProcessQueue
from queue import Queue



class RunnableBuilder:

    @classmethod
    def run_with_lock(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from .strategy import Running_Lock

        cls.__checking_init(target_obj=Running_Lock)
        with Running_Lock:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def run_with_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from .strategy import Running_Semaphore

        cls.__checking_init(target_obj=Running_Semaphore)
        with Running_Semaphore:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def run_with_bounded_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from .strategy import Running_Bounded_Semaphore

        cls.__checking_init(target_obj=Running_Bounded_Semaphore)
        with Running_Bounded_Semaphore:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def get_queue(cls) -> Union[Queue, ProcessQueue]:
        from .strategy import Running_Queue

        cls.__checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    def get_one_value_of_queue(cls) -> object:
        from .strategy import Running_Queue

        cls.__checking_init(target_obj=Running_Queue)
        return Running_Queue.get()


    @classmethod
    def __checking_init(cls, target_obj: object) -> bool:
        if target_obj is None:
            raise GlobalObjectIsNoneError
        return True



class BaseBuilder(metaclass=ABCMeta):

    _Running_Strategy: RunnableStrategy = None

    def __init__(self, running_strategy: RunnableStrategy):
        if isinstance(running_strategy, RunnableStrategy):
            self._Running_Strategy = running_strategy
        else:
            raise TypeError("The strategy object should be 'RunnableStrategy' type. "
                            "Please import pyocean.framework.strategy.RunnableStrategy to build one.")


    def run_with_lock(self, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        return RunnableBuilder.run_with_lock(function=function, arg=arg, kwarg=kwarg)


    def run_with_semaphore(self, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        return RunnableBuilder.run_with_semaphore(function=function, arg=arg, kwarg=kwarg)


    def run_with_bounded_semaphore(self, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        return RunnableBuilder.run_with_bounded_semaphore(function=function, arg=arg, kwarg=kwarg)


    def get_queue(self) -> Union[Queue, ProcessQueue]:
        return RunnableBuilder.get_queue()


    def get_one_value_of_queue(self) -> object:
        return RunnableBuilder.get_one_value_of_queue()


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
