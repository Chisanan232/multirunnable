from multiprocessing.process import BaseProcess
from threading import Thread
from asyncio import Task
from gevent import Greenlet
from typing import List, Union

from ..framework.runnable.context import BaseContext
from ..factory._utils import _ModuleFactory
from ..mode import ContextMode
from .. import get_current_mode



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

