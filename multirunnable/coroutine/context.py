from typing import List, Set
import gevent.threading
import asyncio
import gevent

from ..framework.runnable.context import BaseContext
from .. import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION



class green_thread_context(BaseContext):

    @staticmethod
    def get_current_worker() -> gevent.Greenlet:
        return gevent.getcurrent()


    @staticmethod
    def get_parent_worker() -> gevent.Greenlet:
        return gevent.threading.main_native_thread()


    @staticmethod
    def current_worker_is_parent() -> bool:
        return gevent.threading.__threading__.current_thread() is gevent.threading.__threading__.main_thread()


    @staticmethod
    def get_current_worker_ident() -> str:
        return str(gevent.threading.get_ident)


    @staticmethod
    def get_current_worker_name() -> str:
        return str(gevent.threading.__threading__.current_thread().name).replace("Thread", "GreenThread")
        # return str(gevent.getcurrent().name)


    @staticmethod
    def current_worker_is_alive() -> bool:
        return gevent.getcurrent().dead is not True


    @staticmethod
    def active_workers_count() -> int:
        # raise NotImplemented("Not implement via gevent currently.")
        return gevent.threading.__threading__.active_count()


    @staticmethod
    def children_workers() -> List:
        # raise NotImplemented("Not implement via gevent currently.")
        return gevent.threading.__threading__.enumerate()



class async_task_context(BaseContext):

    @staticmethod
    def get_current_worker() -> asyncio.Task:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            return asyncio.current_task()
        else:
            return asyncio.Task.current_task()


    @staticmethod
    def get_parent_worker() -> asyncio.Task:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            return asyncio.current_task()
        else:
            return asyncio.Task.current_task()


    @staticmethod
    def current_worker_is_parent() -> bool:
        return True


    @staticmethod
    def get_current_worker_ident() -> str:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            return str(id(asyncio.current_task()))
        else:
            return str(id(async_task_context.get_current_worker()))


    @staticmethod
    def get_current_worker_name() -> str:
        return async_task_context.get_current_worker().get_name()


    @staticmethod
    def current_worker_is_alive() -> bool:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            return asyncio.current_task().done() is False
        else:
            return asyncio.Task.current_task().done() is False


    @staticmethod
    def active_workers_count() -> int:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            return len(asyncio.all_tasks())
        else:
            return len(asyncio.Task.all_tasks())


    @staticmethod
    def children_workers() -> Set[asyncio.Task]:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            return asyncio.all_tasks()
        else:
            return asyncio.Task.all_tasks()

