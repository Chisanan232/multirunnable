from pyocean.framework.features import BaseAPI, BaseQueueType
from pyocean.api.mode import RunningMode

from importlib import import_module
from typing import Dict, Callable
import logging


_Package: str = "pyocean"
_Parallel_Module: str = ".parallel.features"
_Concurrent_Module: str = ".concurrent.features"



class RunningStrategyAPI(BaseAPI):

    def __init__(self, mode: RunningMode):
        """
        Description:
            It will import the target module and instancing the target class to be the instance object.
            In the other words, it will
              1. If it's parallel strategy, import pyocean.parallel.features.MultiProcessing.
              2. If it's concurrent strategy, import pyocean.concurrent.features.{MultiThreading, Coroutine or Asynchronous}.
        :param mode:
        """

        __running_info: Dict[str, str] = mode.value
        self.__module_info: str = __running_info.get("module")
        self.__class_info: str = __running_info.get("class")
        self.__package = import_module(name=self.__module_info, package=_Package)
        logging.debug(f"package obj: {self.__package}")
        self.__class: Callable = getattr(self.__package, self.__class_info)
        self.__class_instance = self.__class()
        logging.debug(f"__class: {self.__class}")
        logging.debug(f"__class_instance: {self.__class_instance}")


    def lock(self):
        return self.__class_instance.lock()


    def event(self, **kwargs):
        return self.__class_instance.event(**kwargs)


    def condition(self, **kwargs):
        return self.__class_instance.condition(**kwargs)


    def semaphore(self, value: int):
        return self.__class_instance.semaphore(value=value)


    def bounded_semaphore(self, value: int):
        return self.__class_instance.bounded_semaphore(value=value)


    def queue(self, qtype: BaseQueueType):
        if not isinstance(qtype, BaseQueueType):
            raise TypeError("Parameter 'qtype' should be one value of object 'BaseQueueType'.")
        return self.__class_instance.queue(qtype=qtype)

