from abc import ABC

from ..framework.factory import (
    BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory,
    BaseList as _BaseList)
from ..factory.collection import FeatureList as _FeatureList
from ..factory._utils import _AsyncUtils
from ..mode import FeatureMode as _FeatureMode



class FeatureAdapterFactory(_BaseFeatureAdapterFactory, ABC):

    _Mode: _FeatureMode = None
    _Feature_List: _BaseList = None

    def __init__(self):
        self._kwargs = {}


    def __str__(self):
        return f"<TargetObject object with {self._Mode} mode at {id(self)}e>"


    def __repr__(self):
        __mode = self._Mode
        if self._Mode is _FeatureMode.Asynchronous:
            __loop = self._kwargs.get("loop", None)
            return f"<TargetObject(loop={__loop}) object with {__mode} mode at {id(self)}>"
        else:
            return f"<TargetObject() object with {__mode} mode at {id(self)}>"


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
        if type(mode) is not _FeatureMode:
            raise ValueError("The mode type should be *FeatureMode*.")
        self._Mode = mode


    def _chk_param_by_mode(self, **kwargs):
        if self._Mode is _FeatureMode.Asynchronous:
            self._kwargs["loop"] = _AsyncUtils.check_event_loop(event_loop=kwargs.get("event_loop", None))



class QueueAdapterFactory(_BaseFeatureAdapterFactory, ABC):

    _Mode: _FeatureMode = None

    def __init__(self, **kwargs):
        self._name = kwargs.get("name", None)
        if self._name is None:
            raise Exception("The name of Queue object shouldn't be None object. "
                            "It's the key of each Queue object you create.")


    def __str__(self):
        return f"<Queue Object at {id(self)}>"


    @property
    def feature_mode(self) -> _FeatureMode:
        return self._Mode


    @feature_mode.setter
    def feature_mode(self, mode: _FeatureMode) -> None:
        self._Mode = mode

