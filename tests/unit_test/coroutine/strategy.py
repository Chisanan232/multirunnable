import asyncio
import gevent
import pytest
import re

from multirunnable.coroutine.strategy import GreenThreadStrategy, GreenThreadPoolStrategy, AsynchronousStrategy
from multirunnable.coroutine.result import CoroutineResult
from multirunnable import set_mode, RunningMode, PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ...test_config import (
    Worker_Size, Worker_Pool_Size, Task_Size,
    Test_Function_Args, Test_Function_Multiple_Args, Test_Function_Kwargs, Test_Function_Multiple_Diff_Args
)
from ..._examples import (
    # # Import the flags
    get_running_cnt, get_current_workers, get_running_workers_ids, get_running_done_timestamps,
    # # Import some common functions
    reset_running_flags, initial_lock, initial_async_event_loop,
    # # Import some target functions to run for Pool object
    target_function, target_error_function, target_function_for_map, target_function_for_map_with_diff_args, target_async_function,
    TargetCls, TargetMapCls, TargetAsyncCls,
    target_funcs_iter, target_methods_iter, target_classmethods_iter, target_staticmethods_iter,
    target_func_args_iter, target_funcs_kwargs_iter
)
from ..framework.strategy import GeneralRunningTestSpec, PoolRunningTestSpec


Green_Thread_Size: int = Worker_Size
Pool_Size: int = Worker_Pool_Size
Task_Size: int = Task_Size


@pytest.fixture(scope="class")
def strategy() -> GreenThreadStrategy:
    set_mode(mode=RunningMode.GreenThread)
    _strategy = GreenThreadStrategy(executors=Green_Thread_Size)
    _strategy.initialization()
    return _strategy


@pytest.fixture(scope="class")
def pool_strategy() -> GreenThreadPoolStrategy:
    set_mode(mode=RunningMode.GreenThread)
    _strategy = GreenThreadPoolStrategy(pool_size=Pool_Size)
    _strategy.initialization()
    return _strategy


@pytest.fixture(scope="class")
def async_strategy() -> AsynchronousStrategy:
    set_mode(mode=RunningMode.Asynchronous)
    return AsynchronousStrategy(executors=Green_Thread_Size)


_Generate_Worker_Error_Msg = "" \
                             "The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


class TestGreenThread(GeneralRunningTestSpec):

    def test_start_new_worker_with_function_with_no_argument(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_function_with_args(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function,
            args=Test_Function_Args)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function,
            kwargs=Test_Function_Kwargs)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_no_argument(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_args(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            args=Test_Function_Args)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_bounded_function_with_kwargs(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_args(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_classmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_args(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_start_new_worker_with_staticmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._start_new_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs)

        TestGreenThread._chk_record()
        strategy.reset_result()


    def test_generate_worker_with_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # Test for no any parameters
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_function_with_args(self, strategy: GreenThreadStrategy):
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for no any parameters
        _tc = TargetCls()
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_args(self, strategy: GreenThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '*args'
        _tc = TargetCls()
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_bounded_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '**kwargs'
        _tc = TargetCls()
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for no any parameters
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_args(self, strategy: GreenThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_classmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_no_argument(self, strategy: GreenThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for no any parameters
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_args(self, strategy: GreenThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '*args'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def test_generate_worker_with_staticmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '**kwargs'
        self._generate_worker(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs,
            error_msg=_Generate_Worker_Error_Msg)

        strategy.reset_result()


    def _chk_worker_instance_type(self, _thread) -> bool:
        return isinstance(_thread, gevent.Greenlet)


    def test_activate_workers_with_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_function_with_args(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_bounded_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_bounded_function_with_args(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_bounded_function_with_kwargs(self, strategy: GreenThreadStrategy):
        _tc = TargetCls()
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=_tc.method,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_classmethod_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_classmethod_function_with_args(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_classmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.classmethod_fun,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_staticmethod_function_with_no_arguments(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_staticmethod_function_with_args(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            args=Test_Function_Args)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_activate_workers_with_staticmethod_function_with_kwargs(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=TargetCls.staticmethod_fun,
            kwargs=Test_Function_Kwargs)

        strategy.reset_result()

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestGreenThread._chk_record()


    def test_get_success_result(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_function,
            args=Test_Function_Args)

        _result = strategy.get_result()
        assert _result is not None and _result != [], "The running result should not be empty."
        assert type(_result) is list, "The result should be a list type object."
        for _r in _result:
            assert isinstance(_r, CoroutineResult) is True, "The element of result should be instance of object 'ConcurrentResult'."
            assert _r.pid, "The PID should exists in list we record."
            assert _r.worker_name, "It should have thread name."
            assert _r.worker_ident, "It should have thread identity."
            # assert _r.loop, ""
            assert _r.parent, ""
            assert _r.args is not None, ""
            assert _r.kwargs is not None, ""
            assert _r.data == f"result_{_r.worker_ident}", f"Its data should be same as we expect 'result_{_r.pid}'."
            assert _r.state == "successful", "Its state should be 'successful'."
            assert _r.exception is None, "It should have nothing exception."


    def test_get_failure_result(self, strategy: GreenThreadStrategy):
        self._activate_workers(
            strategy=strategy,
            worker_size=Green_Thread_Size,
            target_fun=target_error_function)

        _result = strategy.get_result()
        assert _result is not None and _result != [], ""
        assert type(_result) is list, ""
        for _r in _result:
            assert isinstance(_r, CoroutineResult) is True, ""
            assert _r.pid, "It should have PID."
            assert _r.worker_name, "It should have thread name."
            assert _r.worker_ident, "It should have thread identity."
            # assert _r.loop, ""
            assert _r.parent, ""
            assert _r.args is not None, ""
            assert _r.kwargs is not None, ""
            assert _r.data is None, "Its data should be None."
            assert _r.state == "fail", "Its state should be 'fail'."
            assert isinstance(_r.exception, Exception) and "Testing result raising an exception" in str(_r.exception), "It should have an exception and error message is 'Testing result raising an exception'."


    def _initial(self):
        # Test for parameters with '**kwargs'
        # reset_running_flag()
        # reset_running_timer()
        reset_running_flags()
        initial_lock()

        # global Running_Parent_PID
        # Running_Parent_PID = os.getpid()


    @staticmethod
    def _chk_record():
        GeneralRunningTestSpec._chk_process_record(
            running_cnt=get_running_cnt(),
            worker_size=Green_Thread_Size,
            running_wokrer_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps()
        )



class TestGreenThreadPool(PoolRunningTestSpec):

    def test_apply_with_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=target_function)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=target_function, args=Test_Function_Args)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=target_function, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetCls()
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=_tc.method)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetCls()
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=_tc.method, args=Test_Function_Args)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_bounded_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetCls()
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_classmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_staticmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_blocking_record()


    def test_async_apply_with_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=target_function)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=target_function, args=Test_Function_Args)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=target_function, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_bounded_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetCls()
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=_tc.method)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_bounded_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        _tc = TargetCls()
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=_tc.method, args=Test_Function_Args)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_bounded_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        _tc = TargetCls()
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=_tc.method, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_classmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_classmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_classmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.classmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '*args'
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun, args=Test_Function_Args)

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_staticmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for parameters with '**kwargs'
        self._async_apply(strategy=pool_strategy, tasks_size=Task_Size, target_fun=TargetCls.staticmethod_fun, kwargs=Test_Function_Kwargs)

        TestGreenThreadPool._chk_record()


    def test_apply_with_iter_with_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(strategy=pool_strategy, target_funcs_iter=target_funcs_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_funcs_iter(),
            args_iter=target_func_args_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_funcs_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_bounded_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(strategy=pool_strategy, target_funcs_iter=target_methods_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_bounded_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_methods_iter(),
            args_iter=target_func_args_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_bounded_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_methods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_classmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(strategy=pool_strategy, target_funcs_iter=target_classmethods_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_classmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_classmethods_iter(),
            args_iter=target_func_args_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_classmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_classmethods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_staticmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(strategy=pool_strategy, target_funcs_iter=target_staticmethods_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_staticmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_staticmethods_iter(),
            args_iter=target_func_args_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_apply_with_iter_with_staticmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_staticmethods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestGreenThreadPool._chk_blocking_record()


    def test_async_apply_with_iter_with_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(strategy=pool_strategy, target_funcs_iter=target_funcs_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_funcs_iter(),
            args_iter=target_func_args_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_funcs_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_bounded_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(strategy=pool_strategy, target_funcs_iter=target_methods_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_bounded_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_methods_iter(),
            args_iter=target_func_args_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_bounded_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_methods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_classmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(strategy=pool_strategy, target_funcs_iter=target_classmethods_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_classmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_classmethods_iter(),
            args_iter=target_func_args_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_classmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_classmethods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_staticmethod_function_with_no_arguments(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(strategy=pool_strategy, target_funcs_iter=target_staticmethods_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_staticmethod_function_with_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_staticmethods_iter(),
            args_iter=target_func_args_iter())

        TestGreenThreadPool._chk_record()


    def test_async_apply_with_iter_with_staticmethod_function_with_kwargs(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply_with_iter(
            strategy=pool_strategy,
            target_funcs_iter=target_staticmethods_iter(),
            kwargs_iter=target_funcs_kwargs_iter())

        TestGreenThreadPool._chk_record()


    def test_map_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map(function=target_fun, args_iter=Test_Function_Args)


    def test_map_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetMapCls()
        self._map(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map(strategy=pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map(strategy=pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.async_map(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetMapCls()
        self._async_map(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map(strategy=pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_by_args_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()

        self._map_by_args(strategy=pool_strategy, target_fun=target_function_for_map_with_diff_args, args_iter=Test_Function_Multiple_Diff_Args)

        TestGreenThreadPool._chk_map_record()

        # Test for parameters with '*args'
        # process_pool_strategy.map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_map_by_args_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetMapCls()
        self._map_by_args(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_by_args_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_map_by_args_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._map_by_args(strategy=pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_by_args_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()

        self._async_map_by_args(strategy=pool_strategy, target_fun=target_function_for_map_with_diff_args, args_iter=Test_Function_Multiple_Diff_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_by_args_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        _tc = TargetMapCls()
        self._async_map_by_args(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_by_args_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_async_map_by_args_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        # Test for no any parameters
        self._async_map_by_args(strategy=pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Multiple_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetMapCls()
        self._imap(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_unordered_with_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_unordered_with_bounded_function(self, pool_strategy: GreenThreadPoolStrategy):
        _tc = TargetMapCls()
        self._imap_unordered(strategy=pool_strategy, target_fun=_tc.method, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_unordered_with_classmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=TargetMapCls.classmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_imap_unordered_with_staticmethod_function(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=TargetMapCls.staticmethod_fun, args_iter=Test_Function_Args)

        TestGreenThreadPool._chk_map_record()


    def test_get_success_result_with_async_apply(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(tasks_size=Task_Size, strategy=pool_strategy, target_fun=target_function)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    @pytest.mark.skip(reason="Still consider about this feature.")
    def test_get_failure_result_with_async_apply(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_apply(tasks_size=Task_Size, strategy=pool_strategy, target_fun=target_error_function)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_failure_result(results=_results)


    def test_get_success_result_with_map(self, pool_strategy: GreenThreadPoolStrategy):
        self._map(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_async_map(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_map(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_map_by_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._map_by_args(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Multiple_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_async_map_by_args(self, pool_strategy: GreenThreadPoolStrategy):
        self._async_map_by_args(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Multiple_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_get_success_result_with_imap_unordered(self, pool_strategy: GreenThreadPoolStrategy):
        self._imap_unordered(strategy=pool_strategy, target_fun=target_function_for_map, args_iter=Test_Function_Args)

        _results = pool_strategy.get_result()
        PoolRunningTestSpec._chk_getting_success_result(results=_results)


    def test_close(self, pool_strategy: GreenThreadPoolStrategy):
        """
        ValueError: Pool not running
        :param pool_strategy:
        :return:
        """
        try:
            pool_strategy.close()
        except Exception as e:
            assert e is not None, "It should work finely without any issue."
        else:
            assert True, "It work finely."


    def test_terminal(self, pool_strategy: GreenThreadPoolStrategy):
        try:
            pool_strategy.terminal()
        except Exception as e:
            assert e is not None, "It should work finely without any issue."
        else:
            assert True, "It work finely."


    def _initial(self):
        reset_running_flags()
        initial_lock()


    @staticmethod
    def _chk_blocking_record():
        PoolRunningTestSpec._chk_process_record_blocking(
            pool_running_cnt=get_running_cnt(),
            worker_size=Task_Size,
            running_worker_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps(),
            de_duplicate=False
        )


    @staticmethod
    def _chk_record():
        PoolRunningTestSpec._chk_process_record(
            pool_running_cnt=get_running_cnt(),
            worker_size=Task_Size,
            running_worker_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps()
        )


    @staticmethod
    def _chk_map_record():
        PoolRunningTestSpec._chk_process_record_map(
            pool_running_cnt=get_running_cnt(),
            function_args=Test_Function_Args,
            running_worker_ids=get_running_workers_ids(),
            running_current_workers=get_current_workers(),
            running_finish_timestamps=get_running_done_timestamps()
        )


_Async_Generate_Worker_Error_Msg = \
    "The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


class TestAsynchronous(GeneralRunningTestSpec):

    @pytest.mark.skip(reason="Not implement testing logic.")
    def test_start_new_worker(self, async_strategy: AsynchronousStrategy):
        pass


    def test_generate_worker_with_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # Test for no any parameters
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=target_async_function,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_function_with_args(self, async_strategy: AsynchronousStrategy):
        # Test for parameters with '*args'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=target_async_function,
                args=Test_Function_Args,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # Test for parameters with '**kwargs'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=target_async_function,
                kwargs=Test_Function_Kwargs,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_bounded_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is bounded function.
        # Test for no any parameters
        async def __chk_type():
            _tc = TargetAsyncCls()
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=_tc.method,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_bounded_function_with_args(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '*args'
        async def __chk_type():
            _tc = TargetAsyncCls()
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=_tc.method,
                args=Test_Function_Args,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_bounded_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '**kwargs'
        async def __chk_type():
            _tc = TargetAsyncCls()
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=_tc.method,
                kwargs=Test_Function_Kwargs,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_classmethod_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is classmethod function.
        # Test for no any parameters
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.classmethod_fun,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_classmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '*args'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.classmethod_fun,
                args=Test_Function_Args,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_classmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '**kwargs'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.classmethod_fun,
                kwargs=Test_Function_Kwargs,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_staticmethod_function_with_no_argument(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is staticmethod function.
        # Test for no any parameters
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.staticmethod_fun,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_staticmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '*args'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.staticmethod_fun,
                args=Test_Function_Args,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def test_generate_worker_with_staticmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '**kwargs'
        async def __chk_type():
            self._generate_worker(
                strategy=async_strategy,
                worker_size=Green_Thread_Size,
                target_fun=TargetAsyncCls.staticmethod_fun,
                kwargs=Test_Function_Kwargs,
                error_msg=_Async_Generate_Worker_Error_Msg)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__chk_type())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__chk_type())


    def _chk_worker_instance_type(self, _thread) -> bool:
        return isinstance(_thread, asyncio.Task)


    def test_activate_workers_with_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_function) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_function_with_args(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_function, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_function, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_bounded_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            _tc = TargetAsyncCls()
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(_tc.method) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_bounded_function_with_args(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            _tc = TargetAsyncCls()
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(_tc.method, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_bounded_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            _tc = TargetAsyncCls()
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(_tc.method, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_classmethod_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_classmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_classmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.classmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_staticmethod_function_with_no_arguments(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_staticmethod_function_with_args(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun, *Test_Function_Args) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def test_activate_workers_with_staticmethod_function_with_kwargs(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(TargetAsyncCls.staticmethod_fun, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestAsynchronous._chk_async_task_record()
        async_strategy.reset_result()


    def _initial(self):
        reset_running_flags()
        initial_async_event_loop()
        initial_lock()


    @staticmethod
    def _chk_async_task_record():
        GeneralRunningTestSpec._chk_running_cnt(running_cnt=get_running_cnt(), worker_size=Green_Thread_Size)

        _current_process_list = get_current_workers()[:]
        assert len(_current_process_list) == Green_Thread_Size, "The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_current_process_list)) == Green_Thread_Size, "The count of PID (de-duplicate) should be the same as the count of processes."

        GeneralRunningTestSpec._chk_done_timestamp(timestamp_list=get_running_done_timestamps()[:])


    def test_get_async_result(self, async_strategy: AsynchronousStrategy):
        self._initial()

        async def __run_process():
            await async_strategy.initialization(queue_tasks=None, features=None)
            _async_task = [async_strategy.generate_worker(target_async_function, **Test_Function_Kwargs) for _ in range(Green_Thread_Size)]
            await async_strategy.activate_workers(_async_task)

        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
            asyncio.run(__run_process())
        else:
            _event_loop = asyncio.get_event_loop()
            _event_loop.run_until_complete(__run_process())

        _result = async_strategy.get_result()
        for _r in _result:
            assert _r.pid, "The PID should exists in list we record."
            assert _r.worker_name, "It should have thread name."
            assert _r.worker_ident, "It should have thread identity."
            assert _r.data, "It should not be an empty value."
            _chksum = re.search(r"result_[0-9]{1,64}", str(_r.data))
            assert _chksum is not None, ""
            assert _r.state == "successful", "Its state should be 'successful'."
            assert _r.exception is None, "It should have nothing exception."


