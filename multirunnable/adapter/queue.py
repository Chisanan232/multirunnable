from multirunnable.api.manage import Globalize as _Globalize
from multirunnable.types import MRQueue as _MRQueue
from multirunnable.adapter.base import QueueAdapterFactory as _QueueAdapterFactory
from multirunnable.adapter._utils import _ModuleFactory



class Queue(_QueueAdapterFactory):

    def __repr__(self):
        return f"<Queue Object(name={self._name}, qtype=Queue) ar {id(self)}>"


    def get_instance(self) -> _MRQueue:
        queue_instance = _ModuleFactory.get_queue_adapter(mode=self.feature_mode)
        __queue = queue_instance.value
        return __queue


    def globalize_instance(self, obj) -> None:
        _Globalize.queue(name=self._name, queue=obj)



class QueueAdapter(_QueueAdapterFactory):

    def __init__(self, **kwargs):
        super(QueueAdapter, self).__init__(name=kwargs.get("name", None))

        self._qtype = kwargs.get("qtype", None)
        if self._qtype is None:
            raise Exception("Queue type parameter shouldn't be None object. "
                            "It must to choice a type of Queue object with mapping strategy.")


    def __repr__(self):
        return f"<Queue Object(name={self._name}, qtype={self._qtype}) ar {id(self)}>"


    def get_instance(self) -> _MRQueue:
        __queue = self._qtype.value
        return __queue


    def globalize_instance(self, obj) -> None:
        _Globalize.queue(name=self._name, queue=obj)


