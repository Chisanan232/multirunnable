""" Test for the module '__init__' of package MultiRunnable """

from typing import List, Callable
import multiprocessing as mp
import multirunnable as mr
import pytest
import time
import sys

from ..test_config import Worker_Size, Running_Diff_Time, Test_Function_Sleep_Time
from .framework.strategy import GeneralRunningTestSpec


Process_Size: int = Worker_Size

Running_Diff_Time: int = Running_Diff_Time

_Manager = mp.Manager()
_Process_Lock = mp.Lock()
_Thread_Lock = None

Running_Process_Count = _Manager.Value("i", 0)
Running_Process_Finish_Timestamp: List = _Manager.list()

Running_Thread_Count = 0
Running_Thread_Finish_Timestamp: List = []

Pool_Running_Count = mp.Value("i", 0)

Sleep_Function: Callable = None


def reset_process_running_flag() -> None:
    global Running_Process_Count
    Running_Process_Count = _Manager.Value("i", 0)


def reset_thread_running_flag() -> None:
    global Running_Thread_Count
    Running_Thread_Count = 0


def reset_process_running_timer() -> None:
    global Running_Process_Finish_Timestamp
    Running_Process_Finish_Timestamp[:] = []


def reset_thread_running_timer() -> None:
    global Running_Thread_Finish_Timestamp
    Running_Thread_Finish_Timestamp[:] = []


def process_target_function_implement() -> str:
    global Running_Process_Count

    with _Process_Lock:
        Running_Process_Count.value += 1
        _time = int(time.time())
        Running_Process_Finish_Timestamp.append(_time)

    time.sleep(Test_Function_Sleep_Time)
    return "test_result"


def thread_target_function_implement() -> str:
    global Running_Thread_Count

    with _Thread_Lock:
        Running_Thread_Count += 1
        _time = int(time.time())
        Running_Thread_Finish_Timestamp.append(_time)

    Sleep_Function(Test_Function_Sleep_Time)
    return "test_result"


@mr.multi_processes(processes=Process_Size)
def _target_with_parallel():
    process_target_function_implement()


@mr.multi_threads(threads=Process_Size)
def _target_with_concurrent():
    thread_target_function_implement()


@mr.multi_green_threads(gthreads=Process_Size)
def _target_with_green_threads():
    thread_target_function_implement()


@mr.asynchronize
def _target_with_asynchronous():
    thread_target_function_implement()


@mr.multi_executors(mode=mr.RunningMode.Parallel, executors=Process_Size)
def _target_with_parallel_mode():
    process_target_function_implement()


@mr.multi_executors(mode=mr.RunningMode.Concurrent, executors=Process_Size)
def _target_with_concurrent_mode():
    thread_target_function_implement()


@mr.multi_executors(mode=mr.RunningMode.Concurrent, executors=Process_Size)
def _target_with_green_threads_mode():
    thread_target_function_implement()



class TestPackageInit:

    def test_python_version(self):
        _python_version = sys.version_info
        _py_major_ver = _python_version.major
        _py_minor_ver = _python_version.minor

        assert mr.PYTHON_MAJOR_VERSION == int(_py_major_ver), ""
        assert mr.PYTHON_MINOR_VERSION == int(_py_minor_ver), ""
        assert mr.PYTHON_VERSION == f"{_py_major_ver}.{_py_minor_ver}", ""


    def test_run_parallel_with_decorator(self):
        reset_process_running_flag()
        reset_process_running_timer()

        _target_with_parallel()
        TestPackageInit._chk_process_result()


    def test_run_concurrent_with_decorator(self):
        reset_thread_running_flag()
        reset_thread_running_timer()

        import threading
        global _Thread_Lock, Sleep_Function
        _Thread_Lock = threading.Lock()
        # Sleep_Function = time.sleep
        Sleep_Function = mr.sleep

        _target_with_concurrent()
        TestPackageInit._chk_thread_result()


    def test_run_coroutine_with_green_thread_with_decorator(self):
        reset_thread_running_flag()
        reset_thread_running_timer()

        from gevent.threading import Lock
        global _Thread_Lock, Sleep_Function
        _Thread_Lock = Lock()
        # Sleep_Function = gevent.sleep
        Sleep_Function = mr.sleep

        _target_with_green_threads()
        TestPackageInit._chk_thread_result()


    @pytest.mark.skip(reason="Not implementation ...")
    def test_run_coroutine_with_asynchronous_with_decorator(self):
        reset_thread_running_flag()
        reset_thread_running_timer()

        import asyncio
        global _Thread_Lock, Sleep_Function
        _Thread_Lock = asyncio.Lock()
        # Sleep_Function = asyncio.sleep
        Sleep_Function = mr.async_sleep

        _target_with_asynchronous()
        TestPackageInit._chk_thread_result()


    def test_run_parallel_by_running_mode_with_decorator(self):
        reset_process_running_flag()
        reset_process_running_timer()

        _target_with_parallel_mode()
        TestPackageInit._chk_process_result()


    def test_run_concurrent_by_running_mode_with_decorator(self):
        reset_thread_running_flag()
        reset_thread_running_timer()

        import threading
        global _Thread_Lock, Sleep_Function
        _Thread_Lock = threading.Lock()
        # Sleep_Function = time.sleep
        Sleep_Function = mr.sleep

        _target_with_concurrent_mode()
        TestPackageInit._chk_thread_result()


    def test_run_coroutine_with_green_thread_by_running_mode_with_decorator(self):
        reset_thread_running_flag()
        reset_thread_running_timer()

        from gevent.threading import Lock
        global _Thread_Lock, Sleep_Function
        _Thread_Lock = Lock()
        # Sleep_Function = gevent.sleep
        Sleep_Function = mr.sleep

        _target_with_green_threads_mode()
        TestPackageInit._chk_thread_result()


    @staticmethod
    def _chk_process_result():
        GeneralRunningTestSpec._chk_running_cnt(running_cnt=Running_Process_Count.value, worker_size=Process_Size)
        GeneralRunningTestSpec._chk_done_timestamp(timestamp_list=Running_Process_Finish_Timestamp)


    @staticmethod
    def _chk_thread_result():
        GeneralRunningTestSpec._chk_running_cnt(running_cnt=Running_Thread_Count, worker_size=Process_Size)
        GeneralRunningTestSpec._chk_done_timestamp(timestamp_list=Running_Thread_Finish_Timestamp)


