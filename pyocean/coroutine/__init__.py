from pyocean.coroutine.features import (
    GeventQueueType, GreenletLock, GreenletCommunication,
    AsynchronousQueueType, AsyncLock, AsyncCommunication)
from pyocean.coroutine.strategy import MultiGreenletStrategy, AsynchronousStrategy
from pyocean.coroutine.result import CoroutineResult, AsynchronousResult
