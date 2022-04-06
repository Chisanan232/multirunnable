from ..framework.runnable.synchronization import PosixThreadCommunication as _PosixThreadCommunication
from ..factory._utils import _ModuleFactory, _AsyncUtils
from ..factory.base import FeatureAdapterFactory as _FeatureAdapterFactory
from ..api.manage import Globalize as _Globalize
from ..types import MREvent as _MREvent, MRCondition as _MRCondition
from ..mode import FeatureMode as _FeatureMode



class EventFactory(_FeatureAdapterFactory):

    def __str__(self):
        return super(EventFactory, self).__str__().replace("TargetObject", "Event")


    def __repr__(self):
        return super(EventFactory, self).__repr__().replace("TargetObject", "Event")


    def get_instance(self, **kwargs) -> _MREvent:
        self._chk_param_by_mode(**kwargs)
        if self.feature_mode is None:
            raise ValueError("FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'.")

        communication_instance: _PosixThreadCommunication = _ModuleFactory.get_communication_adapter(mode=self.feature_mode)
        return communication_instance.get_event(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.event(event=obj)



class ConditionFactory(_FeatureAdapterFactory):

    def __str__(self):
        return super(ConditionFactory, self).__str__().replace("TargetObject", "Condition")


    def __repr__(self):
        __mode = self._Mode
        if __mode is _FeatureMode.Asynchronous:
            __loop = self._kwargs.get("loop", None)
            __lock = self._kwargs.get("lock", None)
            return f"<Condition(loop={__loop}, lock={__lock}) object with {__mode} mode at {id(self)}>"
        else:
            return self.__str__()


    def get_instance(self, **kwargs) -> _MRCondition:
        self._chk_param_by_mode(**kwargs)
        if self.feature_mode is None:
            raise ValueError("FeatureMode is None. Please configure it as one of 'multirunnable.mode.FeatureMode'.")

        if self._Mode is _FeatureMode.Asynchronous:
            self._kwargs["lock"] = _AsyncUtils.check_lock(lock=kwargs.get("lock", None))

        communication_instance: _PosixThreadCommunication = _ModuleFactory.get_communication_adapter(mode=self.feature_mode)
        return communication_instance.get_condition(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        _Globalize.condition(condition=obj)

