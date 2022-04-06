from gevent.threading import get_ident as get_gevent_ident
from gevent import sleep as gevent_sleep
from typing import Union
from abc import ABCMeta, abstractmethod, ABC
import multiprocessing
import threading
import asyncio
import pytest
import random
import time

from multirunnable.adapter import Lock, RLock, Semaphore, BoundedSemaphore
from multirunnable.mode import FeatureMode
from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from ...test_config import Worker_Size, Worker_Pool_Size, Task_Size, Semaphore_Value


_Worker_Size = Worker_Size
_Worker_Pool_Size = Worker_Pool_Size
_Task_Size = Task_Size

_Process_Manager = multiprocessing.Manager()

_Semaphore_Value = Semaphore_Value

_Sleep_Time: int = 1
_Random_Start_Time: int = 60
_Random_End_Time: int = 80



class FeatureTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_get_feature_instance(self, **kwargs):
        pass


    def _feature_instance_testing(self, _lock_inst: Union[Lock, RLock, Semaphore, BoundedSemaphore]):
        _lock_operator = _lock_inst._feature_operator

        _global_feature_inst = _lock_operator._get_feature_instance()
        _feature_inst = _lock_operator._feature_instance
        assert _feature_inst is _global_feature_inst, f"The feature property should be the '{_lock_inst.__class__}' instance we set."


    @abstractmethod
    def test_feature_in_parallel(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_parallel(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_in_concurrent(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_concurrent(self, **kwargs):
        pass


    @staticmethod
    def _get_collection_dict(mode: FeatureMode) -> dict:
        if mode is FeatureMode.Parallel:
            return _Process_Manager.dict()
        else:
            return {}


    @staticmethod
    def _get_collection_list(mode: FeatureMode) -> list:
        if mode is FeatureMode.Parallel:
            return _Process_Manager.list()
        else:
            return []


    @staticmethod
    def _get_worker_id(mode: FeatureMode) -> str:
        if mode is FeatureMode.Parallel:
            return str(multiprocessing.current_process().pid)
        elif mode is FeatureMode.Concurrent:
            return str(threading.get_ident())
        elif mode is FeatureMode.GreenThread:
            return str(get_gevent_ident())
        elif mode is FeatureMode.Asynchronous:
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
            else:
                _async_task = asyncio.Task.current_task()
            _async_task_id = id(_async_task)
            return str(_async_task_id)
        else:
            raise ValueError


    @staticmethod
    def _sleep(mode: FeatureMode) -> None:
        if mode is FeatureMode.Parallel or mode is FeatureMode.Concurrent:
            time.sleep(_Sleep_Time)
        elif mode is FeatureMode.GreenThread:
            gevent_sleep(_Sleep_Time)
        elif mode is FeatureMode.Asynchronous:
            asyncio.sleep(_Sleep_Time)
        else:
            raise ValueError



class LockTestSpec(FeatureTestSpec, ABC):

    @abstractmethod
    def test_feature_in_green_thread(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_green_thread(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_in_asynchronous_tasks(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self, **kwargs):
        pass


    @staticmethod
    def _feature_testing(mode: FeatureMode, _lock, running_function):

        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        def _target_testing():
            # Save a timestamp into list
            _lock.acquire()
            _worker_id = FeatureTestSpec._get_worker_id(mode)
            FeatureTestSpec._sleep(mode)
            _time = float(time.time())
            _done_timestamp[_worker_id] = _time
            _lock.release()

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing)
        LockTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _feature_testing_by_pykeyword_with(mode: FeatureMode, _lock, running_function):

        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        def _target_testing():
            # Save a time stamp into list
            try:
                with _lock:
                    _worker_id = FeatureTestSpec._get_worker_id(mode)
                    FeatureTestSpec._sleep(mode)
                    _time = float(time.time())
                    _done_timestamp[_worker_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing)
        LockTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _async_feature_testing(mode: FeatureMode, _lock, running_function, event_loop=None, factory=None):
        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        async def _target_testing():
            # Save a timestamp into list
            await _lock.acquire()
            await asyncio.sleep(_Sleep_Time)
            _worker_id = FeatureTestSpec._get_worker_id(mode)
            _time = float(time.time())
            _done_timestamp[_worker_id] = _time
            _lock.release()

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing, event_loop=event_loop, _feature=factory)
        LockTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _async_feature_testing_by_pykeyword_with(mode: FeatureMode, _lock, running_function, factory=None):
        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        async def _target_testing():
            # Save a time stamp into list
            try:
                async with _lock:
                    await asyncio.sleep(_Sleep_Time)
                    _worker_id = FeatureTestSpec._get_worker_id(mode)
                    _time = float(time.time())
                    _done_timestamp[_worker_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing, _feature=factory)
        LockTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp(_done_timestamp: dict):
        assert len(_done_timestamp.keys()) == _Worker_Size, f"The amount of thread ID keys (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(set(_done_timestamp.keys())) == _Worker_Size, f"The amount of thread ID keys (de-duplicate) should be equal to worker size '{_Worker_Size}'."
        _previous_v = None
        for _v in sorted(_done_timestamp.values()):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time betweeen them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_done_timestamp}"
                _previous_v = _v



class RLockTestSpec(FeatureTestSpec, ABC):

    @abstractmethod
    def test_feature_in_green_thread(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_green_thread(self, **kwargs):
        pass


    @staticmethod
    def _feature_testing(mode: FeatureMode, _lock, running_function):

        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        def _target_testing():
            # Save a timestamp into list
            _lock.acquire()
            _lock.acquire()
            _worker_id = FeatureTestSpec._get_worker_id(mode)
            FeatureTestSpec._sleep(mode)
            _time = float(time.time())
            _done_timestamp[_worker_id] = _time
            _lock.release()
            _lock.release()

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing)
        RLockTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _feature_testing_by_pykeyword_with(mode: FeatureMode, _lock, running_function):

        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        def _target_testing():
            # Save a time stamp into list
            try:
                with _lock:
                    with _lock:
                        _worker_id = FeatureTestSpec._get_worker_id(mode)
                        FeatureTestSpec._sleep(mode)
                        _time = float(time.time())
                        _done_timestamp[_worker_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

            # # # # Run multiple workers and save something info at the right time

        running_function(_function=_target_testing)
        RLockTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp(_done_timestamp: dict):
        assert len(_done_timestamp.keys()) == _Worker_Size, f"The amount of thread ID keys (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(set(_done_timestamp.keys())) == _Worker_Size, f"The amount of thread ID keys (de-duplicate) should be equal to worker size '{_Worker_Size}'."
        _previous_v = None
        for _v in sorted(_done_timestamp.values()):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time betweeen them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_done_timestamp}"
                _previous_v = _v



class SemaphoreTestSpec(FeatureTestSpec, ABC):

    @abstractmethod
    def test_feature_in_green_thread(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_green_thread(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_in_asynchronous_tasks(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self, **kwargs):
        pass


    @staticmethod
    def _feature_testing(mode: FeatureMode, _lock, running_function):

        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        def _target_testing():
            # Save a timestamp into list
            _lock.acquire()
            _worker_id = FeatureTestSpec._get_worker_id(mode)
            FeatureTestSpec._sleep(mode)
            _time = float(time.time())
            _done_timestamp[_worker_id] = _time
            _lock.release()

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing)
        SemaphoreTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _feature_testing_by_pykeyword_with(mode: FeatureMode, _lock, running_function):

        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        def _target_testing():
            # Save a time stamp into list
            try:
                with _lock:
                    _worker_id = FeatureTestSpec._get_worker_id(mode)
                    FeatureTestSpec._sleep(mode)
                    _time = float(time.time())
                    _done_timestamp[_worker_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing)
        SemaphoreTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _async_feature_testing(_lock, running_function, factory=None):
        _done_timestamp = {}

        async def _target_testing():
            # Save a timestamp into list
            await _lock.acquire()
            await asyncio.sleep(_Sleep_Time)
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
            else:
                _async_task = asyncio.Task.current_task()
            _async_task_id = id(_async_task)
            _time = float(time.time())
            _done_timestamp[_async_task_id] = _time
            _lock.release()

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing, _feature=factory)
        SemaphoreTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _async_feature_testing_by_pykeyword_with(_lock, running_function, factory=None):
        _done_timestamp = {}

        async def _target_testing():
            # Save a time stamp into list
            try:
                async with _lock:
                    await asyncio.sleep(_Sleep_Time)
                    if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                        _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
                    else:
                        _async_task = asyncio.Task.current_task()
                    _async_task_id = id(_async_task)
                    _time = float(time.time())
                    _done_timestamp[_async_task_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing, _feature=factory)
        SemaphoreTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp(_done_timestamp: dict):
        assert len(_done_timestamp.keys()) == _Worker_Size, f"The amount of thread ID keys (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(set(_done_timestamp.keys())) == _Worker_Size, f"The amount of thread ID keys (de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(_done_timestamp.values()) == _Worker_Size, f"The amount of done-timestamp (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        _int_unix_time_timestamps = [int(_v) for _v in _done_timestamp.values()]
        if _Worker_Size % 2 == 0:
            assert len(set(_int_unix_time_timestamps)) == int(_Worker_Size / _Semaphore_Value), \
                f"The amount of done-timestamp (de-duplicate) should be equal to (worker size: {_Worker_Size} / semaphore value: {_Semaphore_Value}) '{int(_Worker_Size / _Semaphore_Value)}'."
        else:
            assert len(set(_int_unix_time_timestamps)) == int(_Worker_Size / _Semaphore_Value) + 1, \
                f"The amount of done-timestamp (de-duplicate) should be equal to (worker size: {_Worker_Size} / semaphore value: {_Semaphore_Value}) '{int(_Worker_Size / _Semaphore_Value)}'."
        _previous_v = None
        for _v in sorted(_int_unix_time_timestamps):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time betweeen them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_done_timestamp}"
                _previous_v = _v



class BoundedSemaphoreTestSpec(FeatureTestSpec, ABC):

    @abstractmethod
    def test_feature_in_green_thread(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_green_thread(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_in_asynchronous_tasks(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self, **kwargs):
        pass


    @staticmethod
    def _feature_testing(mode: FeatureMode, _lock, running_function):

        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        def _target_testing():
            # Save a timestamp into list
            _lock.acquire()
            _worker_id = FeatureTestSpec._get_worker_id(mode)
            FeatureTestSpec._sleep(mode)
            _time = float(time.time())
            _done_timestamp[_worker_id] = _time
            _lock.release()

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing)
        BoundedSemaphoreTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _feature_testing_by_pykeyword_with(mode: FeatureMode, _lock, running_function):

        _done_timestamp = FeatureTestSpec._get_collection_dict(mode)

        def _target_testing():
            # Save a time stamp into list
            try:
                with _lock:
                    _worker_id = FeatureTestSpec._get_worker_id(mode)
                    FeatureTestSpec._sleep(mode)
                    _time = float(time.time())
                    _done_timestamp[_worker_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing)
        BoundedSemaphoreTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _async_feature_testing(_lock, running_function, factory=None):
        _done_timestamp = {}

        async def _target_testing():
            # Save a timestamp into list
            await _lock.acquire()
            await asyncio.sleep(_Sleep_Time)
            if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
            else:
                _async_task = asyncio.Task.current_task()
            _async_task_id = id(_async_task)
            _time = float(time.time())
            _done_timestamp[_async_task_id] = _time
            _lock.release()

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing, _feature=factory)
        BoundedSemaphoreTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _async_feature_testing_by_pykeyword_with(_lock, running_function, factory=None):
        _done_timestamp = {}

        async def _target_testing():
            # Save a time stamp into list
            try:
                async with _lock:
                    await asyncio.sleep(_Sleep_Time)
                    if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                        _async_task = asyncio.current_task(loop=asyncio.get_event_loop())
                    else:
                        _async_task = asyncio.Task.current_task()
                    _async_task_id = id(_async_task)
                    _time = float(time.time())
                    _done_timestamp[_async_task_id] = _time
            except Exception as e:
                assert False, f"Occur something unexpected issue. Please check it. Exception: {e}"
            else:
                assert True, "Testing code successfully."

        # # # # Run multiple workers and save something info at the right time
        running_function(_function=_target_testing, _feature=factory)
        BoundedSemaphoreTestSpec._chk_done_timestamp(_done_timestamp)


    @staticmethod
    def _chk_done_timestamp(_done_timestamp: dict):
        assert len(_done_timestamp.keys()) == _Worker_Size, f"The amount of thread ID keys (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(set(_done_timestamp.keys())) == _Worker_Size, f"The amount of thread ID keys (de-duplicate) should be equal to worker size '{_Worker_Size}'."
        assert len(_done_timestamp.values()) == _Worker_Size, f"The amount of done-timestamp (no de-duplicate) should be equal to worker size '{_Worker_Size}'."
        _int_unix_time_timestamps = [int(_v) for _v in _done_timestamp.values()]
        if _Worker_Size % 2 == 0:
            assert len(set(_int_unix_time_timestamps)) == int(_Worker_Size / _Semaphore_Value), \
                f"The amount of done-timestamp (de-duplicate) should be equal to (worker size: {_Worker_Size} / semaphore value: {_Semaphore_Value}) '{int(_Worker_Size / _Semaphore_Value)}'."
        else:
            assert len(set(_int_unix_time_timestamps)) == int(_Worker_Size / _Semaphore_Value) + 1, \
                f"The amount of done-timestamp (de-duplicate) should be equal to (worker size: {_Worker_Size} / semaphore value: {_Semaphore_Value}) '{int(_Worker_Size / _Semaphore_Value)}'."
        _previous_v = None
        for _v in sorted(_int_unix_time_timestamps):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time betweeen them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_done_timestamp}"
                _previous_v = _v



class EventTestSpec(FeatureTestSpec, ABC):

    @abstractmethod
    def test_feature_in_green_thread(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_in_asynchronous_tasks(self, **kwargs):
        pass


    @pytest.mark.xfail(reason="Doesn't support this feature usage via Python keyword 'with'.")
    def test_feature_by_pykeyword_with_in_parallel(self, **kwargs):
        raise Exception("Doesn't support this feature usage via 'with'.")


    @pytest.mark.xfail(reason="Doesn't support this feature usage via Python keyword 'with'.")
    def test_feature_by_pykeyword_with_in_concurrent(self, **kwargs):
        raise Exception("Doesn't support this feature usage via 'with'.")


    @staticmethod
    def _feature_testing(mode: FeatureMode, _lock, running_function):

        _thread_ids = FeatureTestSpec._get_collection_dict(mode)
        _thread_flag = FeatureTestSpec._get_collection_dict(mode)

        _thread_ids["producer"] = ""
        _thread_ids["consumer"] = ""

        _thread_flag["producer"] = FeatureTestSpec._get_collection_list(mode)
        _thread_flag["consumer"] = FeatureTestSpec._get_collection_list(mode)

        def _target_producer():
            for _ in range(3):
                FeatureTestSpec._sleep(mode)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _thread_flag["producer"].append(_thread_index)
                _worker_id = FeatureTestSpec._get_worker_id(mode)
                _thread_ids["producer"] = str(_worker_id)
                _lock.set()

        def _target_consumer():
            while True:
                FeatureTestSpec._sleep(mode)
                _lock.wait()
                _lock.clear()
                _thread_flag["consumer"].append(float(time.time()))
                _worker_id = FeatureTestSpec._get_worker_id(mode)
                _thread_ids["consumer"] = str(_worker_id)
                if len(_thread_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        running_function(_functions=[_target_producer, _target_consumer])
        EventTestSpec._chk_info(_thread_ids, _thread_flag)


    @staticmethod
    def _async_feature_testing(_lock, running_function, factory=None):

        _async_task_ids = {"producer": "", "consumer": ""}
        _async_task_flag = {"producer": [], "consumer": []}

        async def _target_producer():
            for _ in range(3):
                await asyncio.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _async_task_flag["producer"].append(_thread_index)
                if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                    _async_task_ids["producer"] = str(id(asyncio.current_task()))
                else:
                    _async_task_ids["producer"] = str(id(asyncio.Task.current_task()))
                _lock.set()

        async def _target_consumer():
            while True:
                await _lock.wait()
                _lock.clear()
                _async_task_flag["consumer"].append(float(time.time()))
                _async_task_ids["consumer"] = str(threading.get_ident())
                if len(_async_task_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        running_function(_functions=[_target_producer, _target_consumer], _feature=factory)
        EventTestSpec._chk_info(_async_task_ids, _async_task_flag)


    @staticmethod
    def _chk_info(_thread_ids: dict, _thread_flag: dict):
        assert len(set(_thread_ids.values())) == 2, "The amount of thread ID (de-duplicate) should be equal to amount of functions '2'."
        assert len(_thread_flag["producer"]) == 3, "The amount of producer's flags should be equal to '3'."
        assert len(_thread_flag["consumer"]) == 3, "The amount of consumer's flags should be equal to '3'."

        for _p_index in _thread_flag["producer"]:
            assert _Random_Start_Time <= _p_index <= _Random_End_Time, f"All index of producer set should be in range '{_Random_Start_Time}' and '{_Random_End_Time}'."

        _int_unix_time_timestamps = [int(_v) for _v in _thread_flag["consumer"]]
        _previous_v = None
        for _v in sorted(_int_unix_time_timestamps):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time between them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_thread_flag['consumer']}"
                _previous_v = _v



class ConditionTestSpec(FeatureTestSpec, ABC):

    @abstractmethod
    def test_feature_in_asynchronous_tasks(self, **kwargs):
        pass


    @abstractmethod
    def test_feature_by_pykeyword_with_in_asynchronous_tasks(self, **kwargs):
        pass


    @staticmethod
    def _feature_testing(mode: FeatureMode, _lock, running_function):
        _thread_ids = FeatureTestSpec._get_collection_dict(mode)
        _thread_flag = FeatureTestSpec._get_collection_dict(mode)

        _thread_ids["producer"] = ""
        _thread_ids["consumer"] = ""

        _thread_flag["producer"] = FeatureTestSpec._get_collection_list(mode)
        _thread_flag["consumer"] = FeatureTestSpec._get_collection_list(mode)

        def _target_producer():
            for _ in range(3):
                FeatureTestSpec._sleep(mode)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _thread_flag["producer"].append(_thread_index)
                _worker_id = FeatureTestSpec._get_worker_id(mode)
                _thread_ids["producer"] = str(_worker_id)
                _lock.acquire()
                _lock.notify_all()
                _lock.release()

        def _target_consumer():
            while True:
                _lock.acquire()
                _lock.wait()
                _thread_flag["consumer"].append(float(time.time()))
                _worker_id = FeatureTestSpec._get_worker_id(mode)
                _thread_ids["consumer"] = str(_worker_id)
                _lock.release()
                if len(_thread_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        running_function(_functions=[_target_producer, _target_consumer])
        ConditionTestSpec._chk_info(_thread_ids, _thread_flag)


    @staticmethod
    def _feature_testing_by_pykeyword_with(mode: FeatureMode, _lock, running_function):
        _thread_ids = FeatureTestSpec._get_collection_dict(mode)
        _thread_flag = FeatureTestSpec._get_collection_dict(mode)

        _thread_ids["producer"] = ""
        _thread_ids["consumer"] = ""

        _thread_flag["producer"] = FeatureTestSpec._get_collection_list(mode)
        _thread_flag["consumer"] = FeatureTestSpec._get_collection_list(mode)

        def _target_producer():
            for _ in range(3):
                FeatureTestSpec._sleep(mode)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _thread_flag["producer"].append(_thread_index)
                _worker_id = FeatureTestSpec._get_worker_id(mode)
                _thread_ids["producer"] = str(_worker_id)
                with _lock:
                    _lock.notify_all()

        def _target_consumer():
            while True:
                with _lock:
                    _lock.wait()
                    _thread_flag["consumer"].append(float(time.time()))
                    _worker_id = FeatureTestSpec._get_worker_id(mode)
                    _thread_ids["consumer"] = str(_worker_id)
                    if len(_thread_flag["producer"]) == 3:
                        break

        # # # # Run multiple workers and save something info at the right time
        running_function(_functions=[_target_producer, _target_consumer])
        ConditionTestSpec._chk_info(_thread_ids, _thread_flag)


    @staticmethod
    def _async_feature_testing(_lock, running_function, factory=None):
        _async_task_ids = {"producer": "", "consumer": ""}
        _async_task_flag = {"producer": [], "consumer": []}

        async def _target_producer():
            for _ in range(3):
                await asyncio.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _async_task_flag["producer"].append(_thread_index)
                if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                    _async_task_ids["producer"] = str(id(asyncio.current_task()))
                else:
                    _async_task_ids["producer"] = str(id(asyncio.Task.current_task()))
                await _lock.acquire()
                _lock.notify_all()
                _lock.release()

        async def _target_consumer():
            while True:
                await _lock.acquire()
                await _lock.wait()
                _async_task_flag["consumer"].append(float(time.time()))
                # _async_task_ids["consumer"] = str(threading.get_ident())
                if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                    _async_task_ids["consumer"] = str(id(asyncio.current_task()))
                else:
                    _async_task_ids["consumer"] = str(id(asyncio.Task.current_task()))
                _lock.release()
                if len(_async_task_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        running_function(_functions=[_target_producer, _target_consumer], _feature=factory)
        ConditionTestSpec._chk_info(_async_task_ids, _async_task_flag)


    @staticmethod
    def _async_feature_testing_by_pykeyword_with(_lock, running_function, factory=None):
        _async_task_ids = {"producer": "", "consumer": ""}
        _async_task_flag = {"producer": [], "consumer": []}

        async def _target_producer():
            for _ in range(3):
                await asyncio.sleep(_Sleep_Time)
                _thread_index = random.randrange(_Random_Start_Time, _Random_End_Time)
                _async_task_flag["producer"].append(_thread_index)
                # _async_task_ids["producer"] = str(threading.get_ident())
                if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                    _async_task_ids["producer"] = str(id(asyncio.current_task()))
                else:
                    _async_task_ids["producer"] = str(id(asyncio.Task.current_task()))
                async with _lock:
                    _lock.notify_all()

        async def _target_consumer():
            while True:
                async with _lock:
                    await _lock.wait()
                    _async_task_flag["consumer"].append(float(time.time()))
                    if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) > (3, 6):
                        _async_task_ids["consumer"] = str(id(asyncio.current_task()))
                    else:
                        _async_task_ids["consumer"] = str(id(asyncio.Task.current_task()))
                if len(_async_task_flag["producer"]) == 3:
                    break

        # # # # Run multiple workers and save something info at the right time
        running_function(_functions=[_target_producer, _target_consumer], _feature=factory)
        ConditionTestSpec._chk_info(_async_task_ids, _async_task_flag)


    @staticmethod
    def _chk_info(_thread_ids: dict, _thread_flag: dict):
        assert len(set(_thread_ids.values())) == 2, "The amount of thread ID (de-duplicate) should be equal to amount of functions '2'."
        assert len(_thread_flag["producer"]) == 3, "The amount of producer's flags should be equal to '3'."
        assert len(_thread_flag["consumer"]) == 3, "The amount of consumer's flags should be equal to '3'."

        for _p_index in _thread_flag["producer"]:
            assert _Random_Start_Time <= _p_index <= _Random_End_Time, f"All index of producer set should be in range '{_Random_Start_Time}' and '{_Random_End_Time}'."

        _int_unix_time_timestamps = [int(_v) for _v in _thread_flag["consumer"]]
        _previous_v = None
        for _v in sorted(_int_unix_time_timestamps):
            if _previous_v is None:
                _previous_v = _v
            if _previous_v != _v:
                assert int(abs(float(_v) - float(_previous_v))) == _Sleep_Time, \
                    f"The different time between them should be {_Sleep_Time} second(s). One is {_v} and another one is {_previous_v}. All of them are {_thread_flag['consumer']}"
                _previous_v = _v


