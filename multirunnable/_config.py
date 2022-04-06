import logging

from .mode import RunningMode as _RunningMode

# # Current Running Mode
RUNNING_MODE: _RunningMode = None


def set_mode(mode: _RunningMode) -> None:
    global RUNNING_MODE
    RUNNING_MODE = mode


def get_current_mode(force: bool = False) -> _RunningMode:
    if RUNNING_MODE is None:
        logging.warning("Current 'RUNNING_MODE' is None.")
        if force is True:
            raise ValueError("Current 'RUNNING_MODE' is None.")
    return RUNNING_MODE

