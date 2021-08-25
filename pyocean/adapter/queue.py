from pyocean.api.manager import Globalize as _Globalize
from pyocean.types import OceanQueue as _OceanQueue
from pyocean.adapter.base import QueueAdapterFactory as _QueueAdapterFactory



class Queue(_QueueAdapterFactory):

    def get_instance(self) -> _OceanQueue:
        __queue = self._qtype.value
        return __queue


    def globalize_instance(self, obj) -> None:
        _Globalize.queue(name=self._name, queue=obj)

