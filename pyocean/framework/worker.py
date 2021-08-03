from pyocean.framework.result import OceanResult
from pyocean.api.mode import RunningMode, FeatureMode

from abc import ABCMeta, ABC, abstractmethod
from typing import List, Tuple, Dict, Callable, Union



class BaseTaskFunction:

    @classmethod
    def function(cls, *args, **kwargs) -> List[OceanResult]:
        pass


    @classmethod
    def initialization(cls, *args, **kwargs) -> None:
        pass


    @classmethod
    def done_handler(cls, result: List[OceanResult]) -> List[OceanResult]:
        return result


    @classmethod
    def error_handler(cls, e: Exception) -> Union[List[OceanResult], Exception]:
        raise e



class BaseTaskAsyncFunction:

    @classmethod
    async def function(cls, *args, **kwargs) -> List[OceanResult]:
        pass


    @classmethod
    async def initialization(cls, *args, **kwargs) -> None:
        pass


    @classmethod
    async def done_handler(cls, result: List[OceanResult]) -> List[OceanResult]:
        return result


    @classmethod
    async def error_handler(cls, e: Exception) -> Union[List[OceanResult], Exception]:
        raise e



class BaseTask(metaclass=ABCMeta):

    _Group = None
    _Function = None
    _Fun_Args = ()
    _Fun_Kwargs = {}
    _Initialization = None
    _Init_Args = ()
    _Init_Kwargs = {}
    _Done_Handler = None
    _Error_Handler = None
    _Running_Timeout = 0

    def __init__(self, mode: RunningMode):
        if mode is RunningMode.Asynchronous:
            self._Function = BaseTaskAsyncFunction.function
            self._Initialization = BaseTaskAsyncFunction.initialization
            self._Done_Handler = BaseTaskAsyncFunction.done_handler
            self._Error_Handler = BaseTaskAsyncFunction.error_handler
        else:
            self._Function = BaseTaskFunction.function
            self._Initialization = BaseTaskFunction.initialization
            self._Done_Handler = BaseTaskFunction.done_handler
            self._Error_Handler = BaseTaskFunction.error_handler


    @property
    @abstractmethod
    def function(self) -> Callable:
        pass


    @abstractmethod
    def set_function(self, function: Callable):
        pass


    @property
    @abstractmethod
    def func_args(self) -> Tuple:
        pass


    @abstractmethod
    def set_func_args(self, args: Tuple):
        pass


    @property
    @abstractmethod
    def func_kwargs(self) -> Dict:
        pass


    @abstractmethod
    def set_func_kwargs(self, kwargs: Dict):
        pass


    @property
    @abstractmethod
    def initialization(self) -> Callable:
        pass


    @abstractmethod
    def set_initialization(self, init: Callable):
        pass


    @property
    @abstractmethod
    def init_args(self) -> Tuple:
        pass


    @abstractmethod
    def set_init_args(self, args: Tuple):
        pass


    @property
    @abstractmethod
    def init_kwargs(self) -> Dict:
        pass


    @abstractmethod
    def set_init_kwargs(self, kwargs: Dict):
        pass


    @property
    @abstractmethod
    def group(self) -> str:
        pass


    @abstractmethod
    def set_group(self, group: str):
        pass


    @property
    @abstractmethod
    def done_handler(self) -> Callable:
        pass


    @abstractmethod
    def set_done_handler(self, hdlr: Callable):
        pass


    @property
    @abstractmethod
    def error_handler(self) -> Callable:
        pass


    @abstractmethod
    def set_error_handler(self, hdlr: Callable):
        pass


    @property
    @abstractmethod
    def running_timeout(self) -> int:
        pass


    @abstractmethod
    def set_running_timeout(self, timeout: int):
        pass



class BaseWorker(metaclass=ABCMeta):

    _Worker_Timeout = 3

    @property
    @abstractmethod
    def running_timeout(self) -> int:
        pass


    @running_timeout.setter
    @abstractmethod
    def running_timeout(self, timeout: int) -> None:
        pass


    @abstractmethod
    def _initial_running_strategy(self) -> None:
        pass


    @abstractmethod
    def start(self, task: BaseTask, saving_mode: bool = False,
              init_args: Tuple = (), init_kwargs: Dict = {}, features: List = []) -> None:
        pass


    @abstractmethod
    def pre_activate(self, *args, **kwargs) -> None:
        pass


    @abstractmethod
    def activate(self, task: BaseTask, saving_mode: bool = False) -> None:
        pass


    @abstractmethod
    def run_task(self, task: BaseTask) -> List[OceanResult]:
        pass


    @abstractmethod
    def pre_stop(self, e: Exception) -> None:
        pass


    @abstractmethod
    def post_stop(self) -> None:
        pass


    @abstractmethod
    def post_done(self) -> None:
        pass


    @abstractmethod
    def get_result(self) -> List[OceanResult]:
        pass



class BaseAsyncWorker(BaseWorker):

    @abstractmethod
    async def start(self, task: BaseTask, saving_mode: bool = False,
                    init_args: Tuple = (), init_kwargs: Dict = {}, features: List = []) -> None:
        pass


    @abstractmethod
    async def pre_activate(self, *args, **kwargs) -> None:
        pass


    @abstractmethod
    async def activate(self, task: BaseTask, saving_mode: bool = False) -> None:
        pass


    @abstractmethod
    async def run_task(self, task: BaseTask) -> List[OceanResult]:
        pass



class BaseSystem(metaclass=ABCMeta):

    def __init__(self, mode: RunningMode, worker_num: int):
        self._mode = mode
        self._worker_num = worker_num


    @abstractmethod
    def run(self, task: BaseTask):
        pass


    @abstractmethod
    def dispatcher(self):
        pass


    @abstractmethod
    def terminate(self):
        pass

