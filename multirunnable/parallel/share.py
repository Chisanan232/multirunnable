from multiprocessing.managers import BaseManager
from multiprocessing import managers, Manager
from inspect import isclass as inspect_isclass
from typing import Dict, Any

"""
Note:
    It raises exception about "TypeError: AutoProxy() got an unexpected 
    keyword argument 'manager_owned'" when it has nested manager scenario. 
    
    It's a bug of Python native package --- multiprocessing. Please refer to the URL below: 
    * Stackoverflow discussion: https://stackoverflow.com/questions/46779860/multiprocessing-managers-and-custom-classes
    * Python Bug record: https://bugs.python.org/issue30256
"""

# Backup original AutoProxy function
backup_autoproxy = managers.AutoProxy


# Defining a new AutoProxy that handles unwanted key argument 'manager_owned'
def redefined_autoproxy(token, serializer, manager=None, authkey=None, exposed=None, incref=True, manager_owned=True):
    # Calling original AutoProxy without the unwanted key argument
    return backup_autoproxy(token, serializer, manager, authkey, exposed, incref)


# Updating AutoProxy definition in multiprocessing.managers package
managers.AutoProxy = redefined_autoproxy


_Assign_Manager_Flag: Dict[str, bool] = {}
_Manager_Start_Flag: bool = False
_Current_Sharing_Manager: BaseManager = None

Global_Manager = Manager()


class _SharingManager(BaseManager):
    pass


def get_current_manager() -> BaseManager:
    return _Current_Sharing_Manager


def activate_manager_server() -> _SharingManager:
    return SharingManager()


def get_manager_attr(attr: str) -> Any:
    if _Current_Sharing_Manager is None:
        raise ValueError("Object _SharingManager not be initialed yet.")

    # if hasattr(_Current_Sharing_Manager, attr):    # The built-in function will not work finely here.
    if attr not in dir(_Current_Sharing_Manager):
        raise AttributeError("Target attribute doesn't exist.")

    return getattr(_Current_Sharing_Manager, attr)


def register_to_manager(target_cls: Any, proxytype: Any = None) -> None:
    """
    Description:
        Register the target class to sub-class of 'multiprocessing.managers.BaseManager'.
    :param proxytype:
    :param target_cls:
    :return:
    """

    global _Assign_Manager_Flag
    _chk_cls(target_cls)

    def _register() -> None:
        _SharingManager.register(typeid=str(_cls_name), callable=target_cls, proxytype=proxytype)
        _Assign_Manager_Flag[_cls_name] = True

    _cls_name = target_cls.__name__
    if _cls_name in _Assign_Manager_Flag.keys():
        if _Assign_Manager_Flag[_cls_name] is False:
            _register()
    else:
        _register()


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


def sharing_in_processes(proxytype: Any = None):
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

    :param proxytype:
    :return: The instance which could be used and shared in each different processes.
    """

    def _sharing(_class):

        _chk_cls(_class)

        def _(*args, **kwargs) -> Any:
            _cls_name = _class.__name__
            _cls = get_manager_attr(_cls_name)
            return _cls(*args, **kwargs)

        register_to_manager(target_cls=_class, proxytype=proxytype)
        return _

    return _sharing


def _chk_cls(_cls) -> None:
    if inspect_isclass(_cls) is False:
        raise ValueError("The target object be decorated should be a 'class' level type object.")

