import multiprocessing as mp
import pytest
import os

from multirunnable.parallel.strategy import ProcessStrategy, ProcessPoolStrategy
from multirunnable.parallel.result import ParallelResult
from multirunnable import set_mode, RunningMode

from ...test_config import (
    Worker_Size, Worker_Pool_Size, Task_Size,
    Test_Function_Args, Test_Function_Multiple_Args, Test_Function_Kwargs)
from ..._examples import (
    # # Import the flags
    get_running_cnt, get_running_ppids, get_current_workers, get_running_workers_ids, get_running_done_timestamps,
    # # Import some common functions
    reset_running_flags, initial_lock,  # # Import some target functions to run for Pool object
    target_function, target_error_function, target_function_for_map, TargetCls, TargetMapCls,
    target_funcs_iter, target_methods_iter, target_classmethods_iter, target_staticmethods_iter,
    target_func_args_iter, target_funcs_kwargs_iter
)
from ..framework.strategy import GeneralRunningTestSpec, PoolRunningTestSpec


Process_Size: int = Worker_Size
Pool_Size: int = Worker_Pool_Size
Task_Size: int = Task_Size


@pytest.fixture(scope="class")
def process_strategy():
    set_mode(mode=RunningMode.Parallel)
    _strategy = ProcessStrategy(executors=Process_Size)
    _strategy.initialization()
    return _strategy


@pytest.fixture(scope="class")
def process_pool_strategy():
    set_mode(mode=RunningMode.Parallel)
    _strategy = ProcessPoolStrategy(pool_size=Pool_Size)
    _strategy.initialization()
    return _strategy


_Generate_Worker_Error_Msg = \
    "The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


class TestProcess(GeneralRunningTestSpec):

    def test_start_new_worker_with_function_with_no_argument(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_function)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_function_with_args(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_function,
            args=Test_Function_Args)

        TestProcess._chk_record()
        process_strategy.reset_result()


    def test_start_new_worker_with_function_with_kwargs(self, process_strategy: ProcessStrategy):
        self._start_new_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_function,
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
            target_fun=target_function,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_function_with_args(self, process_strategy: ProcessStrategy):
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_function,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        process_strategy.reset_result()


    def test_generate_worker_with_function_with_kwargs(self, process_strategy: ProcessStrategy):
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_function,
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
            target_fun=target_function)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_function_with_args(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_function,
            args=Test_Function_Args)

        process_strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_record()


    def test_activate_workers_with_function_with_kwargs(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_function,
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


    def test_get_success_result(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_function,
            args=Test_Function_Args)

        _result = process_strategy.get_result()
        assert _result is not None and _result != [], "The running result should not be empty."
        assert type(_result) is list, "The result should be a list type object."
        for _r in _result:
            assert isinstance(_r, ParallelResult) is True, "The element of result should be instance of object 'ParallelResult'."
            assert _r.ppid == Running_Parent_PID, "The PPID should be the same as we recorded."
            assert str(_r.pid) in list(get_running_workers_ids()), "The PID should exists in list we record."
            assert _r.worker_name, "It should have process name."
            assert _r.worker_ident, "It should have process identity."
            assert _r.data == f"result_{_r.worker_ident}", f"Its data should be same as we expect 'result_{_r.pid}'."
            assert _r.state == "successful", "Its state should be 'successful'."
            assert _r.exit_code is None, "The exit code should be None (it return multiprocessing.current_process.exitcode)."
            assert _r.exception is None, "It should have nothing exception."


    def test_get_failure_result(self, process_strategy: ProcessStrategy):
        self._activate_workers(
            strategy=process_strategy,
            worker_size=Process_Size,
            target_fun=target_error_function)

        _result = process_strategy.get_result()
        assert _result is not None and _result != [], ""
        assert type(_result) is list, ""
        for _r in _result:
            assert isinstance(_r, ParallelResult) is True, ""
            assert _r.ppid, "It should have PPID."
            assert _r.pid, "It should have PID."
            assert _r.worker_name, "It should have process name."
            assert _r.worker_ident, "It should have process identity."
            assert _r.data is None, "Its data should be None."
            assert _r.state == "fail", "Its state should be 'fail'."
            assert _r.exit_code is None, "The exit code should not be None (it return multiprocessing.current_process.exitcode)."
            assert isinstance(_r.exception, Exception) and "Testing result raising an exception" in str(_r.exception), "It should have an exception and error message is 'Testing result raising an exception'."


    def _initial(self):
        reset_running_flags()
        # set_lock(lock=Global_Manager.Lock())
        initial_lock()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_record():
        GeneralRunningTestSpec._chk_ppid_info(ppid_list=get_running_ppids(), running_parent_pid=Running_Parent_PID)
        GeneralRunningTestSpec._chk_process_record(
            running_cnt=get_running_cnt(),
            worker_size=Process_Size,
            running_wokrer_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps()
        )



class TestProcessPool(PoolRunningTestSpec):

    def test_apply_with_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=target_function)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=target_function, args=Test_Function_Args)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=target_function, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetCls()
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=_tc.method)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetCls()
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=_tc.method, args=Test_Function_Args)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetCls()
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun, args=Test_Function_Args)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun, args=Test_Function_Args)

        TestProcessPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_blocking_record()


    def test_async_apply_with_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=target_function)

        TestProcessPool._chk_record()


    def test_async_apply_with_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=target_function, args=Test_Function_Args)

        TestProcessPool._chk_record()


    def test_async_apply_with_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=target_function, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_record()


    def test_async_apply_with_bounded_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetCls()
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=_tc.method)

        TestProcessPool._chk_record()


    def test_async_apply_with_bounded_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '*args'
        _tc = TargetCls()
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=_tc.method, args=Test_Function_Args)

        TestProcessPool._chk_record()


    def test_async_apply_with_bounded_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '**kwargs'
        _tc = TargetCls()
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_record()


    def test_async_apply_with_classmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun)

        TestProcessPool._chk_record()


    def test_async_apply_with_classmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun, args=Test_Function_Args)

        TestProcessPool._chk_record()


    def test_async_apply_with_classmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun)

        TestProcessPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun, args=Test_Function_Args)

        TestProcessPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=process_pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestProcessPool._chk_record()


    def test_apply_with_iter_with_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(strategy=process_pool_strategy, target_funcs_iter=target_funcs_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_funcs_iter(),
            args_iter=target_func_args_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_funcs_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_bounded_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(strategy=process_pool_strategy, target_funcs_iter=target_methods_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_bounded_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_methods_iter(),
            args_iter=target_func_args_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_bounded_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_methods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_classmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(strategy=process_pool_strategy, target_funcs_iter=target_classmethods_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_classmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_classmethods_iter(),
            args_iter=target_func_args_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_classmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_classmethods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_staticmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(strategy=process_pool_strategy, target_funcs_iter=target_staticmethods_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_staticmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_staticmethods_iter(),
            args_iter=target_func_args_iter())

        TestProcessPool._chk_blocking_record()


    def test_apply_with_iter_with_staticmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_staticmethods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestProcessPool._chk_blocking_record()


    def test_async_apply_with_iter_with_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(strategy=process_pool_strategy, target_funcs_iter=target_funcs_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_funcs_iter(),
            args_iter=target_func_args_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_funcs_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_bounded_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(strategy=process_pool_strategy, target_funcs_iter=target_methods_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_bounded_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_methods_iter(),
            args_iter=target_func_args_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_bounded_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_methods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_classmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(strategy=process_pool_strategy, target_funcs_iter=target_classmethods_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_classmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_classmethods_iter(),
            args_iter=target_func_args_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_classmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_classmethods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_staticmethod_function_with_no_arguments(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(strategy=process_pool_strategy, target_funcs_iter=target_staticmethods_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_staticmethod_function_with_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_staticmethods_iter(),
            args_iter=target_func_args_iter())

        TestProcessPool._chk_record()


    def test_async_apply_with_iter_with_staticmethod_function_with_kwargs(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply_with_iter(
            strategy=process_pool_strategy,
            target_funcs_iter=target_staticmethods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestProcessPool._chk_record()


    def test_map_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map(function=target_fun, args_iter=Test_Function_Args)


    def test_map_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        _tc = TargetMapCls()
        self._map(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_map_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map(strategy=process_pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_map_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map(strategy=process_pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        _tc = TargetMapCls()
        self._async_map(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=process_pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=process_pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_map_by_args_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_map_by_args_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        _tc = TargetMapCls()
        self._map_by_args(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_map_by_args_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=process_pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_map_by_args_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=process_pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_by_args_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_by_args_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        _tc = TargetMapCls()
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_by_args_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_async_map_by_args_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestProcessPool._chk_map_record()


    def test_imap_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetMapCls()
        self._imap(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap(strategy=process_pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap(strategy=process_pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_unordered_with_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap_unordered(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_unordered_with_bounded_function(self, process_pool_strategy: ProcessPoolStrategy):
        _tc = TargetMapCls()
        self._imap_unordered(strategy=process_pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_unordered_with_classmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap_unordered(strategy=process_pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_imap_unordered_with_staticmethod_function(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap_unordered(strategy=process_pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestProcessPool._chk_map_record()


    def test_get_success_result_with_async_apply(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(tasks_size=Task_Size, strategy=process_pool_strategy, target_fun=target_function)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    @pytest.mark.skip(reason="Not finish yet. Consider about whether the necessary about catch the exception or not.")
    def test_get_failure_result_with_async_apply(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_apply(tasks_size=Task_Size, strategy=process_pool_strategy, target_fun=target_error_function)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_failure_result(results=_results)


    def test_get_success_result_with_map(self, process_pool_strategy: ProcessPoolStrategy):
        self._map(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    @pytest.mark.skip(reason="Not finish yet. Consider about whether the necessary about catch the exception or not.")
    def test_get_failure_result_with_map(self, process_pool_strategy: ProcessPoolStrategy):
        self._map(strategy=process_pool_strategy, target_fun=target_error_function, args_iter=Test_Function_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_failure_result(results=_results)


    def test_get_success_result_with_async_map(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_map(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_map_by_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._map_by_args(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Multiple_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_async_map_by_args(self, process_pool_strategy: ProcessPoolStrategy):
        self._async_map_by_args(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Multiple_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        _results = process_pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap_unordered(self, process_pool_strategy: ProcessPoolStrategy):
        self._imap_unordered(strategy=process_pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

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
            assert e is not None, "It should work finely without any issue."
        else:
            assert True, "It work finely."


    def test_terminal(self, process_pool_strategy: ProcessPoolStrategy):
        try:
            process_pool_strategy.terminal()
        except Exception as e:
            assert e is not None, "It should work finely without any issue."
        else:
            assert True, "It work finely."


    def _initial(self):
        reset_running_flags()
        # set_lock(lock=Global_Manager.Lock())
        initial_lock()

        global Running_Parent_PID
        Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_blocking_record():
        PoolRunningTestSpec._chk_ppid_info(ppid_list=get_running_ppids(), running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_blocking(
            pool_running_cnt=get_running_cnt(),
            worker_size=Task_Size,
            running_worker_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps()
        )


    @staticmethod
    def _chk_record():
        PoolRunningTestSpec._chk_ppid_info(ppid_list=get_running_ppids(), running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record(
            pool_running_cnt=get_running_cnt(),
            worker_size=Task_Size,
            running_worker_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps()
        )


    @staticmethod
    def _chk_map_record():
        PoolRunningTestSpec._chk_ppid_info(ppid_list=get_running_ppids(), running_parent_pid=Running_Parent_PID)
        PoolRunningTestSpec._chk_process_record_map(
            pool_running_cnt=get_running_cnt(),
            function_args=Test_Function_Args,
            running_worker_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps()
        )

