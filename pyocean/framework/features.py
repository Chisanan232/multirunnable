from pyocean.framework.exceptions import ParameterCannotBeEmpty

from abc import ABCMeta, abstractmethod
from enum import Enum



class BaseQueueType(Enum):

    pass



class BaseAPI(metaclass=ABCMeta):

    @abstractmethod
    def lock(self):
        """
        Description:
            Get Lock object.
        :return:
        """
        pass


    @abstractmethod
    def event(self, **kwargs):
        """
        Description:
            Get Event object.
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def condition(self, **kwargs):
        """
        Description:
            Get Condition object.
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def semaphore(self, value: int):
        """
        Description:
            Get Semaphore object.
        :param value:
        :return:
        """
        pass


    @abstractmethod
    def bounded_semaphore(self, value: int):
        """
        Description:
            Get Bounded Semaphore object.
        :param value:
        :return:
        """
        pass


    @abstractmethod
    def queue(self, qtype: BaseQueueType):
        """
        Description:
            Get Queue object.
        :param qtype:
        :return:
        """
        pass



class BaseGlobalizeAPI(metaclass=ABCMeta):

    """
    Description:
        Globalize target object so that it could run, visible and be used between each different threads or processes, etc.
    """

    @staticmethod
    @abstractmethod
    def lock(lock) -> None:
        """
        Description:
            Globalize Lock object.
        :param lock:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def rlock(rlock) -> None:
        """
        Description:
            Globalize RLock object.
        :param rlock:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def event(event) -> None:
        """
        Description:
            Globalize Event object.
        :param event:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def condition(condition) -> None:
        """
        Description:
            Globalize Condition object.
        :param condition:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def semaphore(smp) -> None:
        """
        Description:
            Globalize Semaphore object.
        :param smp:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def bounded_semaphore(bsmp) -> None:
        """
        Description:
            Globalize Bounded Semaphore object.
        :param bsmp:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def queue(queue) -> None:
        """
        Description:
            Globalize Queue object.
        :param queue:
        :return:
        """
        pass



class FeatureUtils:

    @staticmethod
    def chk_obj(param: str, **kwargs):
        """
        Description:
            Ensure that the value of target parameter is not None.
        :param param:
        :param kwargs:
        :return:
        """

        __obj = kwargs.get(param, None)
        if __obj is None:
            raise ParameterCannotBeEmpty(param=param)
        return __obj
