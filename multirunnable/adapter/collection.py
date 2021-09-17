from multirunnable.framework.task import BaseQueueTask as _BaseQueueTask
from multirunnable.framework.adapter.collection import BaseList as _BaseList, BaseIterator as _BaseIterator
from multirunnable.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory

from typing import List



class FeatureList(_BaseList):

    _List: List[_BaseFeatureAdapterFactory] = []

    def index(self, index: int) -> _BaseFeatureAdapterFactory:
        return self._List[index]


    def append(self, feature: _BaseFeatureAdapterFactory) -> None:
        self._List.append(feature)


    def insert(self, index: int, value: _BaseFeatureAdapterFactory) -> None:
        self._List.insert(index, value)


    def extend(self, __iterator) -> None:
        self._List.extend(__iterator)


    def pop(self, index: int) -> None:
        self._List.pop(index)


    def remove(self, value: _BaseFeatureAdapterFactory) -> None:
        self._List.remove(value)


    def clear(self) -> None:
        self._List.clear()


    def iterator(self) -> _BaseIterator:
        return FeatureIterator(factory_list=self)



class QueueTaskList(_BaseList):

    _List: List[_BaseQueueTask] = []

    def index(self, index: int) -> _BaseQueueTask:
        return self._List[index]


    def append(self, feature: _BaseQueueTask) -> None:
        self._List.append(feature)


    def insert(self, index: int, value: _BaseQueueTask) -> None:
        self._List.insert(index, value)


    def extend(self, __iterator) -> None:
        self._List.extend(__iterator)


    def pop(self, index: int) -> None:
        self._List.pop(index)


    def remove(self, value: _BaseQueueTask) -> None:
        self._List.remove(value)


    def clear(self) -> None:
        self._List.clear()


    def iterator(self) -> _BaseIterator:
        return QueueIterator(factory_list=self)



class QueueIterator(_BaseIterator):

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


    def next(self) -> _BaseQueueTask:
        __feature = self.__Queue_Task_List.index(self.__index)
        self.__index += 1
        return __feature



class FeatureIterator(_BaseIterator):

    __Features_List = None

    def __init__(self, factory_list: _BaseList):
        super().__init__(factory_list=factory_list)
        self.__Features_List = factory_list
        self.__index = 0



    def has_next(self) -> bool:
        if self.__index < len(self.__Features_List):
            return True
        else:
            return False


    def next(self) -> _BaseFeatureAdapterFactory:
        __feature = self.__Features_List.index(self.__index)
        self.__index += 1
        return __feature

