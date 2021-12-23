from multirunnable.persistence.file.mediator import SavingMediator

import pytest


@pytest.fixture(scope="function")
def saving_mediator() -> SavingMediator:
    return SavingMediator()


class TestSavingMediator:

    def test_worker_id(self, saving_mediator: SavingMediator):
        assert saving_mediator.worker_id is None, f"The default value of SavingMediator.worker_id should be 'None'."

        _test_val = "Thread-1"
        saving_mediator.worker_id = _test_val
        assert saving_mediator.worker_id == "Thread-1", f"The value of SavingMediator.worker_id should be '{_test_val}'."

        del saving_mediator.worker_id
        assert saving_mediator.worker_id is None, f"The value of SavingMediator.worker_id should be deleted."


    @pytest.mark.skip(reason="This feature doesn't support currently. It will be added in v1.16.0 or v1.17.0.")
    def test_is_super_worker(self, saving_mediator: SavingMediator):
        assert saving_mediator.is_super_worker() is True, f"It should be true because it's main thread right now (only one thread currently)."


    def test_super_worker_running(self, saving_mediator: SavingMediator):
        assert saving_mediator.super_worker_running is False, f"The default value of SavingMediator.super_worker_running should be 'False'."

        saving_mediator.super_worker_running = True
        assert saving_mediator.super_worker_running is True, f"The value of SavingMediator.super_worker_running should be 'True'."


    def test_child_worker_running(self, saving_mediator: SavingMediator):
        assert saving_mediator.child_worker_running is False, f"The default value of SavingMediator.child_worker_running should be 'False'."

        saving_mediator.child_worker_running = True
        assert saving_mediator.child_worker_running is True, f"The value of SavingMediator.child_worker_running should be 'True'."


    def test_enable_compress(self, saving_mediator: SavingMediator):
        assert saving_mediator.enable_compress is False, f"The default value of SavingMediator.enable_compress should be 'False'."

        saving_mediator.enable_compress = True
        assert saving_mediator.enable_compress is True, f"The value of SavingMediator.enable_compress should be 'True'."

