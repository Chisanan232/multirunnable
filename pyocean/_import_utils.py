from importlib import import_module
from typing import Callable
import re



class ImportPyocean:

    _RootPackage = "pyocean"

    @classmethod
    def get_class(cls, pkg_path: str, cls_name: str) -> Callable:
        __chksum = cls.__chk_pkg_path(pkg_path=pkg_path)
        if __chksum:
            __package = import_module(name=pkg_path, package=cls._RootPackage)
            __class: Callable = getattr(__package, cls_name)
            return __class


    @classmethod
    def __chk_pkg_path(cls, pkg_path: str) -> bool:
        if re.search(r".\w{2,64}", pkg_path):
            return True
        else:
            raise ImportError("The format of package path parameter value is incorrect.")
