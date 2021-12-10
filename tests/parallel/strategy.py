from multirunnable.parallel.strategy import ParallelStrategy, ProcessStrategy, ProcessPoolStrategy

from ..framework.strategy import GeneralRunningTestSpec, PoolRunningTestSpec
from typing import List, Tuple, Dict
import multiprocessing as mp
import datetime
import pytest
import time
import os


Process_Size: int = 10
Pool_Size: int = 10
Task_Size: int = 10

_Manager = mp.Manager()
# _Process_Lock = _Manager.Lock()
_Process_Lock = mp.Lock()
_Enable_Lock: bool = False

Running_Parent_PID = None
Running_Count = _Manager.Value("i", 0)
Running_PIDs: List = _Manager.list()
Running_PPIDs: List = _Manager.list()
Running_Current_Processes: List = _Manager.list()
Running_Finish_Timestamp: List = _Manager.list()
Pool_Running_Count = 0
# Running_PIDs: List = []
# Running_PPIDs: List = []
# Running_Current_Processes: List = []
# Running_Finish_Timestamp: List = []


def enable_process_lock():
    global _Enable_Lock
    _Enable_Lock = True


def disable_process_lock():
    global _Enable_Lock
    _Enable_Lock = False


def reset_running_flag() -> None:
    global Running_Count
    Running_Count = _Manager.Value("i", 0)
    # Running_Count = 0


def reset_running_timer() -> None:
    global Running_PIDs, Running_PPIDs, Running_Current_Processes, Running_Finish_Timestamp
    Running_PIDs[:] = []
    Running_PPIDs[:] = []
    Running_Current_Processes[:] = []
    Running_Finish_Timestamp[:] = []


Test_Function_Sleep_Time = 7
Test_Function_Args: Tuple = (1, 2, "test_value")
Test_Function_Kwargs: Dict = {"param_1": 1, "param_2": 2, "test_param": "test_value"}


def target_fun(*args, **kwargs) -> str:
    global Running_Count

    with _Process_Lock:
        Running_Count.value += 1
        # Running_Count += 1
        print(f"Running_Count: {Running_Count} - {mp.current_process()}")

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        # _time = str(datetime.datetime.now())
        _time = str(time.time())

        Running_PIDs.append(_pid)
        Running_PPIDs.append(_ppid)
        Running_Current_Processes.append(_time)
        Running_Finish_Timestamp.append(_time)

    time.sleep(Test_Function_Sleep_Time)
    return f"result_{mp.current_process()}"


def pool_target_fun(*args, **kwargs) -> str:
    global Pool_Running_Count

    with _Process_Lock:
        # Running_Count.value += 1
        Pool_Running_Count += 1
        print(f"Running_Count: {Running_Count} - {mp.current_process()}")

        if args:
            assert args == Test_Function_Args, f"The argument *args* should be same as the input outside."
        if kwargs:
            assert kwargs == Test_Function_Kwargs, f"The argument *kwargs* should be same as the input outside."

        _pid = os.getpid()
        _ppid = os.getppid()
        # _time = str(datetime.datetime.now())
        _time = str(time.time())

        Running_PIDs.append(_pid)
        Running_PPIDs.append(_ppid)
        Running_Current_Processes.append(_time)
        Running_Finish_Timestamp.append(_time)

    time.sleep(Test_Function_Sleep_Time)
    return f"result_{mp.current_process()}"


class TargetCls:

    def method(self, *args, **kwargs) -> None:
        target_fun(*args, **kwargs)


    @classmethod
    def classmethod_fun(cls, *args, **kwargs) -> None:
        target_fun(*args, **kwargs)


    @staticmethod
    def staticmethod_fun(*args, **kwargs) -> None:
        target_fun(*args, **kwargs)


@pytest.fixture(scope="class")
def process_strategy():
    return ProcessStrategy(executors=Process_Size)


@pytest.fixture(scope="class")
def process_pool_strategy():
    _strategy = ProcessPoolStrategy(pool_size=Pool_Size, tasks_size=Task_Size)
    _strategy.initialization()
    return _strategy


class TestProcess(GeneralRunningTestSpec):

    def test_initialization(self, process_strategy: ProcessStrategy):
        pass


    def test_start_new_worker(self, process_strategy: ProcessStrategy):
        pass


    def test_generate_worker(self, process_strategy: ProcessStrategy):
        pass
        # # Test for no any parameters
        # _processes = [process_strategy.generate_worker(target_fun) for _ in range(Process_Size)]
        # _processes_chksums = map(TestProcess._chk_process_instn, _processes)
        # assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."
        #
        # # Test for parameters with '*args'
        # _processes_with_args = [process_strategy.generate_worker(target_fun, *Test_Function_Args) for _ in range(Process_Size)]
        # _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_args)
        # assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."
        #
        # # Test for parameters with '**kwargs'
        # _processes_with_kwargs = [process_strategy.generate_worker(target_fun, **Test_Function_Kwargs) for _ in range(Process_Size)]
        # _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_kwargs)
        # assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_function_with_no_argument(self, process_strategy: ProcessStrategy):
        # Test for no any parameters
        _processes = [process_strategy.generate_worker(target_fun) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_function_with_args(self, process_strategy: ProcessStrategy):
        # Test for parameters with '*args'
        _processes_with_args = [process_strategy.generate_worker(target_fun, *Test_Function_Args) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_args)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_function_with_kwargs(self, process_strategy: ProcessStrategy):
        # Test for parameters with '**kwargs'
        _processes_with_kwargs = [process_strategy.generate_worker(target_fun, **Test_Function_Kwargs) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_kwargs)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_bounded_function_with_no_argument(self, process_strategy: ProcessStrategy):
        # # # # Test target function is bounded function.
        # Test for no any parameters
        _tc = TargetCls()
        _processes = [process_strategy.generate_worker(_tc.method) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_bounded_function_with_args(self, process_strategy: ProcessStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '*args'
        _tc = TargetCls()
        _processes_with_args = [process_strategy.generate_worker(_tc.method, *Test_Function_Args) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_args)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_bounded_function_with_kwargs(self, process_strategy: ProcessStrategy):
        # # # # Test target function is bounded function.
        # Test for parameters with '**kwargs'
        _tc = TargetCls()
        _processes_with_kwargs = [process_strategy.generate_worker(_tc.method, **Test_Function_Kwargs) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_kwargs)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_classmethod_function_with_no_argument(self, process_strategy: ProcessStrategy):
        # # # # Test target function is classmethod function.
        # Test for no any parameters
        _processes = [process_strategy.generate_worker(TargetCls.classmethod_fun) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_classmethod_function_with_args(self, process_strategy: ProcessStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '*args'
        _processes_with_args = [process_strategy.generate_worker(TargetCls.classmethod_fun, *Test_Function_Args) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_args)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_classmethod_function_with_kwargs(self, process_strategy: ProcessStrategy):
        # # # # Test target function is classmethod function.
        # Test for parameters with '**kwargs'
        _processes_with_kwargs = [process_strategy.generate_worker(TargetCls.classmethod_fun, **Test_Function_Kwargs) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_kwargs)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_staticmethod_function_with_no_argument(self, process_strategy: ProcessStrategy):
        # # # # Test target function is staticmethod function.
        # Test for no any parameters
        _processes = [process_strategy.generate_worker(TargetCls.staticmethod_fun) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_staticmethod_function_with_args(self, process_strategy: ProcessStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '*args'
        _processes_with_args = [process_strategy.generate_worker(TargetCls.staticmethod_fun, *Test_Function_Args) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_args)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    def test_generate_worker_with_staticmethod_function_with_kwargs(self, process_strategy: ProcessStrategy):
        # # # # Test target function is staticmethod function.
        # Test for parameters with '**kwargs'
        _processes_with_kwargs = [process_strategy.generate_worker(TargetCls.staticmethod_fun, **Test_Function_Kwargs) for _ in range(Process_Size)]
        _processes_chksums = map(TestProcess._chk_process_instn, _processes_with_kwargs)
        assert False not in list(_processes_chksums), f"The instances which be created by method 'generate_worker' should be an instance of 'multiprocessing.Process'."


    @staticmethod
    def _chk_process_instn(process) -> bool:
        return isinstance(process, mp.Process)


    def test_activate_workers(self, process_strategy: ProcessStrategy):
        pass
        # global Running_Parent_PID
        #
        # enable_process_lock()
        #
        # # Test for no any parameters
        # reset_running_flag()
        # reset_running_timer()
        # Running_Parent_PID = os.getpid()
        # _processes = [process_strategy.generate_worker(target_fun) for _ in range(Process_Size)]
        # process_strategy.activate_workers(_processes)
        # process_strategy.close(_processes)
        # assert Running_Count.value == Process_Size, f"The running count should be the same as the amount of process."
        # # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        # TestProcess._chk_process_record()
        #
        # # Test for parameters with '*args'
        # reset_running_flag()
        # reset_running_timer()
        # Running_Parent_PID = os.getpid()
        # _processes_with_args = [process_strategy.generate_worker(target_fun, *Test_Function_Args) for _ in range(Process_Size)]
        # process_strategy.activate_workers(_processes_with_args)
        # process_strategy.close(_processes_with_args)
        # assert Running_Count.value == Process_Size, f"The running count should be the same as the amount of process."
        # # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        # TestProcess._chk_process_record()
        #
        # # Test for parameters with '**kwargs'
        # reset_running_flag()
        # reset_running_timer()
        # Running_Parent_PID = os.getpid()
        # _processes_with_kwargs = [process_strategy.generate_worker(target_fun, **Test_Function_Kwargs) for _ in range(Process_Size)]
        # process_strategy.activate_workers(_processes_with_kwargs)
        # process_strategy.close(_processes_with_kwargs)
        # assert Running_Count.value == Process_Size, f"The running count should be the same as the amount of process."
        # # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        # TestProcess._chk_process_record()


    def test_activate_workers_with_function_with_no_arguments(self, process_strategy: ProcessStrategy):
        global Running_Parent_PID

        enable_process_lock()

        # Test for no any parameters
        reset_running_flag()
        reset_running_timer()
        Running_Parent_PID = os.getpid()
        _processes = [process_strategy.generate_worker(target_fun) for _ in range(Process_Size)]
        process_strategy.activate_workers(_processes)
        process_strategy.close(_processes)
        assert Running_Count.value == Process_Size, f"The running count should be the same as the amount of process."
        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_process_record()


    def test_activate_workers_with_function_with_args(self, process_strategy: ProcessStrategy):
        global Running_Parent_PID

        enable_process_lock()

        # Test for parameters with '*args'
        reset_running_flag()
        reset_running_timer()
        Running_Parent_PID = os.getpid()
        _processes_with_args = [process_strategy.generate_worker(target_fun, *Test_Function_Args) for _ in range(Process_Size)]
        process_strategy.activate_workers(_processes_with_args)
        process_strategy.close(_processes_with_args)
        assert Running_Count.value == Process_Size, f"The running count should be the same as the amount of process."
        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_process_record()


    def test_activate_workers_with_function_with_kwargs(self, process_strategy: ProcessStrategy):
        global Running_Parent_PID

        enable_process_lock()

        # Test for parameters with '**kwargs'
        reset_running_flag()
        reset_running_timer()
        Running_Parent_PID = os.getpid()
        _processes_with_kwargs = [process_strategy.generate_worker(target_fun, **Test_Function_Kwargs) for _ in range(Process_Size)]
        process_strategy.activate_workers(_processes_with_kwargs)
        process_strategy.close(_processes_with_kwargs)
        assert Running_Count.value == Process_Size, f"The running count should be the same as the amount of process."
        # Check some info which be saved in 'Running_PIDs', 'Running_PPIDs', 'Running_Current_Process' and 'Running_Finish_Timestamp'
        TestProcess._chk_process_record()


    @staticmethod
    def _chk_process_record():
        _ppid_list = Running_PPIDs[:]
        _pid_list = Running_PIDs[:]
        _current_process_list = Running_Current_Processes[:]
        _timestamp_list = Running_Finish_Timestamp[:]

        assert len(set(_ppid_list)) == 1, f"The PPID of each process should be the same."
        assert _ppid_list[0] == Running_Parent_PID, f"The PPID should equal to {Running_Parent_PID}. But it got {_ppid_list[0]}."
        assert len(_pid_list) == Process_Size, f"The count of PID (no de-duplicate) should be the same as the count of processes."
        assert len(set(_pid_list)) == Process_Size, f"The count of PID (de-duplicate) should be the same as the count of processes."
        assert len(_pid_list) == len(_current_process_list), f"The count of current process name (no de-duplicate) should be equal to count of PIDs."
        assert len(set(_pid_list)) == len(set(_current_process_list)), f"The count of current process name (de-duplicate) should be equal to count of PIDs."


    def test_close(self, process_strategy: ProcessStrategy):
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


    def test_terminal(self, process_strategy: ProcessStrategy):
        pass


    def test_kill(self, process_strategy: ProcessStrategy):
        pass


    def test_get_result(self, process_strategy: ProcessStrategy):
        pass



class TestProcessPool(PoolRunningTestSpec):

    def test_initialization(self, process_pool_strategy: ProcessPoolStrategy):
        pass


    def test_apply(self, process_pool_strategy: ProcessPoolStrategy):
        pass
        # Test for no any parameters
        # process_pool_strategy.apply(target_fun)

        # Test for parameters with '*args'
        # process_pool_strategy.apply(target_fun, *Test_Function_Args)

        # Test for parameters with '**kwargs'
        # process_pool_strategy.apply(target_fun, **Test_Function_Kwargs)


    def test_async_apply(self, process_pool_strategy: ProcessPoolStrategy):
        global Running_Parent_PID

        disable_process_lock()

        # Test for no any parameters
        reset_running_flag()
        reset_running_timer()
        Running_Parent_PID = os.getpid()
        process_pool_strategy.async_apply(function=pool_target_fun)
        assert Pool_Running_Count == Pool_Size, f"The running count should be the same as the process pool size."
        TestProcess._chk_process_record()

        # Test for parameters with '*args'
        # process_pool_strategy.async_apply(function=target_fun, args=Test_Function_Args)

        # Test for parameters with '**kwargs'
        # process_pool_strategy.async_apply(function=target_fun, kwargs=Test_Function_Kwargs)


    def test_map(self, process_pool_strategy: ProcessPoolStrategy):
        pass
        # Test for no any parameters
        # process_pool_strategy.map(function=target_fun)

        # Test for parameters with '*args'
        # process_pool_strategy.map(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map(self, process_pool_strategy: ProcessPoolStrategy):
        pass
        # Test for no any parameters
        # process_pool_strategy.async_map(function=target_fun)

        # Test for parameters with '*args'
        # process_pool_strategy.async_map(function=target_fun, args_iter=Test_Function_Args)


    def test_map_by_args(self, process_pool_strategy: ProcessPoolStrategy):
        pass
        # Test for no any parameters
        # process_pool_strategy.map_by_args(function=target_fun)

        # Test for parameters with '*args'
        # process_pool_strategy.map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_async_map_by_args(self, process_pool_strategy: ProcessPoolStrategy):
        pass
        # Test for no any parameters
        # process_pool_strategy.async_map_by_args(function=target_fun)

        # Test for parameters with '*args'
        # process_pool_strategy.async_map_by_args(function=target_fun, args_iter=Test_Function_Args)


    def test_imap(self, process_pool_strategy: ProcessPoolStrategy):
        pass
        # Test for no any parameters
        # process_pool_strategy.imap(function=target_fun)

        # Test for parameters with '*args'
        # process_pool_strategy.imap(function=target_fun, args_iter=Test_Function_Args)


    def test_imap_unordered(self, process_pool_strategy: ProcessPoolStrategy):
        pass
        # Test for no any parameters
        # process_pool_strategy.imap_unordered(function=target_fun)

        # Test for parameters with '*args'
        # process_pool_strategy.imap_unordered(function=target_fun, args_iter=Test_Function_Args)


    def test_close(self, process_pool_strategy: ProcessPoolStrategy):
        pass


    def test_terminal(self, process_pool_strategy: ProcessPoolStrategy):
        pass


    def test_get_result(self, process_pool_strategy: ProcessPoolStrategy):
        pass



