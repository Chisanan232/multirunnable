from multirunnable.mode import RunningMode
from multirunnable._config import set_mode, get_current_mode

import traceback
import pytest



class TestConfig:

    def test_get_current_mode(self):
        _mode = get_current_mode()
        assert _mode is None, "The value which be get via method 'get_current_mode' should be None because we doesn't set the RunningMode currently."

        _mode = get_current_mode(force=False)
        assert _mode is None, "The value which be get via method 'get_current_mode' should be None because we doesn't set the RunningMode currently."


    def test_get_current_mode_with_force(self):
        try:
            _mode = get_current_mode(force=True)
        except ValueError as ve:
            assert str(ve) == "Current 'RUNNING_MODE' is None.", "The error message should tell developers the 'Running_Mode' is None currently."
        except Exception:
            assert False, f"It occur something unexpected error. Please check it. Error: {traceback.format_exc()}"
        else:
            assert False, "It should raise 'ValueError' if option *force* is True."


    @pytest.mark.parametrize("mode", [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread, RunningMode.Asynchronous])
    def test_set(self, mode):
        set_mode(mode=mode)
        _mode = get_current_mode()
        assert _mode is mode, "The mode we got should be the same as we set."

        try:
            _mode = get_current_mode()
        except Exception:
            assert False, f"It shouldn't occur any error when we try to get mode. Error: {traceback.format_exc()}"
        else:
            assert _mode is mode, "The mode we got should be the same as we set."

