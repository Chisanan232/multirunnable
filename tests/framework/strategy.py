from abc import ABCMeta, abstractmethod



class RunningStrategyTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_initialization(self, **kwargs):
        pass


    @abstractmethod
    def test_close(self, **kwargs):
        pass


    @abstractmethod
    def test_terminal(self, **kwargs):
        pass


    @abstractmethod
    def test_get_result(self, **kwargs):
        pass



class GeneralRunningTestSpec(RunningStrategyTestSpec):

    @abstractmethod
    def test_start_new_worker(self, **kwargs):
        pass


    @abstractmethod
    def test_generate_worker(self, **kwargs):
        pass


    @abstractmethod
    def test_activate_workers(self, **kwargs):
        pass


    @abstractmethod
    def test_kill(self, **kwargs):
        pass



class PoolRunningTestSpec(RunningStrategyTestSpec):

    @abstractmethod
    def test_apply(self, **kwargs):
        pass


    @abstractmethod
    def test_async_apply(self, **kwargs):
        pass


    @abstractmethod
    def test_map(self, **kwargs):
        pass


    @abstractmethod
    def test_async_map(self, **kwargs):
        pass


    @abstractmethod
    def test_map_by_args(self, **kwargs):
        pass


    @abstractmethod
    def test_async_map_by_args(self, **kwargs):
        pass


    @abstractmethod
    def test_imap(self, **kwargs):
        pass


    @abstractmethod
    def test_imap_unordered(self, **kwargs):
        pass


