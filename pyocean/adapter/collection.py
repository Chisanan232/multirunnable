from pyocean.framework.collection import BaseList, BaseIterator
from pyocean.framework.features import BaseFeatureAdapterFactory
from pyocean.framework.task import BaseQueueTask

from typing import List



class FeatureList(BaseList):

    _List: List[BaseFeatureAdapterFactory] = []

    def index(self, index: int) -> BaseFeatureAdapterFactory:
        return self._List[index]


    def append(self, feature: BaseFeatureAdapterFactory) -> None:
        self._List.append(feature)


    def insert(self, index: int, value: BaseFeatureAdapterFactory) -> None:
        self._List.insert(index, value)


    def extend(self, __iterator) -> None:
        self._List.extend(__iterator)


    def pop(self, index: int) -> None:
        self._List.pop(index)


    def remove(self, value: BaseFeatureAdapterFactory) -> None:
        self._List.remove(value)


    def clear(self) -> None:
        self._List.clear()


    def iterator(self) -> BaseIterator:
        return FeatureIterator(factory_list=self)



class QueueTaskList(BaseList):

    _List: List[BaseQueueTask] = []

    def index(self, index: int) -> BaseQueueTask:
        return self._List[index]


    def append(self, feature: BaseQueueTask) -> None:
        self._List.append(feature)


    def insert(self, index: int, value: BaseQueueTask) -> None:
        self._List.insert(index, value)


    def extend(self, __iterator) -> None:
        self._List.extend(__iterator)


    def pop(self, index: int) -> None:
        self._List.pop(index)


    def remove(self, value: BaseQueueTask) -> None:
        self._List.remove(value)


    def clear(self) -> None:
        self._List.clear()


    def iterator(self) -> BaseIterator:
        return QueueIterator(factory_list=self)



class QueueIterator(BaseIterator):

    __Queue_Task_List = None

    def __init__(self, factory_list: QueueTaskList):
        super().__init__(factory_list=factory_list)
        self.__Queue_Task_List = factory_list
        self.__index = 0



    def has_next(self) -> bool:
        if self.__index < len(self.__Queue_Task_List):
            return True
        else:
            return False


    def next(self) -> BaseQueueTask:
        __feature = self.__Queue_Task_List.index(self.__index)
        self.__index += 1
        return __feature



class FeatureIterator(BaseIterator):

    __Features_List = None

    def __init__(self, factory_list: BaseList):
        super().__init__(factory_list=factory_list)
        self.__Features_List = factory_list
        self.__index = 0



    def has_next(self) -> bool:
        if self.__index < len(self.__Features_List):
            return True
        else:
            return False


    def next(self) -> BaseFeatureAdapterFactory:
        __feature = self.__Features_List.index(self.__index)
        self.__index += 1
        return __feature

