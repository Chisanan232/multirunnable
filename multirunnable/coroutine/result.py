from multirunnable.framework.result import MRResult as _MRResult



class CoroutineResult(_MRResult):
    pass



class AsynchronousResult(_MRResult):

    _Event_Loop = None

    @property
    def event_loop(self) -> str:
        return self._Event_Loop


    @event_loop.setter
    def event_loop(self, event_loop) -> None:
        self._Event_Loop = event_loop

