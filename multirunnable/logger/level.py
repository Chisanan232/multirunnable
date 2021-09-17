from multirunnable.logger import Ocean_Logging
from multirunnable.logger.config import LoggingConfig

from multiprocessing import Lock
# from threading import Lock
from logging import Handler
from typing import List, Union
import logging
import getpass
# import inspect



class OceanLogger:

    __Logger_Instance = None
    __New_Flag: bool = False
    __Lock = Lock()

    __Log_Message_Formatter = f"%(asctime)s - %(threadName)s - %(levelname)s : %(message)s"
    __Logger_Handler: List = []


    def __new__(cls, *args, **kwargs):
        with cls.__Lock:
            import os
            if cls.__Logger_Instance is None:
                print("[DEBUG] new the class Logger. pid: ", os.getpid())
                cls.__Logger_Instance = super(OceanLogger, cls).__new__(cls)
                cls.__New_Flag = True
            else:
                cls.__New_Flag = False
            print("[DEBUG] return class instance. pid: ", os.getpid())

            # # Just for debug
            # curframe = inspect.currentframe()
            # calframe = inspect.getouterframes(curframe, 2)
            # print('caller name:', calframe[1][3])
            # print('caller name - all:', calframe)
            # print('caller name - stack:', inspect.stack()[1][3])

            return cls.__Logger_Instance


    def __init__(self, config: LoggingConfig = LoggingConfig(), handlers: Union[Handler, List[Handler]] = None):
        with self.__Lock:
            if self.__New_Flag is True:
                # Initialize logging
                user = getpass.getuser()
                # self.__logger = logging.getLogger(user)
                self.__logger = Ocean_Logging.getLogger(user)
                self.__logger.setLevel(level=config.level)

                # # Annotate logging handler
                if isinstance(handlers, List) and isinstance(handlers[0], Handler):
                    for __hdlr in handlers:
                        __hdlr.setFormatter(fmt=config.formatter)
                        self.__logger.addHandler(hdlr=__hdlr)
                elif isinstance(handlers, Handler):
                    handlers.setFormatter(fmt=config.formatter)
                    self.__logger.addHandler(hdlr=handlers)
                else:
                    raise TypeError("Parameter 'handlers' should be 'logging.Handler' type or List which saving "
                                    "'logging.Handler' type.")


    def debug(self, msg: str) -> None:
        self.__logger.debug(msg)


    def info(self, msg: str) -> None:
        self.__logger.info(msg)


    def warning(self, msg: str) -> None:
        self.__logger.warning(msg)


    def error(self, msg: str) -> None:
        self.__logger.error(msg)


    def critical(self, msg: str) -> None:
        self.__logger.critical(msg)


    def customize(self, level, msg: str) -> None:
        self.__logger.log(level, msg)


    def set_level(self, level) -> None:
        self.__logger.setLevel(level)


    def disable(self) -> None:
        logging.disable(50)

