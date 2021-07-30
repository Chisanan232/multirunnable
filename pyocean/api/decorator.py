from pyocean.framework.worker import BaseTask
from pyocean.framework.result import OceanResult

from functools import wraps
from typing import List, Callable, Any, Union



class ReTryMechanism:

    Running_Timeout = 1

    def function(function: Callable):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def retry(*args, **kwargs) -> Union[List[OceanResult], Exception]:
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


    def async_function(function: Callable):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        async def retry(*args, **kwargs) -> Union[List[OceanResult], Exception]:
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


    def task(function: Callable):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def task_retry(self, task: BaseTask) -> Union[List[OceanResult], Exception]:
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


    def async_task(function: Callable):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        async def task_retry(self, task: BaseTask) -> Union[List[OceanResult], Exception]:
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
    def _done_handling(cls, result: List[OceanResult]) -> List[OceanResult]:
        """
        Description:
            Handling the result data after target function running done.
        :param result:
        :return:
        """
        return result


    @classmethod
    def _error_handling(cls, e: Exception) -> Union[List[OceanResult], Exception]:
        """
        Description:
            Handling all the error when occur any unexpected error in target function running.
        :param e:
        :return:
        """
        return e


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
    async def _async_done_handling(cls, result: List[OceanResult]) -> List[OceanResult]:
        """
        Description:
            Handling the result data after target function running done.
        :param result:
        :return:
        """
        return result


    @classmethod
    async def _async_error_handling(cls, e: Exception) -> Union[List[OceanResult], Exception]:
        """
        Description:
            Handling all the error when occur any unexpected error in target function running.
        :param e:
        :return:
        """
        return e



class LockDecorator:

    def run_with_lock(function: Callable):
        """
        Description:
            A decorator which would add lock mechanism around the target
            function for fixed time.
        :return:
        """

        @wraps(function)
        def lock(*args, **kwargs) -> List[OceanResult]:
            from pyocean.framework.strategy import Running_Lock

            with Running_Lock:
                result = function(*args, **kwargs)
            return result

        return lock


    def run_with_semaphore(function: Callable):
        """
        Description:
            A decorator which would add semaphore mechanism around the
            target function for fixed time.
        :return:
        """

        @wraps(function)
        def semaphore(*args, **kwargs) -> List[OceanResult]:
            from pyocean.framework.strategy import Running_Semaphore

            with Running_Semaphore:
                result = function(*args, **kwargs)
            return result

        return semaphore


    def run_with_bounded_semaphore(function: Callable):
        """
        Description:
            A decorator which would add bounded semaphore mechanism
            around the target function for fixed time.
        :return:
        """

        @wraps(function)
        def bounded_semaphore(*args, **kwargs) -> List[OceanResult]:
            from pyocean.framework.strategy import Running_Bounded_Semaphore

            with Running_Bounded_Semaphore:
                result = function(*args, **kwargs)
            return result

        return bounded_semaphore

