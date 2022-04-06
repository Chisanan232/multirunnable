from typing import List, Any

from multirunnable import set_mode
from multirunnable.adapter.context import context as adapter_context
from multirunnable.framework.runnable.context import BaseContext
from multirunnable.persistence.file.mediator import SavingMediator

from tests.test_config import Under_Test_RunningModes, Under_Test_RunningModes_Without_Greenlet

import pytest


class _TestingMediator(BaseContext):

    @staticmethod
    def get_current_worker() -> Any:
        return "ExampleWorker"


    @staticmethod
    def get_parent_worker() -> Any:
        return "ParentExampleWorker"


    @staticmethod
    def current_worker_is_parent() -> bool:
        return False


    @staticmethod
    def get_current_worker_ident() -> str:
        return "123456789"


    @staticmethod
    def get_current_worker_name() -> str:
        return "ExampleWorker"


    @staticmethod
    def current_worker_is_alive() -> bool:
        return True


    @staticmethod
    def active_workers_count() -> int:
        return 1


    @staticmethod
    def children_workers() -> List[Any]:
        return ["Children"]



@pytest.fixture(scope="function")
def saving_mediator(request) -> SavingMediator:
    set_mode(mode=request.param)
    return SavingMediator()


class TestSavingMediator:

    def test_instantiate_without_running_mode(self):
        try:
            set_mode(mode=None)
            SavingMediator()
        except ValueError as ve:
            assert "The RunningMode in context cannot be None object if option *context* is None" in str(ve), "It should raise an exception about RunningMode cannot be None if its option *context* is None."
        else:
            assert False, "It should raise an exception about RunningMode cannot be None if its option *context* is None."


    def test_instantiate_with_customized_mediator(self):
        _tm = _TestingMediator()
        _sm = SavingMediator(context=_tm)
        assert _sm.is_super_worker() == _tm.current_worker_is_parent(), "The checksum between context and mediator should be the same."


    @pytest.mark.parametrize(
        argnames="saving_mediator",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_worker_id(self, saving_mediator: SavingMediator):
        assert saving_mediator.worker_id is None, "The default value of SavingMediator.worker_id should be 'None'."

        _test_worker_id = adapter_context.get_current_worker_ident()
        # _test_val = "Thread-1"
        saving_mediator.worker_id = _test_worker_id
        assert saving_mediator.worker_id == _test_worker_id, f"The value of SavingMediator.worker_id should be '{_test_worker_id}'."

        del saving_mediator.worker_id
        assert saving_mediator.worker_id is None, "The value of SavingMediator.worker_id should be deleted."


    @pytest.mark.parametrize(
        argnames="saving_mediator",
        argvalues=Under_Test_RunningModes_Without_Greenlet,
        indirect=True
    )
    def test_activate_count(self, saving_mediator: SavingMediator):
        assert saving_mediator.activate_count == adapter_context.active_workers_count(), "The count value of activate workers should be same as get the value from context."


    @pytest.mark.parametrize(
        argnames="saving_mediator",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_is_super_worker(self, saving_mediator: SavingMediator):
        assert saving_mediator.is_super_worker() is True, "It should be true because it's main thread right now (only one thread currently)."


    @pytest.mark.parametrize(
        argnames="saving_mediator",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_super_worker_running(self, saving_mediator: SavingMediator):
        assert saving_mediator.super_worker_running is False, "The default value of SavingMediator.super_worker_running should be 'False'."

        saving_mediator.super_worker_running = True
        assert saving_mediator.super_worker_running is True, "The value of SavingMediator.super_worker_running should be 'True'."


    @pytest.mark.parametrize(
        argnames="saving_mediator",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_child_worker_running(self, saving_mediator: SavingMediator):
        assert saving_mediator.child_worker_running is False, "The default value of SavingMediator.child_worker_running should be 'False'."

        saving_mediator.child_worker_running = True
        assert saving_mediator.child_worker_running is True, "The value of SavingMediator.child_worker_running should be 'True'."


    @pytest.mark.parametrize(
        argnames="saving_mediator",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_enable_compress(self, saving_mediator: SavingMediator):
        assert saving_mediator.enable_compress is False, "The default value of SavingMediator.enable_compress should be 'False'."

        saving_mediator.enable_compress = True
        assert saving_mediator.enable_compress is True, "The value of SavingMediator.enable_compress should be 'True'."

