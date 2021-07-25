from pyocean.framework.worker import BaseTask
from pyocean.framework.result import OceanResult

from typing import List, Callable, Any, Union



class ReTryDecorator:

    Running_Timeout = 1

    def retry_mechanism(function: Callable):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        def retry(*args, **kwargs) -> Union[List[OceanResult], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < ReTryDecorator.Running_Timeout:
                try:
                    result = function(*args, **kwargs)
                except Exception as e:
                    result = ReTryDecorator._error_handling(e=e)
                else:
                    result = ReTryDecorator._done_handling(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return retry


    def task_retry_mechanism(function: Callable):
        """
        Description:
            A decorator which would add re-try mechanism around the
            target function for fixed time.
        :return:
        """

        def retry(task: BaseTask) -> Union[List[OceanResult], Exception]:
            result = None

            __fun_run_time = 0

            while __fun_run_time < task.running_timeout:
                try:
                    task.initialization(*task.init_args, **task.init_kwargs)
                    result = function(*task.func_args, **task.func_kwargs)
                except Exception as e:
                    result = task.error_handler(e=e)
                else:
                    result = task.done_handler(result=result)
                    return result
                finally:
                    __fun_run_time += 1
            else:
                return result

        return retry


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



class LockDecorator:

    def run_with_lock(function: Callable):
        """
        Description:
            A decorator which would add lock mechanism around the target
            function for fixed time.
        :return:
        """

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

        def bounded_semaphore(*args, **kwargs) -> List[OceanResult]:
            from pyocean.framework.strategy import Running_Bounded_Semaphore

            with Running_Bounded_Semaphore:
                result = function(*args, **kwargs)
            return result

        return bounded_semaphore

