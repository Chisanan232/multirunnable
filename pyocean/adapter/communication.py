from pyocean.framework.features import PosixThreadCommunication
from pyocean.mode import FeatureMode
from pyocean.api.manager import Globalize
from pyocean.types import OceanEvent, OceanCondition
from pyocean.adapter.base import FeatureAdapterFactory, BaseAdapter
from pyocean.adapter._utils import _ModuleFactory, _AsyncUtils
from pyocean._import_utils import ImportPyocean



class Event(FeatureAdapterFactory):

    def __str__(self):
        return super(Event, self).__str__().replace("TargetObject", "Event")


    def __repr__(self):
        return super(Event, self).__repr__().replace("TargetObject", "Event")


    def get_instance(self) -> OceanEvent:
        communication_instance: PosixThreadCommunication = _ModuleFactory.get_communication_adapter(mode=self._mode)
        return communication_instance.get_event(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.event(event=obj)



class Condition(FeatureAdapterFactory):

    def __init__(self, mode: FeatureMode, **kwargs):
        super(Condition, self).__init__(mode=mode, **kwargs)
        if self._mode is FeatureMode.Asynchronous:
            self._kwargs["lock"] = _AsyncUtils.check_lock(lock=kwargs.get("lock", None))


    def __str__(self):
        return super(Condition, self).__str__().replace("TargetObject", "Condition")


    def __repr__(self):
        __mode = self._mode
        if __mode is FeatureMode.Asynchronous:
            __loop = self._kwargs["loop"]
            __lock = self._kwargs["lock"]
            return f"<Condition(loop={__loop}, lock={__lock}) object with {__mode} mode at {id(self)}>"
        else:
            return self.__str__()


    def get_instance(self) -> OceanCondition:
        communication_instance: PosixThreadCommunication = _ModuleFactory.get_communication_adapter(mode=self._mode)
        return communication_instance.get_condition(**self._kwargs)


    def globalize_instance(self, obj) -> None:
        Globalize.condition(condition=obj)



class CommunicationAdapter(BaseAdapter, PosixThreadCommunication):

    def __init__(self, mode: FeatureMode, **kwargs):
        super().__init__(mode=mode)
        self.__communication_cls_name: str = self._running_info.get("communication")
        self.communication_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__communication_cls_name)
        self.communication_instance: PosixThreadCommunication = self.communication_cls()

        if mode is FeatureMode.Asynchronous:
            self.__event_loop = kwargs.get("event_loop", None)
            if self.__event_loop is None:
                raise Exception("Async Event Loop object cannot be empty.")


    def get_event(self, *args, **kwargs) -> OceanEvent:
        if self._mode is FeatureMode.Asynchronous:
            kwargs["loop"] = self.__event_loop
        if self._mode is FeatureMode.Asynchronous:
            return self.communication_instance.get_event(*args, **kwargs)
        else:
            return self.communication_instance.get_event()


    def get_condition(self, *args, **kwargs) -> OceanCondition:
        if self._mode is FeatureMode.Asynchronous:
            if kwargs.get("lock", None):
                raise Exception("Async Lock object cannot be empty.")
            kwargs["loop"] = self.__event_loop
        if self._mode is FeatureMode.Asynchronous:
            return self.communication_instance.get_condition(*args, **kwargs)
        else:
            return self.communication_instance.get_condition()

