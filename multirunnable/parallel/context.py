from .. import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from ..framework.runnable.context import BaseContext

from multiprocessing.process import BaseProcess
if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 7):
    from multiprocessing import current_process, parent_process, active_children as active_children_process
else:
    from multiprocessing import current_process, active_children as active_children_process
from typing import List



class context(BaseContext):

    @staticmethod
    def get_current_worker() -> BaseProcess:
        return current_process()


    @staticmethod
    def get_parent_worker() -> BaseProcess:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 7):
            return parent_process()
        else:
            raise NotImplemented("It doesn't support to get parent process via APIs of multiprocessing less than Python 3.8.")


    @staticmethod
    def current_worker_is_parent() -> bool:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 7):
            return current_process() is parent_process()
        else:
            raise NotImplemented("It doesn't support to get parent process via APIs of multiprocessing less than Python 3.8.")


    @staticmethod
    def get_current_worker_ident() -> str:
        return str(current_process().ident)


    @staticmethod
    def get_current_worker_name() -> str:
        return str(current_process().name)


    @staticmethod
    def current_worker_is_alive() -> bool:
        return current_process().is_alive()


    @staticmethod
    def active_workers_count() -> int:
        return len(active_children_process())


    @staticmethod
    def children_workers() -> List[BaseProcess]:
        return active_children_process()

