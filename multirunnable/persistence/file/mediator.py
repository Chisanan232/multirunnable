from abc import ABCMeta, abstractmethod

from ...framework.runnable.context import BaseContext
from ...adapter.context import context as context_adapter
from ... import get_current_mode



class BaseMediator(metaclass=ABCMeta):

    @property
    @abstractmethod
    def worker_id(self) -> str:
        pass


    @worker_id.setter
    @abstractmethod
    def worker_id(self, worker_id: str) -> None:
        pass


    @property
    @abstractmethod
    def activate_count(self) -> int:
        pass


    @abstractmethod
    def is_super_worker(self) -> bool:
        pass


    @property
    @abstractmethod
    def super_worker_running(self) -> bool:
        pass


    @super_worker_running.setter
    @abstractmethod
    def super_worker_running(self, activate: bool) -> None:
        pass


    @property
    @abstractmethod
    def child_worker_running(self) -> bool:
        pass


    @child_worker_running.setter
    @abstractmethod
    def child_worker_running(self, activate: bool) -> None:
        pass


    @property
    @abstractmethod
    def enable_compress(self) -> bool:
        pass


    @enable_compress.setter
    @abstractmethod
    def enable_compress(self, enable: bool) -> None:
        pass



class SavingMediator(BaseMediator):

    __Worker_ID: str = None
    __Activate_Super_Worker: bool = False
    __Activate_Child_Worker: bool = False
    __Enable_Compress: bool = False


    def __init__(self, context: BaseContext = None):
        if context is None:
            _rmode = get_current_mode()
            if _rmode is None:
                raise ValueError("The RunningMode in context cannot be None object if option *context* is None.")
            self._context = context_adapter
        else:
            self._context = context


    @property
    def worker_id(self) -> str:
        return self.__Worker_ID


    @worker_id.setter
    def worker_id(self, worker_id: str) -> None:
        self.__Worker_ID = worker_id


    @worker_id.deleter
    def worker_id(self) -> None:
        del self.__Worker_ID


    @property
    def activate_count(self) -> int:
        return self._context.active_workers_count()


    def is_super_worker(self) -> bool:
        return self._context.current_worker_is_parent()


    @property
    def super_worker_running(self) -> bool:
        return self.__Activate_Super_Worker


    @super_worker_running.setter
    def super_worker_running(self, activate: bool) -> None:
        self.__Activate_Super_Worker = activate


    @property
    def child_worker_running(self) -> bool:
        return self.__Activate_Child_Worker


    @child_worker_running.setter
    def child_worker_running(self, activate: bool) -> None:
        self.__Activate_Child_Worker = activate


    @property
    def enable_compress(self) -> bool:
        return self.__Enable_Compress


    @enable_compress.setter
    def enable_compress(self, enable: bool) -> None:
        self.__Enable_Compress = enable

