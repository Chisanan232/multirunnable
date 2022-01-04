from multirunnable import PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION

from abc import ABCMeta, abstractmethod
from gevent import sleep as gevent_sleep
from asyncio import sleep as async_sleep, AbstractEventLoop, Future
import logging



class CoroutineWaiter(metaclass=ABCMeta):

    @abstractmethod
    def sleep(self, *args, **kwargs) -> None:
        pass



class GreenThreadWaiter(CoroutineWaiter):

    @staticmethod
    def sleep(seconds: int, ref: bool = True) -> None:
        gevent_sleep(seconds=seconds, ref=ref)



class AsynchronousWaiter(CoroutineWaiter):

    @staticmethod
    async def sleep(delay: float, result=None, loop: AbstractEventLoop = None) -> Future:
        if (PYTHON_MAJOR_VERSION, PYTHON_MINOR_VERSION) >= (3, 10):
            logging.info("Doesn't pass parameter 'loop' to asyncio.sleep.")
            return await async_sleep(delay=delay, result=result)
        return await async_sleep(delay=delay, result=result, loop=loop)

