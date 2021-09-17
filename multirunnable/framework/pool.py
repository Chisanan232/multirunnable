from multirunnable.framework.result import OceanResult as _OceanResult
from multirunnable.mode import RunningMode as _RunningMode
from multirunnable.types import OceanTasks as _OceanTasks
import multirunnable._utils as _utils

from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict, Iterable, Callable



class BasePool(metaclass=ABCMeta):

    _Worker_Timeout = 3
    _Ocean_Tasks_List: List[_OceanTasks] = []

    def __init__(self, mode: _RunningMode, pool_size: int):
        self._mode = mode
        self.pool_size = pool_size


    def __str__(self):
        return f"{self.__str__()} at {id(self.__class__)}"


    def __repr__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(" \
                               f"mode={self._mode}, " \
                               f"pool_size={self.pool_size})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


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
    def apply(self, function: Callable, *args, **kwargs) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.apply.
        :param function:
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def async_apply(self,
                    function: Callable,
                    args: Tuple = (),
                    kwargs: Dict = {},
                    callback: Callable = None,
                    error_callback: Callable = None) -> None:
        """
        Description:
            The adapter of multiprocessing.pool.apply_async.
        :param function:
        :param args:
        :param kwargs:
        :param callback:
        :param error_callback:
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
    def async_map(self,
                  function: Callable,
                  args_iter: Iterable = (),
                  chunksize: int = None,
                  callback: Callable = None,
                  error_callback: Callable = None) -> None:
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
    def async_map_by_args(self,
                          function: Callable,
                          args_iter: Iterable[Iterable] = (),
                          chunksize: int = None,
                          callback: Callable = None,
                          error_callback: Callable = None) -> None:
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
    def get_result(self) -> List[_OceanResult]:
        """
        Description:
            Get the running result.
        :return:
        """
        pass

