from pyocean.framework.result import ResultState, OceanResult



class CoroutineResult(OceanResult):
    pass



class AsynchronousResult(OceanResult):

    _Event_Loop = None

    @property
    def event_loop(self) -> str:
        return self._Event_Loop


    @event_loop.setter
    def event_loop(self, event_loop) -> None:
        self._Event_Loop = event_loop

