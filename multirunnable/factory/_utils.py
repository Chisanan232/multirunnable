from typing import Dict, Tuple, Type, Union

from ..framework.runnable import (
    BaseContext,
    PosixThreadLock,
    PosixThreadCommunication,
    BaseQueue
)
from .._import_utils import ImportMultiRunnable
from ..mode import ContextMode, FeatureMode



class _ModuleFactory:

    @staticmethod
    def get_lock_adapter(mode: FeatureMode) -> PosixThreadLock:
        __module, __lock_cls_name = _ModuleFactory.get_module(mode=mode, cls="lock")
        lock_cls = ImportMultiRunnable.get_class(pkg_path=__module, cls_name=__lock_cls_name)
        return lock_cls()


    @staticmethod
    def get_communication_adapter(mode: FeatureMode) -> PosixThreadCommunication:
        __module, __communication_cls_name = _ModuleFactory.get_module(mode=mode, cls="communication")
        communication_cls = ImportMultiRunnable.get_class(pkg_path=__module, cls_name=__communication_cls_name)
        return communication_cls()


    @staticmethod
    def get_queue_adapter(mode: FeatureMode) -> BaseQueue:
        __module, __queue_cls_name = _ModuleFactory.get_module(mode=mode, cls="queue")
        queue_cls = ImportMultiRunnable.get_class(pkg_path=__module, cls_name=__queue_cls_name)
        return queue_cls


    @staticmethod
    def get_context(mode: ContextMode) -> Type[BaseContext]:
        __module, __lock_cls_name = _ModuleFactory.get_module(mode=mode, cls="context")
        lock_cls = ImportMultiRunnable.get_class(pkg_path=__module, cls_name=__lock_cls_name)
        return lock_cls


    @staticmethod
    def get_module(mode: Union[FeatureMode, ContextMode], cls: str) -> Tuple[str, str]:
        _running_info: Dict[str, str] = mode.value
        __module: str = _running_info.get("module")
        __cls_name: str = _running_info.get(cls)
        return __module, __cls_name



class _AsyncUtils:

    @staticmethod
    def check_event_loop(event_loop):
        if event_loop is None:
            raise Exception("Async Event Loop object cannot be empty.")
        return event_loop


    @staticmethod
    def check_lock(lock):
        if lock:
            raise Exception("Async Lock object cannot be empty.")
        return lock

