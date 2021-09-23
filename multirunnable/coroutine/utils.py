from abc import ABCMeta, abstractmethod
import asyncio
import gevent



class CoroutineWaiter(metaclass=ABCMeta):

    @abstractmethod
    def sleep(self, *args, **kwargs) -> None:
        pass



class GreenThreadWaiter(CoroutineWaiter):

    @staticmethod
    def sleep(seconds: int, ref: bool = True) -> None:
        gevent.sleep(seconds=seconds, ref=ref)



class AsynchronousWaiter(CoroutineWaiter):

    @staticmethod
    async def sleep(delay: float, result=None, loop: asyncio.AbstractEventLoop = None) -> asyncio.Future:
        return await asyncio.sleep(delay=delay, result=result, loop=loop)

