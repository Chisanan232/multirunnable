from pyocean.framework.strategy import RunnableStrategy
from pyocean.framework.features import BaseQueueType
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



class BaseRunnableProcedure(metaclass=ABCMeta):

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
            tasks: Iterable = None,
            queue_type: BaseQueueType = None, *args, **kwargs) -> Union[object, None]:
        pass


    @abstractmethod
    def initial(self, tasks: Iterable = None, queue_type: BaseQueueType = None, *args, **kwargs) -> None:
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
