from multirunnable.framework.result import OceanResult as _OceanResult



class CoroutineResult(_OceanResult):
    pass



class AsynchronousResult(_OceanResult):

    _Event_Loop = None

    @property
    def event_loop(self) -> str:
        return self._Event_Loop


    @event_loop.setter
    def event_loop(self, event_loop) -> None:
        self._Event_Loop = event_loop

