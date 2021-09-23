from multirunnable.mode import RunningMode as _RunningMode

# # Current Running Mode
RUNNING_MODE: _RunningMode


def set_mode(mode: _RunningMode) -> None:
    global RUNNING_MODE
    RUNNING_MODE = mode


def get_current_mode() -> _RunningMode:
    return RUNNING_MODE

