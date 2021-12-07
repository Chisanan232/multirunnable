from multirunnable.mode import RunningMode as _RunningMode
import logging

# # Current Running Mode
RUNNING_MODE: _RunningMode


def set_mode(mode: _RunningMode) -> None:
    global RUNNING_MODE
    RUNNING_MODE = mode


def get_current_mode(force: bool = False) -> _RunningMode:
    if RUNNING_MODE is None:
        logging.warning(f"Current 'RUNNING_MODE' is None.")
        if force is True:
            raise ValueError("Current 'RUNNING_MODE' is None.")
    return RUNNING_MODE

