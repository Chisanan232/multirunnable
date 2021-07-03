from pyocean.framework.operator import RunnableOperator
from pyocean.types import OceanQueue

from typing import Tuple, Dict, Callable



class MultiRunnableOperator(RunnableOperator):

    @classmethod
    def run_with_lock(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Lock

        cls._checking_init(target_obj=Running_Lock)
        with Running_Lock:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def run_with_rlock(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_RLock

        cls._checking_init(target_obj=Running_RLock)
        with Running_RLock:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def run_with_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Semaphore

        cls._checking_init(target_obj=Running_Semaphore)
        with Running_Semaphore:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def run_with_bounded_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Bounded_Semaphore

        cls._checking_init(target_obj=Running_Bounded_Semaphore)
        with Running_Bounded_Semaphore:
            value = function(*arg, **kwarg)
        return value


    @classmethod
    def get_queue(cls) -> OceanQueue:
        from pyocean.framework.strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    def get_one_value_of_queue(cls) -> object:
        from pyocean.framework.strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue.get()



class AsyncRunnableOperator(RunnableOperator):

    @classmethod
    async def run_with_lock(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Lock

        cls._checking_init(target_obj=Running_Lock)
        async with Running_Lock:
            value = await function(*arg, **kwarg)
        return value


    @classmethod
    async def run_with_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Semaphore

        cls._checking_init(target_obj=Running_Semaphore)
        async with Running_Semaphore:
            value = await function(*arg, **kwarg)
        return value


    @classmethod
    async def run_with_bounded_semaphore(cls, function: Callable, arg: Tuple = (), kwarg: Dict = {}) -> object:
        from pyocean.framework.strategy import Running_Bounded_Semaphore

        cls._checking_init(target_obj=Running_Bounded_Semaphore)
        async with Running_Bounded_Semaphore:
            value = await function(*arg, **kwarg)
        return value


    @classmethod
    def get_queue(cls) -> OceanQueue:
        from pyocean.framework.strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return Running_Queue


    @classmethod
    async def get_one_value_of_queue(cls) -> object:
        from pyocean.framework.strategy import Running_Queue

        cls._checking_init(target_obj=Running_Queue)
        return await Running_Queue.get()

