from enum import Enum
from abc import ABCMeta, abstractmethod

from ...types import MRQueue as _MRQueue



class BaseQueueType(Enum):

    pass



class BaseQueue(metaclass=ABCMeta):

    @abstractmethod
    def get_queue(self, qtype: BaseQueueType) -> _MRQueue:
        pass



class BaseGlobalizeAPI(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def queue(name, queue) -> None:
        """
        Description:
            Globalize Queue object.
        :param name:
        :param queue:
        :return:
        """
        pass

