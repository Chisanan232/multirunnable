from pyocean.framework.features import (
    BaseQueue, BaseQueueType)
from pyocean.mode import FeatureMode
from pyocean.api.manager import Globalize
from pyocean.types import OceanQueue
from pyocean.adapter.base import QueueAdapterFactory, BaseAdapter
# from pyocean.adapter.collection import QueueTaskList
# from pyocean.adapter._utils import _ModuleFactory
from pyocean._import_utils import ImportPyocean

from typing import List, Iterable, Any



class Queue(QueueAdapterFactory):

    def __init__(self, **kwargs):
        super(Queue, self).__init__(**kwargs)

        self.__name = kwargs.get("name", None)
        if self.__name is None:
            raise Exception("The name of Queue object shouldn't be None object. "
                            "It's the key of each Queue object you create.")

        self.__qtype = kwargs.get("qtype", None)
        if self.__qtype is None:
            raise Exception("Queue type parameter shouldn't be None object. "
                            "It must to choice a type of Queue object with mapping strategy.")


    def __str__(self):
        return f"<Queue Object at {id(self)}>"


    def __repr__(self):
        return f"<Queue Object(name={self.__name}, qtype={self.__qtype}) ar {id(self)}>"


    def get_instance(self) -> OceanQueue:
        __queue = self.__qtype.value
        return __queue
        # queue_instance: BaseQueue = _ModuleFactory.get_queue_adapter(mode=self._mode)
        # return queue_instance.get_queue(qtype=self.__qtype)


    def globalize_instance(self, obj) -> None:
        Globalize.queue(name=self.__name, queue=obj)



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

