from logging import Formatter
from typing import Dict
from enum import Enum
import logging



class LogLevel(Enum):

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL



class LoggingConfigDefaultValue(Enum):

    Formatter: Formatter = Formatter(f"%(asctime)s - %(threadName)s - %(levelname)s : %(message)s")
    Log_Level = LogLevel.DEBUG.value



class LoggingConfig:

    _Logging_Config: Dict[str, object] = {}

    @property
    def formatter(self) -> Formatter:
        return self._Logging_Config.get("formatter", LoggingConfigDefaultValue.Formatter.value)


    @formatter.setter
    def formatter(self, fmt: str) -> None:
        self._Logging_Config["formatter"] = Formatter(fmt)


    @property
    def level(self):
        return self._Logging_Config.get("level", LoggingConfigDefaultValue.Log_Level.value)


    @level.setter
    def level(self, level: LogLevel) -> None:
        print("[DEBUG] the logging level is: ", level)
        # # # Just for debug
        # import inspect
        # curframe = inspect.currentframe()
        # calframe = inspect.getouterframes(curframe, 2)
        # print('caller name:', calframe[1][3])
        # print('caller name - all:', calframe)
        # print('caller name - stack:', inspect.stack()[1][3])
        self._Logging_Config["level"] = level.value

