from abc import ABCMeta
from typing import Dict, TypeVar, Generic, Any
from inspect import isclass as inspect_isclass


T = TypeVar("T")


def chk_cls(_cls):
    if inspect_isclass(_cls) is False:
        raise ValueError("The target object be decorated should be a 'class' level type object.")


def simple_singleton(_class):

    chk_cls(_class)

    __Instance: Generic[T] = None

    def get_instance(*args, **kwargs):
        nonlocal __Instance
        if __Instance is None:
            __Instance = _class(*args, **kwargs)
        return __Instance

    return get_instance



def singleton(_class):

    chk_cls(_class)

    class _SingletonClass(_class):

        _Instance: Generic[T] = None

        def __new__(_class, *args, **kwargs):
            if _SingletonClass._Instance is None:
                _SingletonClass._Instance = super(_SingletonClass, _class).__new__(_class)
                _SingletonClass._Instance._sealed = False
            return _SingletonClass._Instance


        def __init__(self, *args, **kwargs):
            if _SingletonClass._Instance._sealed:
                return
            super(_SingletonClass, self).__init__(*args, **kwargs)
            _SingletonClass._Instance._sealed = True


    _SingletonClass.__name__ = _class.__name__
    _SingletonClass.__doc__ = _class.__doc__
    _SingletonClass.__str__ = _class.__str__
    _SingletonClass.__repr__ = _class.__repr__

    return _SingletonClass



class Singleton:

    _Instance: Generic[T] = None

    def __new__(cls, *args, **kwargs):
        if cls._Instance is None:
            cls._Instance = super(Singleton, cls).__new__(cls)
        return cls._Instance



class NamedSingleton:

    _Instances: Dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        _cls_name = cls.__name__
        if _cls_name not in cls._Instances.keys():
            cls._Instances[_cls_name] = super(NamedSingleton, cls).__new__(cls)
        return cls._Instances[_cls_name]



class ConnectionPoolSingleton:

    _Instances: Dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        _pool_name = kwargs.get("pool_name", "")
        if _pool_name not in cls._Instances.keys():
            cls._Instances[_pool_name] = super(ConnectionPoolSingleton, cls).__new__(cls)
        return cls._Instances[_pool_name]



class SingletonMeta(type):

    _Instance: Generic[T] = None

    def __call__(cls, *args, **kwargs):
        if cls._Instance is None:
            __super_cls = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._Instance = __super_cls
        return cls._Instance



class NamedSingletonMeta(type):

    _Instances: Dict[str, Any] = {}

    def __call__(cls, *args, **kwargs):
        _cls_name = cls.__name__
        if _cls_name not in cls._Instances:
            __super_cls = super(NamedSingletonMeta, cls).__call__(*args, **kwargs)
            cls._Instances[_cls_name] = __super_cls
        return cls._Instances[_cls_name]



class NamedSingletonABCMeta(ABCMeta):

    _NamedInstances: Dict[str, Any] = {}

    def __call__(cls, *args, **kwargs):
        _cls_name = cls.__name__
        if _cls_name not in cls._NamedInstances:
            __super_cls = super(NamedSingletonABCMeta, cls).__call__(*args, **kwargs)
            cls._NamedInstances[_cls_name] = __super_cls
        return cls._NamedInstances[_cls_name]


