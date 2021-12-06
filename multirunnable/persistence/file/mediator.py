from abc import ABCMeta, abstractmethod
import re



class BaseMediator(metaclass=ABCMeta):

    @property
    @abstractmethod
    def worker_id(self) -> str:
        pass


    @worker_id.setter
    @abstractmethod
    def worker_id(self, worker_id: str) -> None:
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

    @property
    def worker_id(self) -> str:
        return self.__Worker_ID


    @worker_id.setter
    def worker_id(self, worker_id: str) -> None:
        self.__Worker_ID = worker_id


    @worker_id.deleter
    def worker_id(self) -> None:
        del self.__Worker_ID


    def is_super_worker(self) -> bool:
        import threading
        checksum = threading.current_thread() is threading.main_thread()
        print(f"Main thread Checksum: {checksum}")
        return checksum
        # return re.search(r"", self.__Worker_ID, re.IGNORECASE) is not None


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

