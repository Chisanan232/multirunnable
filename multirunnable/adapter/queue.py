from multirunnable.api.manage import Globalize as _Globalize
from multirunnable.types import OceanQueue as _OceanQueue
from multirunnable.adapter.base import QueueAdapterFactory as _QueueAdapterFactory



class Queue(_QueueAdapterFactory):

    def get_instance(self) -> _OceanQueue:
        __queue = self._qtype.value
        return __queue


    def globalize_instance(self, obj) -> None:
        _Globalize.queue(name=self._name, queue=obj)

