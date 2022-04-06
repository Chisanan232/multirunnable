from typing import List, Tuple, Dict, Iterable, Callable
from abc import ABCMeta, abstractmethod

from .runnable.result import MRResult as _MRResult
from ..types import MRTasks as _MRTasks



class BasePool(metaclass=ABCMeta):

    _Worker_Timeout = 3
    _Ocean_Tasks_List: List[_MRTasks] = []

    def __init__(self, pool_size: int):
        self.pool_size = pool_size


    def __str__(self):
        return f"{self.__str__()} at {id(self.__class__)}"


    def __enter__(self):
        pass


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


    @abstractmethod
    def _initial_running_strategy(self) -> None:
        """
        Description:
            Initialize and instantiate RunningStrategy.
        :return:
        """
        pass


    @abstractmethod
    def initial(self) -> None:
        """
        Description:
            Initializing Process.
        :return:
        """
        pass


    @abstractmethod
    def apply(self, tasks_size: int, function: Callable, *args, **kwargs) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.apply.
        :param tasks_size:
        :param function:
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def async_apply(self, tasks_size: int, function: Callable, args: Tuple = (),
                    kwargs: Dict = {}, callback: Callable = None, error_callback: Callable = None) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.apply_async.
        :param tasks_size:
        :param function:
        :param args:
        :param kwargs:
        :param callback:
        :param error_callback:
        :return:
        """
        pass


    @abstractmethod
    def apply_with_iter(self, functions_iter: List[Callable], args_iter: List[Tuple] = None, kwargs_iter: List[Dict] = None) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.apply with iterator of arguments.
        :param functions_iter:
        :param args_iter:
        :param kwargs_iter:
        :return:
        """
        pass


    @abstractmethod
    def async_apply_with_iter(self, functions_iter: List[Callable], args_iter: List[Tuple] = None,
                              kwargs_iter: List[Dict] = None, callback_iter: List[Callable] = None,
                              error_callback_iter: List[Callable] = None) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.apply_async with iterator of arguments.
        :param functions_iter:
        :param args_iter:
        :param kwargs_iter:
        :param callback_iter:
        :param error_callback_iter:
        :return:
        """
        pass


    @abstractmethod
    def map(self, function: Callable, args_iter: Iterable = (), chunksize: int = None) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.map.
        :param function:
        :param args_iter:
        :param chunksize:
        :return:
        """
        pass


    @abstractmethod
    def async_map(self, function: Callable, args_iter: Iterable = (), chunksize: int = None,
                  callback: Callable = None, error_callback: Callable = None) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.map_async.
        :param function:
        :param args_iter:
        :param chunksize:
        :param callback:
        :param error_callback:
        :return:
        """
        pass


    @abstractmethod
    def map_by_args(self, function: Callable, args_iter: Iterable[Iterable] = (), chunksize: int = None) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.starmap.
        :param function:
        :param args_iter:
        :param chunksize:
        :return:
        """
        pass


    @abstractmethod
    def async_map_by_args(self, function: Callable, args_iter: Iterable[Iterable] = (),
                          chunksize: int = None, callback: Callable = None, error_callback: Callable = None) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.starmap_async.
        :param function:
        :param args_iter:
        :param chunksize:
        :param callback:
        :param error_callback:
        :return:
        """
        pass


    @abstractmethod
    def imap(self, function: Callable, args_iter: Iterable = (), chunksize: int = 1) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.imap.
        :param function:
        :param args_iter:
        :param chunksize:
        :return:
        """
        pass


    @abstractmethod
    def imap_unordered(self, function: Callable, args_iter: Iterable = (), chunksize: int = 1) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.imap_unordered.
        :param function:
        :param args_iter:
        :param chunksize:
        :return:
        """
        pass


    @abstractmethod
    def close(self) -> None:
        """
        Description:
            Close and join the Pool.
        :return:
        """
        pass


    @abstractmethod
    def terminal(self) -> None:
        """
        Description:
            Terminal Pool.
        :return:
        """
        pass


    @abstractmethod
    def get_result(self) -> List[_MRResult]:
        """
        Description:
            Get the running result.
        :return:
        """
        pass

