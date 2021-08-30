from abc import ABCMeta, abstractmethod



class AdapterOperator(metaclass=ABCMeta):

    pass



class BaseLockAdapterOperator(AdapterOperator):

    def __init__(self, *args, **kwargs):
        self._feature_instance = self._get_feature_instance()


    def __repr__(self):
        pass


    def __enter__(self):
        self._feature_instance.__enter__()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._feature_instance.__exit__(exc_type, exc_val, exc_tb)

    # # # # Error records:
    # # # # Parallel - multiprocessing
    # File "/.../apache-pyocean/pyocean/api/operator.py", line 118, in __exit__
    #     self.__bounded_semaphore.__exit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)
    # TypeError: __exit__() got an unexpected keyword argument 'exc_type'

    # # # # Concurrent - threading
    #   File "/apache-pyocean/pyocean/concurrent/strategy.py", line 52, in save_value_fun
    #     value = task.function(*task.func_args, **task.func_kwargs)
    #   File "/apache-pyocean/example/persistence_file/dao.py", line 33, in get_test_data
    #     data = self.sql_process_many()
    #   File "/apache-pyocean/pyocean/api/decorator.py", line 668, in __bounded_semaphore_process
    #     result = function(*args, **kwargs)
    #   File "/apache-pyocean/pyocean/api/operator.py", line 190, in __exit__
    #     self.__bounded_semaphore.__exit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)
    #  TypeError: __exit__() got an unexpected keyword argument 'exc_type'

    # # # # Green Thread - gevent
    #   File "/apache-pyocean/pyocean/api/decorator.py", line 104, in task_retry
    #     result = task.error_handler(e=e)
    #   File "/apache-pyocean/pyocean/framework/task.py", line 31, in error_handler
    #     raise e
    #   File "/apache-pyocean/pyocean/api/decorator.py", line 102, in task_retry
    #     result = task.function(*task.func_args, **task.func_kwargs)
    #   File "/apache-pyocean/example/persistence_file/dao.py", line 33, in get_test_data
    #     data = self.sql_process_many()
    #   File "/apache-pyocean/pyocean/api/decorator.py", line 668, in __bounded_semaphore_process
    #     result = function(*args, **kwargs)
    #   File "/apache-pyocean/pyocean/api/operator.py", line 201, in __exit__
    #     self.__bounded_semaphore.__exit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)
    #   File "src/gevent/_semaphore.py", line 144, in gevent.__semaphore.Semaphore.__exit__
    # TypeError: __exit__() takes exactly 3 positional arguments (0 given)


    @abstractmethod
    def _get_feature_instance(self):
        pass


    @abstractmethod
    def acquire(self, *args, **kwargs) -> None:
        pass


    @abstractmethod
    def release(self, *args, **kwargs) -> None:
        pass



class _AsyncContextManager:

    def __init__(self, lock):
        self._lock = lock


    def __enter__(self):
        return None


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()



class AsyncAdapterOperator(metaclass=ABCMeta):

    def __enter__(self):
        raise RuntimeError("")


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass




class BaseAsyncLockAdapterOperator(AsyncAdapterOperator):

    def __init__(self, *args, **kwargs):
        self._feature_instance = self._get_feature_instance()


    def __repr__(self):
        pass


    def __await__(self):
        return self.__acquire_ctx().__await__()


    async def __aenter__(self):
        await self._feature_instance.__aenter__()
        return None


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._feature_instance.__aexit__(exc_type, exc_val, exc_tb)


    async def __acquire_ctx(self):
        await self.acquire()
        return _AsyncContextManager(self)


    @abstractmethod
    def _get_feature_instance(self):
        pass


    @abstractmethod
    async def acquire(self, *args, **kwargs) -> None:
        pass


    @abstractmethod
    def release(self, *args, **kwargs) -> None:
        pass

