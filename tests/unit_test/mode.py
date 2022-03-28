"""
A unittest for multirunnable.mode module
"""

from multirunnable.mode import ContextMode, RunningMode, FeatureMode

from typing import Union
from abc import ABCMeta, abstractmethod
import pytest



class ModeTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_mode(self, mode):
        pass


    def _check_mechanism(self, mode: Union[ContextMode, RunningMode, FeatureMode]):
        __mode_cls_info = mode.value
        ModeTestSpec.__check_data_type(mode_cls_info=__mode_cls_info)
        self.__check_keys(mode_cls_info=__mode_cls_info)
        ModeTestSpec.__check_values(mode_cls_info=__mode_cls_info)


    @staticmethod
    def __check_data_type(mode_cls_info: dict):
        assert type(mode_cls_info) is dict


    def __check_keys(self, mode_cls_info: dict):
        assert tuple(mode_cls_info.keys()) == self.mode_keys()


    def mode_keys(self):
        pass


    @staticmethod
    def __check_values(mode_cls_info: dict):
        for key, value in mode_cls_info.items():
            assert value is not None and value != ""



class FinalProveResult:

    @staticmethod
    def context_mode_key():
        return "module", "context"


    @staticmethod
    def running_mode_key():
        return "strategy_module", "class_key", "executor_strategy", "pool_strategy", "feature", "context"


    @staticmethod
    def feature_mode_key():
        return "module", "queue", "lock", "communication"



class TestContextMode(ModeTestSpec):

    @pytest.mark.parametrize("mode", [ContextMode.Parallel, ContextMode.Concurrent, ContextMode.GreenThread, ContextMode.Asynchronous])
    def test_mode(self, mode):
        self._check_mechanism(mode=mode)


    def mode_keys(self):
        return FinalProveResult.context_mode_key()



class TestRunningMode(ModeTestSpec):

    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_mode(self, mode):
        self._check_mechanism(mode=mode)


    def mode_keys(self):
        return FinalProveResult.running_mode_key()



class TestFeatureMode(ModeTestSpec):

    @pytest.mark.parametrize("mode", [FeatureMode.Parallel, FeatureMode.Concurrent, FeatureMode.GreenThread, FeatureMode.Asynchronous])
    def test_mode(self, mode):
        self._check_mechanism(mode=mode)


    def mode_keys(self):
        return FinalProveResult.feature_mode_key()

