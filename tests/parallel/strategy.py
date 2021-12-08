from multirunnable.parallel.strategy import ParallelStrategy, ProcessStrategy, ProcessPoolStrategy

from ..framework.strategy import GeneralRunningTestSpec, PoolRunningTestSpec
import pytest
import time
import os


Process_Size = 10
Pool_Size = 10
Task_Size = 10

Running_Count = 0
Running_Timer_List = []


def reset_running_flag() -> None:
    global Running_Count
    Running_Count = 0


def target_fun() -> None:
    global Running_Count
    Running_Count += 1


class TargetCls:

    def method(self) -> None:
        global Running_Count
        Running_Count += 1


    @classmethod
    def classmethod_fun(cls) -> None:
        global Running_Count
        Running_Count += 1


    @staticmethod
    def staticmethod_fun() -> None:
        global Running_Count
        Running_Count += 1


@pytest.fixture(scope="class")
def process_strategy():
    return ProcessStrategy(executors=Process_Size)


@pytest.fixture(scope="class")
def process_pool_strategy():
    return ProcessPoolStrategy(pool_size=Pool_Size, tasks_size=Task_Size)


class TestProcess(GeneralRunningTestSpec):

    def test_initialization(self, process_strategy):
        pass


    def test_start_new_worker(self, process_strategy):
        pass


    def test_generate_worker(self, process_strategy):
        pass


    def test_activate_workers(self, process_strategy):
        pass


    def test_close(self, process_strategy):
        pass


    def test_terminal(self, process_strategy):
        pass


    def test_kill(self, process_strategy):
        pass


    def test_get_result(self, process_strategy):
        pass



class TestProcessPool(PoolRunningTestSpec):

    def test_initialization(self, process_pool_strategy):
        pass


    def test_apply(self, process_pool_strategy):
        pass


    def test_async_apply(self, process_pool_strategy):
        pass


    def test_map(self, process_pool_strategy):
        pass


    def test_async_map(self, process_pool_strategy):
        pass


    def test_map_by_args(self, process_pool_strategy):
        pass


    def test_async_map_by_args(self, process_pool_strategy):
        pass


    def test_imap(self, process_pool_strategy):
        pass


    def test_imap_unordered(self, process_pool_strategy):
        pass


    def test_close(self, process_pool_strategy):
        pass


    def test_terminal(self, process_pool_strategy):
        pass


    def test_get_result(self, process_pool_strategy):
        pass



