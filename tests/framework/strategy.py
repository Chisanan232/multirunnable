from multirunnable.framework.strategy import GeneralRunnableStrategy, PoolRunnableStrategy, AsyncRunnableStrategy

from ..test_config import Worker_Pool_Size, Running_Diff_Time, Test_Function_Sleep_Time

from abc import ABCMeta, abstractmethod, ABC
from typing import List, Tuple, Dict, Callable
import re



class RunningStrategyTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_initialization(self, **kwargs):
        pass


    @abstractmethod
    def test_close(self, **kwargs):
        pass



class GeneralRunningTestSpec(RunningStrategyTestSpec):

    def _start_new_worker(self, strategy: GeneralRunnableStrategy, worker_size: int, target_fun: Callable, args=None, kwargs=None) -> None:
        self._initial()

        if args is not None:
            _workers = [strategy.start_new_worker(target=target_fun, args=args) for _ in range(worker_size)]
        elif kwargs is not None:
            _workers = [strategy.start_new_worker(target=target_fun, kwargs=kwargs) for _ in range(worker_size)]
        elif args is not None and kwargs is not None:
            _workers = [strategy.start_new_worker(target=target_fun, args=args, kwargs=kwargs) for _ in range(worker_size)]
        else:
            _workers = [strategy.start_new_worker(target=target_fun) for _ in range(worker_size)]
        strategy.close(_workers)


    def _generate_worker(self, strategy: GeneralRunnableStrategy, worker_size: int, target_fun: Callable, error_msg: str, args=None, kwargs=None) -> None:
        if args is not None:
            _workers = [strategy.generate_worker(target_fun, *args) for _ in range(worker_size)]
        elif kwargs is not None:
            _workers = [strategy.generate_worker(target_fun, **kwargs) for _ in range(worker_size)]
        elif args is not None and kwargs is not None:
            _workers = [strategy.generate_worker(target_fun, *args, **kwargs) for _ in range(worker_size)]
        else:
            _workers = [strategy.generate_worker(target_fun) for _ in range(worker_size)]
        _workers_chksums = map(self._chk_worker_instance_type, _workers)
        assert False not in list(_workers_chksums), error_msg


    @abstractmethod
    def _chk_worker_instance_type(self, worker):
        pass


    def _activate_workers(self, strategy: GeneralRunnableStrategy, worker_size: int, target_fun: Callable, args=None, kwargs=None) -> None:
        self._initial()

        if args is not None:
            _workers = [strategy.generate_worker(target_fun, *args) for _ in range(worker_size)]
        elif kwargs is not None:
            _workers = [strategy.generate_worker(target_fun, **kwargs) for _ in range(worker_size)]
        elif args is not None and kwargs is not None:
            _workers = [strategy.generate_worker(target_fun, *args, **kwargs) for _ in range(worker_size)]
        else:
            _workers = [strategy.generate_worker(target_fun) for _ in range(worker_size)]
        _workers = [strategy.generate_worker(target_fun) for _ in range(worker_size)]
        strategy.activate_workers(_workers)
        strategy.close(_workers)


    @abstractmethod
    def _initial(self):
        pass


    @staticmethod
    def _chk_process_record(
            running_cnt: int, worker_size: int, running_wokrer_ids: List[str],
            running_current_workers: List[str], running_finish_timestamps: List[int],
            de_duplicate: bool = True):

        GeneralRunningTestSpec._chk_running_cnt(running_cnt=running_cnt, worker_size=worker_size)

        # _ppid_list = running_ppids[:]
        _worker_id_list = running_wokrer_ids[:]
        _current_worker_list = running_current_workers[:]
        _timestamp_list = running_finish_timestamps[:]

        # GeneralRunningTestSpec._chk_ppid_info(ppid_list=_ppid_list, running_parent_pid=running_parent_pid)
        GeneralRunningTestSpec._chk_worker_id_size(worker_id_list=_worker_id_list, worker_size=worker_size, de_duplicate=de_duplicate)
        GeneralRunningTestSpec._chk_current_worker(worker_id_list=_worker_id_list, current_worker_list=_current_worker_list, de_duplicate=de_duplicate)
        GeneralRunningTestSpec._chk_done_timestamp(timestamp_list=_timestamp_list)


    @staticmethod
    def _chk_running_cnt(running_cnt: int, worker_size: int):
        assert running_cnt == worker_size, f"The running count should be the same as the process pool size."


    @staticmethod
    def _chk_ppid_info(ppid_list: List[str], running_parent_pid: str):
        assert len(set(ppid_list)) == 1, f"The PPID of each process should be the same."
        assert ppid_list[0] == running_parent_pid, f"The PPID should equal to {running_parent_pid}. But it got {ppid_list[0]}."


    @staticmethod
    def _chk_worker_id_size(worker_id_list: List[str], worker_size: int, de_duplicate: bool = True):
        assert len(worker_id_list) == worker_size, f"The count of PID (no de-duplicate) should be the same as the count of processes."
        if de_duplicate is True:
            assert len(set(worker_id_list)) == worker_size, f"The count of PID (de-duplicate) should be the same as the count of processes."


    @staticmethod
    def _chk_current_worker(worker_id_list: List[str], current_worker_list: List[str], de_duplicate: bool = True):
        assert len(worker_id_list) == len(current_worker_list), f"The count of current process name (no de-duplicate) should be equal to count of PIDs."
        if de_duplicate is True:
            assert len(set(worker_id_list)) == len(set(current_worker_list)), f"The count of current process name (de-duplicate) should be equal to count of PIDs."


    @staticmethod
    def _chk_done_timestamp(timestamp_list: List[int]):
        _max_timestamp = max(timestamp_list)
        _min_timestamp = min(timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= Running_Diff_Time, f"Processes should be run in the same time period."



class PoolRunningTestSpec(RunningStrategyTestSpec, ABC):

    def _apply(self, strategy: PoolRunnableStrategy, target_fun: Callable, args=(), kwargs={}):
        self._initial()

        if args:
            strategy.apply(function=target_fun, args=args)
        elif kwargs:
            strategy.apply(function=target_fun, kwargs=kwargs)
        elif args and kwargs:
            strategy.apply(function=target_fun, args=args, kwargs=kwargs)
        else:
            strategy.apply(function=target_fun)


    def _async_apply(self, strategy: PoolRunnableStrategy, target_fun: Callable, args=(), kwargs={}):
        self._initial()

        if args is not None:
            strategy.async_apply(function=target_fun, args=args)
        elif kwargs is not None:
            strategy.async_apply(function=target_fun, kwargs=kwargs)
        elif args is not None and kwargs is not None:
            strategy.async_apply(function=target_fun, args=args, kwargs=kwargs)
        else:
            strategy.async_apply(function=target_fun)


    def _map(self, strategy: PoolRunnableStrategy, target_fun: Callable, args_iter=()):
        self._initial()

        strategy.map(function=target_fun, args_iter=args_iter)


    def _async_map(self, strategy: PoolRunnableStrategy, target_fun: Callable, args_iter=()):
        self._initial()

        strategy.async_map(function=target_fun, args_iter=args_iter)


    def _map_by_args(self, strategy: PoolRunnableStrategy, target_fun: Callable, args_iter=()):
        self._initial()

        strategy.map_by_args(function=target_fun, args_iter=args_iter)


    def _async_map_by_args(self, strategy: PoolRunnableStrategy, target_fun: Callable, args_iter=()):
        self._initial()

        strategy.async_map_by_args(function=target_fun, args_iter=args_iter)


    def _imap(self, strategy: PoolRunnableStrategy, target_fun: Callable, args_iter=()):
        self._initial()

        strategy.imap(function=target_fun, args_iter=args_iter)


    def _imap_unordered(self, strategy: PoolRunnableStrategy, target_fun: Callable, args_iter=()):
        self._initial()

        strategy.imap_unordered(function=target_fun, args_iter=args_iter)


    @abstractmethod
    def _initial(self):
        pass


    @staticmethod
    def _chk_process_record_blocking(
            pool_running_cnt: int, worker_size: int,
            running_worker_ids: List[str], running_current_workers: List[str],
            running_finish_timestamps: List[int], de_duplicate: bool = True):

        GeneralRunningTestSpec._chk_running_cnt(running_cnt=pool_running_cnt, worker_size=worker_size)

        # _ppid_list = running_ppids[:]
        _pid_list = running_worker_ids[:]
        _current_workers_list = running_current_workers[:]
        _timestamp_list = running_finish_timestamps[:]

        # GeneralRunningTestSpec._chk_ppid_info(ppid_list=_ppid_list, running_parent_pid=running_parent_pid)
        GeneralRunningTestSpec._chk_worker_id_size(worker_id_list=_current_workers_list, worker_size=worker_size, de_duplicate=de_duplicate)
        GeneralRunningTestSpec._chk_current_worker(worker_id_list=_current_workers_list, current_worker_list=_current_workers_list, de_duplicate=de_duplicate)
        PoolRunningTestSpec._chk_blocking_done_timestamp(timestamp_list=_timestamp_list)


    @staticmethod
    def _chk_blocking_done_timestamp(timestamp_list: List[int]):
        _max_timestamp = max(timestamp_list)
        _min_timestamp = min(timestamp_list)
        _diff_timestamp = _max_timestamp - _min_timestamp
        assert _diff_timestamp <= (Test_Function_Sleep_Time * Worker_Pool_Size) + Running_Diff_Time, f"Processes should be run in the same time period."


    @staticmethod
    def _chk_process_record(
            pool_running_cnt: int, worker_size: int,
            running_worker_ids: List[str], running_current_workers: List[str],
            running_finish_timestamps: List[int]):

        GeneralRunningTestSpec._chk_process_record(
            running_cnt=pool_running_cnt,
            worker_size=worker_size,
            running_wokrer_ids=running_worker_ids,
            running_current_workers=running_current_workers,
            running_finish_timestamps=running_finish_timestamps
        )


    @staticmethod
    def _chk_ppid_info(ppid_list: List[str], running_parent_pid: str):
        GeneralRunningTestSpec._chk_ppid_info(ppid_list=ppid_list, running_parent_pid=running_parent_pid)


    @staticmethod
    def _chk_process_record_map(
            pool_running_cnt: int, function_args: List[str],
            running_worker_ids: List[str], running_current_workers: List[str],
            running_finish_timestamps: List[int], de_duplicate: bool = True):

        _argument_size = len(function_args)
        GeneralRunningTestSpec._chk_running_cnt(running_cnt=pool_running_cnt, worker_size=_argument_size)

        # _ppid_list = running_ppids[:]
        _pid_list = running_worker_ids[:]
        _current_workers_list = running_current_workers[:]
        _timestamp_list = running_finish_timestamps[:]

        # GeneralRunningTestSpec._chk_ppid_info(ppid_list=_ppid_list, running_parent_pid=running_parent_pid)
        GeneralRunningTestSpec._chk_worker_id_size(worker_id_list=_current_workers_list, worker_size=_argument_size, de_duplicate=de_duplicate)
        GeneralRunningTestSpec._chk_current_worker(worker_id_list=_current_workers_list, current_worker_list=_current_workers_list, de_duplicate=de_duplicate)
        GeneralRunningTestSpec._chk_done_timestamp(timestamp_list=_timestamp_list)


    @staticmethod
    def _chk_getting_success_result(results):
        assert results is not None and results != [], f""
        assert type(results) is list, f""
        for _r in results:
            assert _r.data is not None, f""
            _chksum = re.search(r"result_[0-9]{1,64}", str(_r.data))
            assert _chksum is not None, f""
            assert _r.is_successful is True, f""


    @staticmethod
    def _chk_getting_failure_result(results):
        assert results is not None and results != [], f""
        assert type(results) is list, f""
        for _r in results:
            assert _r.data is not None, f""
            assert isinstance(_r.data, Exception) is True and "Testing result raising an exception" in str(_r.data), f""
            assert _r.is_successful is False, f""

