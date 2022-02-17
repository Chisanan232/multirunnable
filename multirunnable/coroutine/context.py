from ..framework.runnable.context import BaseContext

from typing import List, Set
import asyncio
import gevent.threading
import gevent



class green_thread_context(BaseContext):

    @staticmethod
    def get_current_worker() -> gevent.Greenlet:
        return gevent.getcurrent()


    @staticmethod
    def get_parent_worker() -> gevent.Greenlet:
        return gevent.threading.main_native_thread()


    @staticmethod
    def current_worker_is_parent() -> bool:
        return gevent.getcurrent() is gevent.threading.main_native_thread()


    @staticmethod
    def get_current_worker_ident() -> str:
        return str(gevent.threading.get_ident)


    @staticmethod
    def get_current_worker_name() -> str:
        return str(gevent.getcurrent().name)


    @staticmethod
    def current_worker_is_alive() -> bool:
        return gevent.getcurrent().dead is not True


    @staticmethod
    def active_workers_count() -> int:
        raise NotImplemented("Not implement via gevent currently.")


    @staticmethod
    def children_workers() -> List:
        raise NotImplemented("Not implement via gevent currently.")



class async_task_context(BaseContext):

    @staticmethod
    def get_current_worker() -> asyncio.Task:
        return asyncio.Task.current_task()


    @staticmethod
    def get_parent_worker() -> asyncio.Task:
        return asyncio.Task.current_task()


    @staticmethod
    def current_worker_is_parent() -> bool:
        return True


    @staticmethod
    def get_current_worker_ident() -> str:
        return str(id(async_task_context.get_current_worker()))


    @staticmethod
    def get_current_worker_name() -> str:
        return str(async_task_context.get_current_worker().get_name())


    @staticmethod
    def current_worker_is_alive() -> bool:
        return asyncio.Task.current_task().done() is False


    @staticmethod
    def active_workers_count() -> int:
        return len(asyncio.Task.all_tasks())


    @staticmethod
    def children_workers() -> Set[asyncio.Task]:
        return asyncio.Task.all_tasks()


