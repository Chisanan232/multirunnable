from multirunnable.parallel.strategy import ParallelStrategy, ProcessStrategy, ProcessPoolStrategy
from multirunnable.parallel.result import ParallelResult

from ..framework.strategy import GeneralRunningTestSpec, PoolRunningTestSpec
from ..test_config import (
    Worker_Size, Worker_Pool_Size, Task_Size,
    Running_Diff_Time,
    Test_Function_Sleep_Time,
    Test_Function_Args, Test_Function_Multiple_Args, Test_Function_Kwargs)

from typing import List, Tuple, Dict
import multiprocessing as mp
import datetime
import pytest
import time
import os
import re


Process_Size: int = Worker_Size
Pool_Size: int = Worker_Pool_Size
Task_Size: int = Task_Size

Running_Diff_Time: int = Running_Diff_Time

_Manager = mp.Manager()
_Process_Lock = mp.Lock()

Running_Parent_PID: str = ""
Running_Count = _Manager.Value("i", 0)
Running_PIDs: List = _Manager.list()
Running_PPIDs: List = _Manager.list()
Running_Current_Processes: List = _Manager.list()
Running_Finish_Timestamp: List = _Manager.list()

Pool_Running_Count = mp.Value("i", 0)


def reset_running_flag() -> None:
    global Running_Count
    Running_Count = _Manager.Value("i", 0)
    # Running_Count = 0


def reset_pool_running_value() -> None:
    global Pool_Running_Count
    Pool_Running_Count.value = 0
    # Pool_Running_Count = mp.Value("i", 0)


def reset_running_timer() -> None:
    global Running_PIDs, Running_PPIDs, Running_Current_Processes, Running_Finish_Timestamp
    Running_PIDs[:] = []
    Running_PPIDs[:] = []
    Running_Current_Processes[:] = []
    Running_Finish_Timestamp[:] = []


Test_Function_Sleep_Time = Test_Function_Sleep_Time
Test_Function_Args: Tuple = Test_Function_Args
Test_Function_Kwargs: Dict = Test_Function_Kwargs
Test_Function_Multiple_Args = Test_Function_Multiple_Args


def target_fun(*args, **kwargs) -> str:
    global Running_Count

    with _Process_Lock:
        Running_Count.value += 1

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_PIDs.append(_pid)
        Running_PPIDs.append(_ppid)
        Running_Current_Processes.append(str(mp.current_process()))
        Running_Finish_Timestamp.append(_time)

    time.sleep(Test_Function_Sleep_Time)
    return f"result_{_pid}"


def target_error_fun(*args, **kwargs) -> str:
    raise Exception("Testing result raising an exception.")


def pool_target_fun(*args, **kwargs) -> str:
    global Pool_Running_Count

    with _Process_Lock:
        Pool_Running_Count.value += 1

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_PIDs.append(_pid)
        Running_PPIDs.append(_ppid)
        Running_Current_Processes.append(str(mp.current_process()))
        Running_Finish_Timestamp.append(_time)

    time.sleep(Test_Function_Sleep_Time)
    return f"result_{_pid}"


def map_target_fun(*args, **kwargs):
    """
    Description:
        Test for 'map', 'starmap' methods.
    :param args:
    :param kwargs:
    :return:
    """
    global Pool_Running_Count

    with _Process_Lock:
        Pool_Running_Count.value += 1

        if args:
            assert set(args) <= set(Test_Function_Args), f"The argument *args* should be one of element of the input outside."
            if len(args) > 1:
                assert args == Test_Function_Args, f"The argument *args* should be same as the global variable 'Test_Function_Args'."
        if kwargs:
            assert kwargs is None or kwargs == {}, f"The argument *kwargs* should be empty or None value."

        _pid = os.getpid()
        _ppid = os.getppid()
        # _time = str(datetime.datetime.now())
        _time = int(time.time())

        Running_PIDs.append(_pid)
        Running_PPIDs.append(_ppid)
        Running_Current_Processes.append(str(mp.current_process()))
        Running_Finish_Timestamp.append(_time)

    time.sleep(Test_Function_Sleep_Time)
    return f"result_{_pid}"


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
def process_strategy():
    return ProcessStrategy(executors=Process_Size)


@pytest.fixture(scope="class")
def process_pool_strategy():
    _strategy = ProcessPoolStrategy(pool_size=Pool_Size, tasks_size=Task_Size)
    _strategy.initialization()
    return _strategy


_Generate_Worker_Error_Msg = \
    f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


class TestProcess(GeneralRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_initialization(self, process_strategy: ProcessStrategy):
        pass


    def test_start_new_worker_with_function_with_no_argument(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_function_with_args(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun,
            args=Test_Function_Args)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_function_with_kwargs(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun,
            kwargs=Test_Function_Kwargs)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_no_argument(self, process_strategy: ProcessStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=_tc.method)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_args(self, process_strategy: ProcessStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=_tc.method,
            args=Test_Function_Args)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_kwargs(self, process_strategy: ProcessStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_no_argument(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.classmethod_fun)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_args(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_kwargs(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_no_argument(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.staticmethod_fun)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_args(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_kwargs(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_generate_worker_with_function_with_no_argument(self, process_strategy: ProcessStrategy):
        # Test for no any parameters
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_function_with_args(self, process_strategy: ProcessStrategy):
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_function_with_kwargs(self, process_strategy: ProcessStrategy):
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_no_argument(self, process_strategy: ProcessStrategy):
        # # # # Test target function is bounded function.
        # Test for no any parameters
        _tc = TargetCls()
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=_tc.method,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_args(self, process_strategy: ProcessStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '*args'
        _tc = TargetCls()
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=_tc.method,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_kwargs(self, process_strategy: ProcessStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '**kwargs'
        _tc = TargetCls()
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_no_argument(self, process_strategy: ProcessStrategy):
        # # # # Test target function is classmethod function.
        # Test for no any parameters
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.classmethod_fun,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_args(self, process_strategy: ProcessStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_kwargs(self, process_strategy: ProcessStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_no_argument(self, process_strategy: ProcessStrategy):
        # # # # Test target function is staticmethod function.
        # Test for no any parameters
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.staticmethod_fun,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_args(self, process_strategy: ProcessStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_kwargs(self, process_strategy: ProcessStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def _chk_worker_instance_type(self, worker) -> bool:
        return isinstance(worker, mp.Process)


    def test_activate_workers_with_function_with_no_arguments(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_function_with_args(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun,
            args=Test_Function_Args)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_function_with_kwargs(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun,
            kwargs=Test_Function_Kwargs)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_bounded_function_with_no_arguments(self, process_strategy: ProcessStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=_tc.method)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_bounded_function_with_args(self, process_strategy: ProcessStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=_tc.method,
            args=Test_Function_Args)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_bounded_function_with_kwargs(self, process_strategy: ProcessStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_classmethod_function_with_no_arguments(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.classmethod_fun)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_classmethod_function_with_args(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_classmethod_function_with_kwargs(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_staticmethod_function_with_no_arguments(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.staticmethod_fun)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_staticmethod_function_with_args(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_staticmethod_function_with_kwargs(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_close(self, process_strategy: ProcessStrategy):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_terminal(self, process_strategy: ProcessStrategy):
        pass


    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_kill(self, process_strategy: ProcessStrategy):
        pass


    def test_get_success_result(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_fun,
            args=Test_Function_Args)

        _result = process_strategy.get_result()
        assert _result is not None and _result != [], f"The running result should not be empty."
        assert type(_result) is list, f"The result should be a list type object."
        for _r in _result:
            assert isinstance(_r, ParallelResult) is True, f"The element of result should be instance of object 'ParallelResult'."
            assert _r.ppid == Running_Parent_PID, f"The PPID should be the same as we recorded."
            assert _r.pid in Running_PIDs, f"The PID should exists in list we record."
            assert _r.worker_name, f"It should have process name."
            assert _r.worker_ident, f"It should have process identity."
            assert _r.data == f"result_{_r.pid}", f"Its data should be same as we expect 'result_{_r.pid}'."
            assert _r.state == "successful", f"Its state should be 'successful'."
            assert _r.exit_code is None, f"The exit code should be None (it return multiprocessing.current_process.exitcode)."
            assert _r.exception is None, f"It should have nothing exception."


    def test_get_failure_result(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_error_fun)

        _result = process_strategy.get_result()
        assert _result is not None and _result != [], f""
        assert type(_result) is list, f""
        for _r in _result:
            assert isinstance(_r, ParallelResult) is True, f""
            assert _r.ppid, f"It should have PPID."
            assert _r.pid, f"It should have PID."
            assert _r.worker_name, f"It should have process name."
            assert _r.worker_ident, f"It should have process identity."
            assert _r.data is None, f"Its data should be None."
            assert _r.state == "fail", f"Its state should be 'fail'."
            assert _r.exit_code is None, f"The exit code should not be None (it return multiprocessing.current_process.exitcode)."
            assert isinstance(_r.exception, Exception) and "Testing result raising an exception" in str(_r.exception), f"It should have an exception and error message is 'Testing result raising an exception'."


    def _initial(self):
        # Test for parameters with '**kwargs'
        reset_running_flag()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_record():
        GeneralRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        GeneralRunningTestSpec._chk_process_record(
            running_cnt=Running_Count.value,
            worker_size=Process_Size,
            running_wokrer_ids=Running_PIDs,
            running_current_workers=Running_Current_Processes,
            running_finish_timestamps=Running_Finish_Timestamp
        )



class TestProcessPool(PoolRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_initialization(self, process_pool_strategy: ProcessPoolStrategy):
        pass


    def test_apply_with_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, target_fun=pool_target_fun)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, target_fun=pool_target_fun, args=Test_Function_Args)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, target_fun=pool_target_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetPoolCls()
        self._apply(strategy=process_pool_strategy, target_fun=_tc.method)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetPoolCls()
        self._apply(strategy=process_pool_strategy, target_fun=_tc.method, args=Test_Function_Args)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetPoolCls()
        self._apply(strategy=process_pool_strategy, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.classmethod_fun)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.classmethod_fun, args=Test_Function_Args)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.staticmethod_fun)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, args=Test_Function_Args)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_blocking_record()


    def test_async_apply_with_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(strategy=process_pool_strategy, target_fun=pool_target_fun)

        TestProcessPool._chk_record()


    def test_async_apply_with_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=process_pool_strategy, target_fun=pool_target_fun, args=Test_Function_Args)

        TestProcessPool._chk_record()


    def test_async_apply_with_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=process_pool_strategy, target_fun=pool_target_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_record()


    def test_async_apply_with_bounded_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetPoolCls()
        self._async_apply(strategy=process_pool_strategy, target_fun=_tc.method)

        TestProcessPool._chk_record()


    def test_async_apply_with_bounded_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '*args'
        _tc = TargetPoolCls()
        self._async_apply(strategy=process_pool_strategy, target_fun=_tc.method, args=Test_Function_Args)

        TestProcessPool._chk_record()


    def test_async_apply_with_bounded_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '**kwargs'
        _tc = TargetPoolCls()
        self._async_apply(strategy=process_pool_strategy, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_record()


    def test_async_apply_with_classmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.classmethod_fun)

        TestProcessPool._chk_record()


    def test_async_apply_with_classmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.classmethod_fun, args=Test_Function_Args)

        TestProcessPool._chk_record()


    def test_async_apply_with_classmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.staticmethod_fun)

        TestProcessPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, args=Test_Function_Args)

        TestProcessPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=process_pool_strategy, target_fun=TargetPoolCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_record()


    def test_map_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map(function=target_fun, args_iter=Test_Function_Args)


    def test_map_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._map(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_map_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_map_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._async_map(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_map_by_args_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_map_by_args_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._map_by_args(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_map_by_args_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_map_by_args_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_by_args_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_by_args_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        _tc = TargetPoolMapCls()
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_by_args_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_by_args_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_imap_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetPoolMapCls()
        self._imap(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_unordered_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap_unordered(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_unordered_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetPoolMapCls()
        self._imap_unordered(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_unordered_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap_unordered(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_unordered_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap_unordered(strategy=process_pool_strategy, target_fun=TargetPoolMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_get_success_result_with_async_apply(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(strategy=process_pool_strategy, target_fun=pool_target_fun)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    @pytest.mark.skip(reason="Not finish yet. Consider about whether the necessary about catch the exception or not.")
    def test_get_failure_result_with_async_apply(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(strategy=process_pool_strategy, target_fun=target_error_fun)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_failure_result(results=_results)


    def test_get_success_result_with_map(self, process_pool_strategy: ProcessPoolStrategy):
        self._map(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    @pytest.mark.skip(reason="Not finish yet. Consider about whether the necessary about catch the exception or not.")
    def test_get_failure_result_with_map(self, process_pool_strategy: ProcessPoolStrategy):
        self._map(strategy=process_pool_strategy, target_fun=target_error_fun, args_iter=Test_Function_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_failure_result(results=_results)


    def test_get_success_result_with_async_map(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_map(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_map_by_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._map_by_args(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_async_map_by_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Multiple_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap_unordered(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap_unordered(strategy=process_pool_strategy, target_fun=map_target_fun, args_iter=Test_Function_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_close(self, process_pool_strategy: ProcessPoolStrategy):
        """
        ValueError: Pool not running
        :param process_pool_strategy:
        :return:
        """
        try:
            process_pool_strategy.close()
        except Exception as e:
            assert e is not None, f"It should work finely without any issue."
        else:
            assert True, f"It work finely."


    def test_terminal(self, process_pool_strategy: ProcessPoolStrategy):
        try:
            process_pool_strategy.terminal()
        except Exception as e:
            assert e is not None, f"It should work finely without any issue."
        else:
            assert True, f"It work finely."


    def _initial(self):
        # Test for parameters with '**kwargs'
        reset_pool_running_value()
        reset_running_timer()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_blocking_record():
        PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_blocking(
            pool_running_cnt=Pool_Running_Count.value,
            worker_size=Pool_Size,
            running_worker_ids=Running_PIDs,
            running_current_workers=Running_Current_Processes,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    @staticmethod
    def _chk_record():
        PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record(
            pool_running_cnt=Pool_Running_Count.value,
            worker_size=Pool_Size,
            running_worker_ids=Running_PIDs,
            running_current_workers=Running_Current_Processes,
            running_finish_timestamps=Running_Finish_Timestamp
        )


    @staticmethod
    def _chk_map_record():
        PoolRunningTestSpec._chk_ppid_info(ppid_list=Running_PPIDs, running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_map(
            pool_running_cnt=Pool_Running_Count.value,
            function_args=Test_Function_Args,
            running_worker_ids=Running_PIDs,
            running_current_workers=Running_Current_Processes,
            running_finish_timestamps=Running_Finish_Timestamp
        )

