from pyocean.framework.features import BaseFeatureAdapterFactory
from pyocean.framework.collection import BaseList
from pyocean.mode import FeatureMode
from pyocean.adapter.collection import FeatureList
from pyocean.adapter._utils import _AsyncUtils

from abc import ABCMeta, ABC
from typing import Dict



class FeatureAdapterFactory(BaseFeatureAdapterFactory, ABC):

    _Feature_List: BaseList = None

    def __init__(self, mode: FeatureMode, **kwargs):
        super(FeatureAdapterFactory, self).__init__(mode=mode, **kwargs)
        if self._mode is FeatureMode.Asynchronous:
            self._kwargs["loop"] = _AsyncUtils.check_event_loop(event_loop=kwargs.get("event_loop", None))


    def __add__(self, other) -> BaseList:
        if isinstance(other, BaseList):
            other.append(self)
            self._Feature_List = other
        else:
            if self._Feature_List is None:
                self._Feature_List = FeatureList()
            self._Feature_List.append(self)
            self._Feature_List.append(other)
        return self._Feature_List



class QueueAdapterFactory(BaseFeatureAdapterFactory, ABC):

    def __init__(self, **kwargs):
        super(QueueAdapterFactory, self).__init__(**kwargs)



class BaseAdapter(metaclass=ABCMeta):

    def __init__(self, mode: FeatureMode):
        """
        Description:
            It will import the target module and instancing the target class to be the instance object.
            In the other words, it will
              1. If it's parallel strategy, import pyocean.parallel.features.MultiProcessing.
              2. If it's concurrent strategy, import pyocean.concurrent.features.{MultiThreading, Coroutine or Asynchronous}.
        :param mode:
        """

        self._mode = mode
        self._running_info: Dict[str, str] = mode.value
        self._module: str = self._running_info.get("module")

