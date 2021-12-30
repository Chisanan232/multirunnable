from multirunnable.framework.result import MRResult as _MRResult, PoolResult as _PoolResult

from typing import List, Any



class CoroutineResult(_MRResult):

    _Parent = None
    _Args = None
    _Kwargs = None

    @property
    def parent(self):
        return self._Parent


    @parent.setter
    def parent(self, parent):
        self._Parent = parent


    @property
    def args(self):
        return self._Args


    @args.setter
    def args(self, args):
        self._Args = args


    @property
    def kwargs(self):
        return self._Kwargs


    @kwargs.setter
    def kwargs(self, kwargs):
        self._Kwargs = kwargs



class GreenThreadPoolResult(_PoolResult):
    pass



class AsynchronousResult(_MRResult):

    _Event_Loop = None

    @property
    def event_loop(self) -> str:
        return self._Event_Loop


    @event_loop.setter
    def event_loop(self, event_loop) -> None:
        self._Event_Loop = event_loop

