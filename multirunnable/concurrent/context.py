from typing import List
from threading import current_thread, main_thread, active_count, enumerate, Thread

from ..framework.runnable.context import BaseContext



class context(BaseContext):

    @staticmethod
    def get_current_worker() -> Thread:
        return current_thread()


    @staticmethod
    def get_parent_worker() -> Thread:
        return main_thread()


    @staticmethod
    def current_worker_is_parent() -> bool:
        return current_thread() is main_thread()


    @staticmethod
    def get_current_worker_ident() -> str:
        return str(current_thread().ident)


    @staticmethod
    def get_current_worker_name() -> str:
        return str(current_thread().name)


    @staticmethod
    def current_worker_is_alive() -> bool:
        return current_thread().is_alive()


    @staticmethod
    def active_workers_count() -> int:
        return active_count()


    @staticmethod
    def children_workers() -> List[Thread]:
        return enumerate()

