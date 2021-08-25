from pyocean.framework.task import BaseTask as _BaseTask
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.types import OceanQueue as _OceanQueue
from pyocean.exceptions import GlobalObjectIsNoneError as _GlobalObjectIsNoneError
from pyocean.api.exceptions import QueueNotExistWithName as _QueueNotExistWithName

from functools import wraps
from typing import List, Dict, Callable, Optional, Type, Any, Union



class ReTryMechanism:

    Running_Timeout = 1

    @staticmethod
    def function(function: Callable[[Any, Any], Union[List[Type[_OceanResult]], Exception]]):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def retry(*args, **kwargs) -> Union[List[Type[_OceanResult]], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < ReTryMechanism.Running_Timeout:
                try:
                    ReTryMechanism._initialization(*args, **kwargs)
                    result = function(*args, **kwargs)
                except Exception as e:
                    result = ReTryMechanism._error_handling(e=e)
                else:
                    result = ReTryMechanism._done_handling(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return retry


    @staticmethod
    def async_function(function: Callable):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        async def retry(*args, **kwargs) -> Union[List[Type[_OceanResult]], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < ReTryMechanism.Running_Timeout:
                try:
                    await ReTryMechanism._async_initialization(*args, **kwargs)
                    result = await function(*args, **kwargs)
                except Exception as e:
                    result = await ReTryMechanism._async_error_handling(e=e)
                else:
                    result = await ReTryMechanism._async_done_handling(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return retry


    @staticmethod
    def task(function: Callable[[_BaseTask], Union[List[Type[_OceanResult]], Exception]]):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def task_retry(self, task: _BaseTask) -> Union[List[Type[_OceanResult]], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < task.running_timeout + 1:
                try:
                    task.initialization(*task.init_args, **task.init_kwargs)
                    result = task.function(*task.func_args, **task.func_kwargs)
                except Exception as e:
                    result = task.error_handler(e=e)
                else:
                    result = task.done_handler(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return task_retry


    @staticmethod
    def async_task(function: Callable[[_BaseTask], Union[List[Type[_OceanResult]], Exception]]):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        async def task_retry(self, task: _BaseTask) -> Union[List[Type[_OceanResult]], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < task.running_timeout + 1:
                try:
                    await task.initialization(*task.init_args, **task.init_kwargs)
                    result = await task.function(*task.func_args, **task.func_kwargs)
                except Exception as e:
                    result = await task.error_handler(e=e)
                else:
                    result = await task.done_handler(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return task_retry


    @classmethod
    def _initialization(cls, *args, **kwargs) -> None:
        """
        Description:
            Initial something before run main logic.
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @classmethod
    def _done_handling(cls, result: List[Type[_OceanResult]]) -> List[Type[_OceanResult]]:
        """
        Description:
            Handling the result data after target function running done.
        :param result:
        :return:
        """
        return result


    @classmethod
    def _error_handling(cls, e: Exception) -> Union[List[Type[_OceanResult]], Exception]:
        """
        Description:
            Handling all the error when occur any unexpected error in target function running.
        :param e:
        :return:
        """
        raise e


    @classmethod
    async def _async_initialization(cls, *args, **kwargs) -> None:
        """
        Description:
            Initial something before run main logic.
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @classmethod
    async def _async_done_handling(cls, result: List[Type[_OceanResult]]) -> List[Type[_OceanResult]]:
        """
        Description:
            Handling the result data after target function running done.
        :param result:
        :return:
        """
        return result


    @classmethod
    async def _async_error_handling(cls, e: Exception) -> Union[List[Type[_OceanResult]], Exception]:
        """
        Description:
            Handling all the error when occur any unexpected error in target function running.
        :param e:
        :return:
        """
        raise e



class LockDecorator:

    @staticmethod
    def run_with_lock(function: Callable[[Any, Any], List[Type[_OceanResult]]]):
        """
        Description:
            A decorator which would add lock mechanism around the target
            function for fixed time.
        :return:
        """

        @wraps(function)
        def lock(*args, **kwargs) -> List[Type[_OceanResult]]:
            from pyocean.api.manager import Running_Lock

            with Running_Lock:
                result = function(*args, **kwargs)
            return result

        return lock


    @staticmethod
    def run_with_semaphore(function: Callable[[Any, Any], List[Type[_OceanResult]]]):
        """
        Description:
            A decorator which would add semaphore mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def semaphore(*args, **kwargs) -> List[Type[_OceanResult]]:
            from pyocean.api.manager import Running_Semaphore

            with Running_Semaphore:
                result = function(*args, **kwargs)
            return result

        return semaphore


    @staticmethod
    def run_with_bounded_semaphore(function: Callable[[Any, Any], List[Type[_OceanResult]]]):
        """
        Description:
            A decorator which would add bounded semaphore mechanism
            around the target function for fixed time.
        :return:
        """

        @wraps(function)
        def bounded_semaphore(*args, **kwargs) -> List[Type[_OceanResult]]:
            from pyocean.api.manager import Running_Bounded_Semaphore

            with Running_Bounded_Semaphore:
                result = function(*args, **kwargs)
            return result

        return bounded_semaphore


    @staticmethod
    def async_run_with_lock(function: Callable):
        """
        Description:
            Asynchronous version of run_with_lock.
        :return:
        """

        @wraps(function)
        async def lock(*args, **kwargs) -> List[Type[_OceanResult]]:
            from pyocean.api.manager import Running_Lock

            async with Running_Lock:
                result = await function(*args, **kwargs)
            return result

        return lock


    @staticmethod
    def async_run_with_semaphore(function: Callable):
        """
        Description:
            Asynchronous version of run_with_semaphore.
        :return:
        """

        @wraps(function)
        async def semaphore(*args, **kwargs) -> List[Type[_OceanResult]]:
            from pyocean.api.manager import Running_Semaphore

            async with Running_Semaphore:
                result = await function(*args, **kwargs)
            return result

        return semaphore


    @staticmethod
    def async_run_with_bounded_semaphore(function: Callable):
        """
        Description:
             Asynchronous version of run_with_bounded_semaphore.
       :return:
        """

        @wraps(function)
        async def bounded_semaphore(*args, **kwargs) -> List[Type[_OceanResult]]:
            from pyocean.api.manager import Running_Bounded_Semaphore

            async with Running_Bounded_Semaphore:
                result = await function(*args, **kwargs)
            return result

        return bounded_semaphore



class QueueOperator:

    @classmethod
    def _checking_init(cls, target_obj: object) -> bool:
        if target_obj is None:
            raise _GlobalObjectIsNoneError
        return True


    @classmethod
    def has_queue(cls, name: str):
        from pyocean.api.manager import Running_Queue

        if name in Running_Queue.keys():
            return True
        else:
            return False


    @classmethod
    def get_queue(cls) -> Optional[Dict[str, _OceanQueue]]:
        from pyocean.api.manager import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    def get_queue_with_name(cls, name: str) -> _OceanQueue:
        from pyocean.api.manager import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        if cls.has_queue(name=name):
            return Running_Queue[name]
        else:
            raise _QueueNotExistWithName

