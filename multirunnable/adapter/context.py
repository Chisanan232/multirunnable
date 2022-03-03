from multirunnable.framework.runnable.context import BaseContext
from multirunnable import get_current_mode
from multirunnable.mode import ContextMode
from multirunnable.factory._utils import _ModuleFactory

from typing import List, Union
from gevent import Greenlet
from asyncio import Task
from threading import Thread
from multiprocessing.process import BaseProcess



class context(BaseContext):

    @staticmethod
    def get_current_worker() -> Union[BaseProcess, Thread, Greenlet, Task]:
        _cmode = context._get_cmode()
        return _ModuleFactory.get_context(mode=_cmode).get_current_worker()


    @staticmethod
    def get_parent_worker() -> Union[BaseProcess, Thread, Greenlet, Task]:
        _cmode = context._get_cmode()
        return _ModuleFactory.get_context(mode=_cmode).get_parent_worker()


    @staticmethod
    def current_worker_is_parent() -> bool:
        _cmode = context._get_cmode()
        return _ModuleFactory.get_context(mode=_cmode).current_worker_is_parent()


    @staticmethod
    def get_current_worker_ident() -> str:
        _cmode = context._get_cmode()
        return _ModuleFactory.get_context(mode=_cmode).get_current_worker_ident()


    @staticmethod
    def get_current_worker_name() -> str:
        _cmode = context._get_cmode()
        return _ModuleFactory.get_context(mode=_cmode).get_current_worker_name()


    @staticmethod
    def current_worker_is_alive() -> bool:
        _cmode = context._get_cmode()
        return _ModuleFactory.get_context(mode=_cmode).current_worker_is_alive()


    @staticmethod
    def active_workers_count() -> int:
        _cmode = context._get_cmode()
        return _ModuleFactory.get_context(mode=_cmode).active_workers_count()


    @staticmethod
    def children_workers() -> List[Union[BaseProcess, Thread, Greenlet, Task]]:
        _cmode = context._get_cmode()
        return _ModuleFactory.get_context(mode=_cmode).children_workers()


    @staticmethod
    def _get_cmode() -> ContextMode:
        _rmode = get_current_mode(force=True)
        _cmode = _rmode.value["context"]
        return _cmode

