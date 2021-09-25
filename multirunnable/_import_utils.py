from importlib import import_module
from typing import Callable
import re



class ImportMultiRunnable:

    _RootPackage = "multirunnable"

    @classmethod
    def get_class(cls, pkg_path: str, cls_name: str) -> Callable:
        """
        Description:
            Get the target class object by importing path and class name in string.
        :param pkg_path: importing path from modules.
        :param cls_name: the target class.
        :return: Class object.
        """
        __chksum = cls.__chk_pkg_path(pkg_path=pkg_path)
        if __chksum:
            __package = import_module(name=pkg_path, package=cls._RootPackage)
            __class: Callable = getattr(__package, cls_name)
            return __class


    @classmethod
    def __chk_pkg_path(cls, pkg_path: str) -> bool:
        """
        Description:
            Check whether the path  of importing module or class is correct or not.
            It raises ImportError if the importing path is wrong.
        :param pkg_path: importing path from modules.
        :return: True or raising ImportError.
        """
        if re.search(r".\w{2,64}", pkg_path):
            return True
        else:
            raise ImportError("The format of package path parameter value is incorrect.")
