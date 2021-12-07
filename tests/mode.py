"""
A unittest for multirunnable.mode module
"""

from multirunnable.mode import RunningMode, FeatureMode
from abc import ABCMeta, abstractmethod



class RunningModeTestCases(metaclass=ABCMeta):

    @abstractmethod
    def test_parallel_mode(self):
        pass


    @abstractmethod
    def test_concurrent_mode(self):
        pass


    @abstractmethod
    def test_greenlet_mode(self):
        pass


    @abstractmethod
    def test_asynchronous_mode(self):
        pass



class FeatureModeTestCases(metaclass=ABCMeta):

    @abstractmethod
    def test_parallel_mode(self):
        pass


    @abstractmethod
    def test_concurrent_mode(self):
        pass


    @abstractmethod
    def test_greenlet_mode(self):
        pass


    @abstractmethod
    def test_asynchronous_mode(self):
        pass



class FinalProveResult:

    @staticmethod
    def running_mode_key():
        return "strategy_module", "class_key", "executor_strategy", "pool_strategy"


    @staticmethod
    def feature_mode_key():
        return "module", "queue", "lock", "communication"



class TestRunningMode(RunningModeTestCases):

    def test_parallel_mode(self):
        self.__check_mechanism(mode=RunningMode.Parallel)


    def test_concurrent_mode(self):
        self.__check_mechanism(mode=RunningMode.Concurrent)


    def test_greenlet_mode(self):
        self.__check_mechanism(mode=RunningMode.GreenThread)


    def test_asynchronous_mode(self):
        self.__check_mechanism(mode=RunningMode.Asynchronous)


    def __check_mechanism(self, mode: RunningMode):
        __mode_cls_info = mode.value
        self.__check_data_type(mode_cls_info=__mode_cls_info)
        self.__check_keys(mode_cls_info=__mode_cls_info)
        self.__check_values(mode_cls_info=__mode_cls_info)


    def __check_data_type(self, mode_cls_info: dict):
        assert type(mode_cls_info) is dict


    def __check_keys(self, mode_cls_info: dict):
        assert tuple(mode_cls_info.keys()) == FinalProveResult.running_mode_key()


    def __check_values(self, mode_cls_info: dict):
        for key, value in mode_cls_info.items():
            assert value is not None and value != ""



class TestFeatureMode(FeatureModeTestCases):

    def test_parallel_mode(self):
        self.__check_mechanism(mode=FeatureMode.Parallel)


    def test_concurrent_mode(self):
        self.__check_mechanism(mode=FeatureMode.Concurrent)


    def test_greenlet_mode(self):
        self.__check_mechanism(mode=FeatureMode.GreenThread)


    def test_asynchronous_mode(self):
        self.__check_mechanism(mode=FeatureMode.Asynchronous)


    def __check_mechanism(self, mode: FeatureMode):
        __mode_cls_info = mode.value
        self.__check_data_type(mode_cls_info=__mode_cls_info)
        self.__check_keys(mode_cls_info=__mode_cls_info)
        self.__check_values(mode_cls_info=__mode_cls_info)


    def __check_data_type(self, mode_cls_info: dict):
        assert type(mode_cls_info) is dict


    def __check_keys(self, mode_cls_info: dict):
        assert tuple(mode_cls_info.keys()) == FinalProveResult.feature_mode_key()


    def __check_values(self, mode_cls_info: dict):
        for key, value in mode_cls_info.items():
            assert value is not None and value != ""

