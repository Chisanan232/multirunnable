from multirunnable.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from multirunnable.framework.adapter.collection import BaseList as _BaseList
from multirunnable.mode import FeatureMode as _FeatureMode
from multirunnable.adapter.collection import FeatureList as _FeatureList
from multirunnable.adapter._utils import _AsyncUtils

from abc import ABC



class FeatureAdapterFactory(_BaseFeatureAdapterFactory, ABC):

    _Mode: _FeatureMode = None
    _Feature_List: _BaseList = None

    def __init__(self):
        self._kwargs = {}


    def __str__(self):
        return f"<TargetObject Adapter object with {self._Mode} mode at {id(self)}>"


    def __repr__(self):
        __mode = self._Mode
        if self._Mode is _FeatureMode.Asynchronous:
            __loop = self._kwargs.get("loop", None)
            return f"<TargetObject(loop={__loop}) Adapter object with {__mode} mode at {id(self)}>"
        else:
            return f"<TargetObject() Adapter object with {__mode} mode at {id(self)}>"


    def __add__(self, other) -> _BaseList:
        if isinstance(other, _BaseList):
            other.append(self)
            self._Feature_List = other
        else:
            if self._Feature_List is None:
                self._Feature_List = _FeatureList()
            self._Feature_List.append(self)
            self._Feature_List.append(other)
        return self._Feature_List


    @property
    def feature_mode(self) -> _FeatureMode:
        return self._Mode


    @feature_mode.setter
    def feature_mode(self, mode: _FeatureMode) -> None:
        self._Mode = mode


    def _chk_param_by_mode(self, **kwargs):
        if self._Mode is _FeatureMode.Asynchronous:
            self._kwargs["loop"] = _AsyncUtils.check_event_loop(event_loop=kwargs.get("event_loop", None))



class QueueAdapterFactory(_BaseFeatureAdapterFactory, ABC):

    def __init__(self, **kwargs):
        self._name = kwargs.get("name", None)
        if self._name is None:
            raise Exception("The name of Queue object shouldn't be None object. "
                            "It's the key of each Queue object you create.")

        self._qtype = kwargs.get("qtype", None)
        if self._qtype is None:
            raise Exception("Queue type parameter shouldn't be None object. "
                            "It must to choice a type of Queue object with mapping strategy.")


    def __str__(self):
        return f"<Queue Object at {id(self)}>"


    def __repr__(self):
        return f"<Queue Object(name={self._name}, qtype={self._qtype}) ar {id(self)}>"

