from pyocean.framework.features import (
    BaseQueue, BaseQueueType)
from pyocean.mode import FeatureMode
from pyocean.api.manager import Globalize
from pyocean.types import OceanQueue
from pyocean.adapter.base import QueueAdapterFactory, BaseAdapter
from pyocean._import_utils import ImportPyocean

from typing import Iterable, Any



class Queue(QueueAdapterFactory):

    def get_instance(self) -> OceanQueue:
        __queue = self._qtype.value
        return __queue


    def globalize_instance(self, obj) -> None:
        Globalize.queue(name=self._name, queue=obj)



class QueueAdapter(BaseAdapter, BaseQueue):

    def __init__(self, mode: FeatureMode):
        super().__init__(mode=mode)
        self.__queue_cls_name: str = self._running_info.get("queue")
        self.queue_cls = ImportPyocean.get_class(pkg_path=self._module, cls_name=self.__queue_cls_name)
        self.queue_instance: BaseQueue = self.queue_cls()


    def get_queue(self, qtype: BaseQueueType) -> OceanQueue:
        return self.queue_instance.get_queue(qtype=qtype)


    def init_queue_with_values(self, qtype: BaseQueueType, values: Iterable[Any]) -> OceanQueue:
        __queue = self.get_queue(qtype=qtype)
        for value in values:
            __queue.put(value)
        return __queue


    async def async_init_queue_with_values(self, qtype: BaseQueueType, values: Iterable[Any]) -> OceanQueue:
        __queue = self.get_queue(qtype=qtype)
        for value in values:
            await __queue.put(value)
        return __queue

