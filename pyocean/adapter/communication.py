from pyocean.framework.features import PosixThreadCommunication as _PosixThreadCommunication
from pyocean.mode import FeatureMode as _FeatureMode
from pyocean.api.manage import Globalize as _Globalize
from pyocean.types import OceanEvent as _OceanEvent, OceanCondition as _OceanCondition
from pyocean.adapter.base import FeatureAdapterFactory as _FeatureAdapterFactory
from pyocean.adapter._utils import _ModuleFactory, _AsyncUtils



class Event(_FeatureAdapterFactory):

    def __str__(self):
        return super(Event, self).__str__().replace("TargetObject", "Event")


    def __repr__(self):
        return super(Event, self).__repr__().replace("TargetObject", "Event")


    def get_instance(self) -> _OceanEvent:
        communication_instance: _PosixThreadCommunication = _ModuleFactory.get_communication_adapter(mode=self.feature_mode)
        return communication_instance.get_event(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.event(event=obj)



class Condition(_FeatureAdapterFactory):

    def __str__(self):
        return super(Condition, self).__str__().replace("TargetObject", "Condition")


    def __repr__(self):
        __mode = self._Mode
        if __mode is _FeatureMode.Asynchronous:
            __loop = self._kwargs.get("loop", None)
            __lock = self._kwargs.get("lock", None)
            return f"<Condition(loop={__loop}, lock={__lock}) object with {__mode} mode at {id(self)}>"
        else:
            return self.__str__()


    def get_instance(self, **kwargs) -> _OceanCondition:
        if self._Mode is _FeatureMode.Asynchronous:
            self._kwargs["lock"] = _AsyncUtils.check_lock(lock=kwargs.get("lock", None))
        communication_instance: _PosixThreadCommunication = _ModuleFactory.get_communication_adapter(mode=self.feature_mode)
        return communication_instance.get_condition(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.condition(condition=obj)

