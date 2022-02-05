from abc import ABCMeta, abstractmethod



class BaseFeatureAdapterFactory(metaclass=ABCMeta):

    @abstractmethod
    def get_instance(self, **kwargs):
        pass


    @abstractmethod
    def globalize_instance(self, obj) -> None:
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

