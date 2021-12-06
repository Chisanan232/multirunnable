from multiprocessing.managers import BaseManager
from inspect import isclass as inspect_isclass
from typing import Dict, Any


_Assign_Manager_Flag: Dict[str, bool] = {}
_Manager_Start_Flag: bool = False
_Current_Sharing_Manager: BaseManager


class _SharingManager(BaseManager):
    pass


def get_current_manager() -> BaseManager:
    return _Current_Sharing_Manager


def get_manager_attr(attr: str) -> Any:
    if _Current_Sharing_Manager is None:
        raise ValueError("Object _SharingManager not be initialed yet.")

    # if hasattr(_Current_Sharing_Manager, attr):    # The built-in function will not work finely here.
    if attr not in dir(_Current_Sharing_Manager):
        raise AttributeError("Target attribute doesn't exist.")

    return getattr(_Current_Sharing_Manager, attr)


def assign_to_manager(target_cls) -> None:
    """
    Description:
        Register the target class to sub-class of 'multiprocessing.managers.BaseManager'.
    :param target_cls:
    :return:
    """

    global _Assign_Manager_Flag
    _chk_cls(target_cls)

    def _assign() -> None:
        _SharingManager.register(typeid=str(_cls_name), callable=target_cls)
        _Assign_Manager_Flag[_cls_name] = True

    _cls_name = target_cls.__name__
    if _cls_name in _Assign_Manager_Flag.keys():
        if _Assign_Manager_Flag[_cls_name] is False:
            _assign()
    else:
        _assign()


def SharingManager() -> _SharingManager:
    """
    Description:
        Initial sub-class of  'multiprocessing.managers.BaseManager'.
    :return:
    """
    global _Manager_Start_Flag, _Current_Sharing_Manager
    if _Manager_Start_Flag is False:
        _Current_Sharing_Manager = _SharingManager()
        _Current_Sharing_Manager.start()
        _Manager_Start_Flag = True

    return _Current_Sharing_Manager


def sharing_in_processes(_class):
    """
    Description:
        This is a decorator which could register target class into sub-class of
        'multiprocessing.managers.BaseManager' object.
        It also could help you get the instance which has been registered and could be shared between processes.

    Usage example:

        @sharing_in_processes
        class Foo:
            ...

        _foo = Foo()    # It could be used and shared in each different processes.

    :param _class: A class.
    :return: The instance which could be used and shared in each different processes.
    """

    _chk_cls(_class)

    def _(*args, **kwargs) -> Any:
        _cls_name = _class.__name__
        _cls = get_manager_attr(_cls_name)
        print(f"[DEBUG] sharing_in_processes._cls: {_cls}")
        print(f"[DEBUG] sharing_in_processes.args: {args}")
        print(f"[DEBUG] sharing_in_processes.kwargs: {kwargs}")
        return _cls(*args, **kwargs)

    assign_to_manager(_class)
    return _


def _chk_cls(_cls) -> None:
    if inspect_isclass(_cls) is False:
        raise ValueError("The target object be decorated should be a 'class' level type object.")

