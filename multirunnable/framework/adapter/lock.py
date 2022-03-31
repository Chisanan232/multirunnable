from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Union

from ..api.operator import _AsyncContextManager
from ..api import BaseLockAdapterOperator, BaseAsyncLockAdapterOperator
from ..factory import BaseFeatureAdapterFactory
from ...types import MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition
from ...mode import RunningMode, FeatureMode
from ..._config import get_current_mode



class BaseFeatureAdapter(metaclass=ABCMeta):

    _Feature_Factory_Inst: BaseFeatureAdapterFactory = None
    _Feature_Operator_Inst: Union[BaseLockAdapterOperator, BaseAsyncLockAdapterOperator] = None


    def __init__(self, mode: Union[RunningMode, FeatureMode] = None, init: bool = False, **kwargs):
        self._run_init_flag = init
        self._feature_mode = mode
        self._lock_params = kwargs

        if self._feature_mode is None:
            _current_running_mode = get_current_mode(force=True)
            self._feature_mode = _current_running_mode.value["feature"]
        else:
            if isinstance(self._feature_mode, RunningMode) is False and \
                    isinstance(self._feature_mode, FeatureMode) is False:
                raise TypeError("The *feature_mode* type is invalid. It should be one of enum object *multirunnable.mode.FeatureMode*.")

        if isinstance(self._feature_mode, RunningMode) is True:
            self._feature_mode = self._feature_mode.value["feature"]

        self._feature_factory.feature_mode = self._feature_mode
        if self._run_init_flag is True:
            self.initial()


    def initial(self):
        """
        Description:
            Instantiate the object and globalize it.
        :return:
        """
        __instance = self._feature_factory.get_instance(**self._lock_params)
        self._feature_factory.globalize_instance(__instance)


    @property
    def _feature_factory(self) -> BaseFeatureAdapterFactory:
        """
        Description:
            The APIs generating instance with RunningMode.
        :return:
        """
        if self._Feature_Factory_Inst is None:
            self._Feature_Factory_Inst = self._instantiate_factory()
        return self._Feature_Factory_Inst


    @property
    def _feature_operator(self) -> Union[BaseLockAdapterOperator, BaseAsyncLockAdapterOperator]:
        """
        Description:
            The APIs operating instance from factory *_feature_factory*.
        :return:
        """
        if self._Feature_Operator_Inst is None:
            self._Feature_Operator_Inst = self._instantiate_operator()
        return self._Feature_Operator_Inst


    @abstractmethod
    def _instantiate_factory(self) -> BaseFeatureAdapterFactory:
        """
        Description:
            The reality implementation returns the instance of Feature Factory.
        :return:
        """
        pass


    @abstractmethod
    def _instantiate_operator(self) -> Union[BaseLockAdapterOperator, BaseAsyncLockAdapterOperator]:
        """
        Description:
            The reality implementation returns the instance of Operators Factory.
        :return:
        """
        pass


    @abstractmethod
    def get_instance(self, **kwargs) -> Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]:
        """
        Description:
            Return the instance by RunningMode. For example, it would
            return *threading.Lock* instance if RunningMode is Concurrent.
        :return:
        """
        pass


    @abstractmethod
    def globalize_instance(self, obj: Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]) -> None:
        """
        Description:
            Globalize the object in package MultiRunnable.
        :param obj:
        :return:
        """
        pass



class BaseLockAdapter(BaseFeatureAdapter):

    def __init__(self, mode: Union[RunningMode, FeatureMode] = None, init: bool = False, **kwargs):
        if mode is not None and (mode is RunningMode.Asynchronous or mode is FeatureMode.Asynchronous):
            raise TypeError(f"This object {__class__} doesn't receive Asynchronous mode.")
        super().__init__(mode=mode, init=init, **kwargs)


    def __repr__(self):
        return f"<{self.__class__} object as Adapter with {self._feature_mode} mode at {id(self)}>"


    def __enter__(self):
        """
        Description:
            Support the instance to use with Python keyword 'with'.

        Example:
            import multirunnable.adapter import Lock

            _lock = Lock()
            with _lock:
                print('Do something here with Lock')

        :return:
        """
        self._feature_operator.__enter__()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._feature_operator.__exit__(exc_type, exc_val, exc_tb)


    def get_instance(self) -> Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]:
        return self._feature_factory.get_instance()


    def globalize_instance(self, obj: Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]) -> None:
        self._feature_factory.globalize_instance(obj=obj)


    @abstractmethod
    def acquire(self, **kwargs) -> None:
        pass


    @abstractmethod
    def release(self, **kwargs) -> None:
        pass



class BaseCommunicationAdapter(BaseFeatureAdapter):

    def __init__(self, mode: Union[RunningMode, FeatureMode] = None, init: bool = False, **kwargs):
        if mode is not None and (mode is RunningMode.Asynchronous or mode is FeatureMode.Asynchronous):
            raise TypeError(f"This object {__class__} doesn't receive Asynchronous mode.")
        super().__init__(mode=mode, init=init, **kwargs)


    def __repr__(self):
        return f"<{self.__class__} object as Adapter with {self._feature_mode} mode at {id(self)}>"


    def get_instance(self) -> Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]:
        return self._feature_factory.get_instance()


    def globalize_instance(self, obj: Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]) -> None:
        self._feature_factory.globalize_instance(obj=obj)


    @abstractmethod
    def wait(self, **kwargs) -> Optional[Any]:
        pass



class BaseAsyncLockAdapter(BaseFeatureAdapter):

    def __init__(self, mode: Union[RunningMode, FeatureMode] = None, init: bool = False, **kwargs):
        if mode is not None and (mode is not RunningMode.Asynchronous and mode is not FeatureMode.Asynchronous):
            raise TypeError(f"This object {__class__} only receives Asynchronous mode.")
        super().__init__(mode=mode, init=init, **kwargs)


    def __repr__(self):
        return f"<{self.__class__} object as Adapter with {self._feature_mode} mode at {id(self)}>"


    def __await__(self):
        return self._feature_operator.__await__()


    async def __aenter__(self):
        return await self._feature_operator.__aenter__()


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._feature_operator.__aexit__(exc_type, exc_val, exc_tb)


    async def __acquire_ctx(self):
        await self.acquire()
        return _AsyncContextManager(self)


    def get_instance(self, **kwargs) -> Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]:
        return self._feature_factory.get_instance(**kwargs)


    def globalize_instance(self, obj: Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]) -> None:
        self._feature_factory.globalize_instance(obj=obj)


    @abstractmethod
    async def acquire(self, **kwargs) -> None:
        pass


    @abstractmethod
    def release(self, **kwargs) -> None:
        pass



class BaseAsyncCommunicationAdapter(BaseFeatureAdapter):

    def __init__(self, mode: Union[RunningMode, FeatureMode] = None, init: bool = False, **kwargs):
        if mode is not None and (mode is not RunningMode.Asynchronous and mode is not FeatureMode.Asynchronous):
            raise TypeError(f"This object {__class__} only receives Asynchronous mode.")
        super().__init__(mode=mode, init=init, **kwargs)


    def __repr__(self):
        return f"<{self.__class__} object as Adapter with {self._feature_mode} mode at {id(self)}>"


    def get_instance(self, **kwargs) -> Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]:
        return self._feature_factory.get_instance(**kwargs)


    def globalize_instance(self, obj: Union[MRLock, MRRLock, MRSemaphore, MRBoundedSemaphore, MREvent, MRCondition]) -> None:
        self._feature_factory.globalize_instance(obj=obj)


    @abstractmethod
    async def wait(self, **kwargs) -> None:
        pass


