from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION
from multirunnable.concurrent.strategy import ConcurrentStrategy, ThreadStrategy, ThreadPoolStrategy
from multirunnable.concurrent.result import ConcurrentResult, ThreadPoolResult

from ..framework.strategy import GeneralRunningTestSpec, PoolRunningTestSpec
from ..test_config import (
    Worker_Size, Worker_Pool_Size, Task_Size,
    Running_Diff_Time,
    Test_Function_Sleep_Time,
    Test_Function_Args, Test_Function_Multiple_Args, Test_Function_Kwargs)

from typing import List, Tuple, Dict
import threading
import datetime
import pytest
import time
import os


Thread_Size: int = Worker_Size
Pool_Size: int = Worker_Pool_Size
Task_Size: int = Task_Size

Running_Diff_Time: int = Running_Diff_Time

_Thread_Lock = threading.Lock()

Running_Parent_PID: str = None
Running_Count = 0
Running_Thread_IDs: List = []
Running_PPIDs: List = []
Running_Current_Threads: List = []
Running_Finish_Timestamp: List = []

Pool_Running_Count = 0


def reset_running_flag() -> None:
    global Running_Count
    Running_Count = 0


def reset_pool_running_value() -> None:
    global Pool_Running_Count
    Pool_Running_Count = 0


def reset_running_timer() -> None:
    global Running_Thread_IDs, Running_PPIDs, Running_Current_Threads, Running_Finish_Timestamp
    Running_Thread_IDs[:] = []
    Running_PPIDs[:] = []
    Running_Current_Threads[:] = []
    Running_Finish_Timestamp[:] = []


Test_Function_Sleep_Time = Test_Function_Sleep_Time
Test_Function_Args: Tuple = Test_Function_Args
Test_Function_Kwargs: Dict = Test_Function_Kwargs
Test_Function_Multiple_Args = Test_Function_Multiple_Args


def target_fun(*args, **kwargs) -> str:
    global Running_Count

    with _Thread_Lock:
        Running_Count += 1

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        _ident = threading.get_ident()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_Thread_IDs.append(_ident)
        Running_PPIDs.append(_ppid)
        Running_Current_Threads.append(str(threading.current_thread()))
        Running_Finish_Timestamp.append(_time)

    time.sleep(Test_Function_Sleep_Time)
    return f"result_{_ident}"


def target_error_fun(*args, **kwargs) -> str:
    raise Exception("Testing result raising an exception.")


def pool_target_fun(*args, **kwargs) -> str:
    global Pool_Running_Count

    with _Thread_Lock:
        Pool_Running_Count += 1

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        _ident = threading.get_ident()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_Thread_IDs.append(_ident)
        Running_PPIDs.append(_ppid)
        Running_Current_Threads.append(str(threading.current_thread()))
        Running_Finish_Timestamp.append(_time)

    time.sleep(Test_Function_Sleep_Time)
    return f"result_{_ident}"


def map_target_fun(*args, **kwargs):
    """
    Description:
        Test for 'map', 'starmap' methods.
    :param args:
    :param kwargs:
    :return:
    """
    global Pool_Running_Count

    with _Thread_Lock:
        Pool_Running_Count += 1

        if args:
            assert set(args) <= set(Test_Function_Args), f"The argument *args* should be one of element of the input outside."
            if len(args) > 1:
                assert args == Test_Function_Args, f"The argument *args* should be same as the global variable 'Test_Function_Args'."
        if kwargs:
            assert kwargs is None or kwargs == {}, f"The argument *kwargs* should be empty or None value."

        _pid = os.getpid()
        _ppid = os.getppid()
        _ident = threading.get_ident()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_Thread_IDs.append(_ident)
        Running_PPIDs.append(_ppid)
        Running_Current_Threads.append(str(threading.current_thread()))
        Running_Finish_Timestamp.append(_time)

    time.sleep(Test_Function_Sleep_Time)
    return f"result_{_ident}"


class TargetCls:

    def method(self, *args, **kwargs) -> None:
        target_fun(*args, **kwargs)


    @classmethod
    def classmethod_fun(cls, *args, **kwargs) -> None:
        target_fun(*args, **kwargs)


    @staticmethod
    def staticmethod_fun(*args, **kwargs) -> None:
        target_fun(*args, **kwargs)


class TargetPoolCls:

    def method(self, *args, **kwargs) -> None:
        pool_target_fun(*args, **kwargs)


    @classmethod
    def classmethod_fun(cls, *args, **kwargs) -> None:
        pool_target_fun(*args, **kwargs)


    @staticmethod
    def staticmethod_fun(*args, **kwargs) -> None:
        pool_target_fun(*args, **kwargs)


class TargetPoolMapCls:

    def method(self, *args, **kwargs) -> None:
        map_target_fun(*args, **kwargs)


    @classmethod
    def classmethod_fun(cls, *args, **kwargs) -> None:
        map_target_fun(*args, **kwargs)


    @staticmethod
    def staticmethod_fun(*args, **kwargs) -> None:
        map_target_fun(*args, **kwargs)


@pytest.fixture(scope="class")
def strategy():
    return ThreadStrategy(executors=Thread_Size)


@pytest.fixture(scope="class")
def pool_strategy():
    _strategy = ThreadPoolStrategy(pool_size=Pool_Size, tasks_size=Task_Size)
    _strategy.initialization()
    return _strategy


_Generate_Worker_Error_Msg = \
    f"The instances which be created by method 'generate_worker' should be an instance of 'threading.Thread'."


class TestThread(GeneralRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_initialization(self, strategy: ThreadStrategy):
        pass


    def test_start_new_worker_with_function_with_no_argument(self, strategy: ThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_function_with_args(self, strategy: ThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun,
            args=Test_Function_Args)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_function_with_kwargs(self, strategy: ThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun,
            kwargs=Test_Function_Kwargs)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_no_argument(self, strategy: ThreadStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=_tc.method)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_args(self, strategy: ThreadStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=_tc.method,
            args=Test_Function_Args)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_kwargs(self, strategy: ThreadStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_no_argument(self, strategy: ThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.classmethod_fun)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_args(self, strategy: ThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_kwargs(self, strategy: ThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_no_argument(self, strategy: ThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.staticmethod_fun)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_args(self, strategy: ThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args)

        TestThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_kwargs(self, strategy: ThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs)

        TestThread._chk_record()
        strategy.reset_result()


    def test_generate_worker_with_function_with_no_argument(self, strategy: ThreadStrategy):
        # Test for no any parameters
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_function_with_args(self, strategy: ThreadStrategy):
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_function_with_kwargs(self, strategy: ThreadStrategy):
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_no_argument(self, strategy: ThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for no any parameters
        _tc = TargetCls()
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=_tc.method,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_args(self, strategy: ThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '*args'
        _tc = TargetCls()
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=_tc.method,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_kwargs(self, strategy: ThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '**kwargs'
        _tc = TargetCls()
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_no_argument(self, strategy: ThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for no any parameters
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_args(self, strategy: ThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_kwargs(self, strategy: ThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_no_argument(self, strategy: ThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for no any parameters
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_args(self, strategy: ThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_kwargs(self, strategy: ThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def _chk_worker_instance_type(self, worker) -> bool:
        return isinstance(worker, threading.Thread)


    def test_activate_workers_with_function_with_no_arguments(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_function_with_args(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_function_with_kwargs(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_bounded_function_with_no_arguments(self, strategy: ThreadStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=_tc.method)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_bounded_function_with_args(self, strategy: ThreadStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=_tc.method,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_bounded_function_with_kwargs(self, strategy: ThreadStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_classmethod_function_with_no_arguments(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.classmethod_fun)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_classmethod_function_with_args(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_classmethod_function_with_kwargs(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_staticmethod_function_with_no_arguments(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.staticmethod_fun)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_staticmethod_function_with_args(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_activate_workers_with_staticmethod_function_with_kwargs(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestThread._chk_record()


    def test_get_success_result(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_fun,
            args=Test_Function_Args)

        _result = strategy.get_result()
        assert _result is not None and _result != [], f"The running result should not be empty."
        assert type(_result) is list, f"The result should be a list type object."
        for _r in _result:
            assert isinstance(_r, ConcurrentResult) is True, f"The element of result should be instance of object 'ConcurrentResult'."
            assert _r.pid, f"The PID should exists in list we record."
            assert _r.worker_name, f"It should have thread name."
            assert _r.worker_ident, f"It should have thread identity."
            if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION >= 8:
                assert _r.native_id, f"It should have thread native ID."
            assert _r.data == f"result_{_r.worker_ident}", f"Its data should be same as we expect 'result_{_r.pid}'."
            assert _r.state == "successful", f"Its state should be 'successful'."
            assert _r.exception is None, f"It should have nothing exception."


    def test_get_failure_result(self, strategy: ThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Thread_Size,
            target_fun=target_error_fun)

        _result = strategy.get_result()
        assert _result is not None and _result != [], f""
        assert type(_result) is list, f""
        for _r in _result:
            assert isinstance(_r, ConcurrentResult) is True, f""
            assert _r.pid, f"It should have PID."
            assert _r.worker_name, f"It should have thread name."
            assert _r.worker_ident, f"It should have thread identity."
            if PYTHON_MAJOR_VERSION == 3 and PYTHON_MINOR_VERSION >= 8:
                assert _r.native_id, f"It should have thread native ID."
            assert _r.data is None, f"Its data should be None."
            assert _r.state == "fail", f"Its state should be 'fail'."
            assert isinstance(_r.exception, Exception) and "Testing result raising an exception" in str(_r.exception), f"It should have an exception and error message is 'Testing result raising an exception'."


    def _initial(self):
        # Test for parameters with '**kwargs'
        reset_running_flag()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_record():
        GeneralRunningTestSpec._chk_process_record(
            running_cnt=Running_Count,
            worker_size=Thread_Size,
            running_wokrer_ids=Running_Thread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_close(self, strategy: ThreadStrategy):
        # Test for no any parameters
        # process_strategy.close(self.__Processes)
        # _active_children_list = mp.active_children()
        # print(len(_active_children_list) == 0)
        # # assert len(_active_children_list) == 0, f"Processes should be closed finely."
        #
        # # Test for parameters with '*args'
        # process_strategy.close(self.__Processes_With_Args)
        # _active_children_list = mp.active_children()
        # print(len(_active_children_list) == 0)
        # # assert len(_active_children_list) == 0, f"Processes should be closed finely."
        #
        # # Test for parameters with '**kwargs'
        # process_strategy.close(self.__Processes_With_Kwargs)
        # _active_children_list = mp.active_children()
        # print(len(_active_children_list) == 0)
        # assert len(_active_children_list) == 0, f"Processes should be closed finely."
        pass



class TestThreadPool(PoolRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_initialization(self, pool_strategy: ThreadPoolStrategy):
        pass


    def test_apply_with_function_with_no_arguments(self, pool_strategy: ThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=pool_target_fun)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_function_with_args(self, pool_strategy: ThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=pool_target_fun, args=Test_Function_Args)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_function_with_kwargs(self, pool_strategy: ThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=pool_target_fun, kwargs=Test_Function_Kwargs)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_no_arguments(self, pool_strategy: ThreadPoolStrategy):
        _tc = TargetPoolCls()
        self._apply(strategy=pool_strategy, target_fun=_tc.method)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_args(self, pool_strategy: ThreadPoolStrategy):
        _tc = TargetPoolCls()
        self._apply(strategy=pool_strategy, target_fun=_tc.method, args=Test_Function_Args)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_kwargs(self, pool_strategy: ThreadPoolStrategy):
        _tc = TargetPoolCls()
        self._apply(strategy=pool_strategy, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_no_arguments(self, pool_strategy: ThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_args(self, pool_strategy: ThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun, args=Test_Function_Args)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_kwargs(self, pool_strategy: ThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_no_arguments(self, pool_strategy: ThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_args(self, pool_strategy: ThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, args=Test_Function_Args)

        TestThreadPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_kwargs(self, pool_strategy: ThreadPoolStrategy):
        self._apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestThreadPool._chk_blocking_record()


    def test_async_apply_with_function_with_no_arguments(self, pool_strategy: ThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=pool_target_fun)

        TestThreadPool._chk_record()


    def test_async_apply_with_function_with_args(self, pool_strategy: ThreadPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=pool_strategy, target_fun=pool_target_fun, args=Test_Function_Args)

        TestThreadPool._chk_record()


    def test_async_apply_with_function_with_kwargs(self, pool_strategy: ThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=pool_strategy, target_fun=pool_target_fun, kwargs=Test_Function_Kwargs)

        TestThreadPool._chk_record()


    def test_async_apply_with_bounded_function_with_no_arguments(self, pool_strategy: ThreadPoolStrategy):
        _tc = TargetPoolCls()
        self._async_apply(strategy=pool_strategy, target_fun=_tc.method)

        TestThreadPool._chk_record()


    def test_async_apply_with_bounded_function_with_args(self, pool_strategy: ThreadPoolStrategy):
        # Test for parameters with '*args'
        _tc = TargetPoolCls()
        self._async_apply(strategy=pool_strategy, target_fun=_tc.method, args=Test_Function_Args)

        TestThreadPool._chk_record()


    def test_async_apply_with_bounded_function_with_kwargs(self, pool_strategy: ThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        _tc = TargetPoolCls()
        self._async_apply(strategy=pool_strategy, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestThreadPool._chk_record()


    def test_async_apply_with_classmethod_function_with_no_arguments(self, pool_strategy: ThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun)

        TestThreadPool._chk_record()


    def test_async_apply_with_classmethod_function_with_args(self, pool_strategy: ThreadPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun, args=Test_Function_Args)

        TestThreadPool._chk_record()


    def test_async_apply_with_classmethod_function_with_kwargs(self, pool_strategy: ThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestThreadPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_no_arguments(self, pool_strategy: ThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun)

        TestThreadPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_args(self, pool_strategy: ThreadPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, args=Test_Function_Args)

        TestThreadPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_kwargs(self, pool_strategy: ThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestThreadPool._chk_record()


    def test_map_with_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._map(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map(function=target_fun, args_iter=Test_Function_Args)


    def test_map_with_bounded_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._map(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_map_with_classmethod_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._map(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_map_with_staticmethod_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._map(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_async_map_with_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_with_bounded_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._async_map(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_async_map_with_classmethod_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_async_map_with_staticmethod_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_map_by_args_with_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._map_by_args(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_map_by_args_with_bounded_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestThreadPool._chk_map_record()


    def test_map_by_args_with_classmethod_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestThreadPool._chk_map_record()


    def test_map_by_args_with_staticmethod_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        TestThreadPool._chk_map_record()


    def test_async_map_by_args_with_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._async_map_by_args(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_by_args_with_bounded_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._async_map_by_args(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestThreadPool._chk_map_record()


    def test_async_map_by_args_with_classmethod_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestThreadPool._chk_map_record()


    def test_async_map_by_args_with_staticmethod_function(self, pool_strategy: ThreadPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestThreadPool._chk_map_record()


    def test_imap_with_function(self, pool_strategy: ThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_imap_with_bounded_function(self, pool_strategy: ThreadPoolStrategy):
        _tc = TargetPoolMapCls()
        self._imap(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_imap_with_classmethod_function(self, pool_strategy: ThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_imap_with_staticmethod_function(self, pool_strategy: ThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_imap_unordered_with_function(self, pool_strategy: ThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_imap_unordered_with_bounded_function(self, pool_strategy: ThreadPoolStrategy):
        _tc = TargetPoolMapCls()
        self._imap_unordered(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_imap_unordered_with_classmethod_function(self, pool_strategy: ThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_imap_unordered_with_staticmethod_function(self, pool_strategy: ThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestThreadPool._chk_map_record()


    def test_get_success_result_with_async_apply(self, pool_strategy: ThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=pool_target_fun)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    @pytest.mark.skip(reason="Not finish yet. Consider about whether the necessary about catch the exception or not.")
    def test_get_failure_result_with_async_apply(self, pool_strategy: ThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, target_fun=target_error_fun)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_failure_result(results=_results)


    def test_get_success_result_with_map(self, pool_strategy: ThreadPoolStrategy):
        self._map(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_async_map(self, pool_strategy: ThreadPoolStrategy):
        self._async_map(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_map_by_args(self, pool_strategy: ThreadPoolStrategy):
        self._map_by_args(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_async_map_by_args(self, pool_strategy: ThreadPoolStrategy):
        self._async_map_by_args(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap(self, pool_strategy: ThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap_unordered(self, pool_strategy: ThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def _initial(self):
        # Test for parameters with '**kwargs'
        reset_pool_running_value()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_blocking_record():
        PoolRunningTestSpec._chk_process_record_blocking(
            pool_running_cnt=Pool_Running_Count,
            worker_size=Thread_Size,
            running_worker_ids=Running_Thread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp,
            de_duplicate=False
        )


    @staticmethod
    def _chk_record():
        PoolRunningTestSpec._chk_process_record(
            pool_running_cnt=Pool_Running_Count,
            worker_size=Thread_Size,
            running_worker_ids=Running_Thread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    @staticmethod
    def _chk_map_record():
        PoolRunningTestSpec._chk_process_record_map(
            pool_running_cnt=Pool_Running_Count,
            function_args=Test_Function_Args,
            running_worker_ids=Running_Thread_IDs,
            running_current_workers=Running_Current_Threads,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    def test_close(self, pool_strategy: ThreadPoolStrategy):
        """
        ValueError: Pool not running
        :param pool_strategy:
        :return:
        """
        try:
            pool_strategy.close()
        except Exception as e:
            assert e is not None, f"It should work finely without any issue."
        else:
            assert True, f"It work finely."


    def test_terminal(self, pool_strategy: ThreadPoolStrategy):
        try:
            pool_strategy.terminal()
        except Exception as e:
            assert e is not None, f"It should work finely without any issue."
        else:
            assert True, f"It work finely."

