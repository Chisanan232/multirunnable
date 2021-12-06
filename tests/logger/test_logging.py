import pathlib
import sys

__package_pyocean = str(pathlib.Path(__file__).parent.parent.parent.absolute())
print("Package path: ", __package_pyocean)
sys.path.append(__package_pyocean)

from multirunnable.logging.level import Logger, LogLevel
# from pyocean.logging.handler import LoggingHandler, SysStreamHandler, FileIOHandler, KafkaStreamHandler, KafkaHandler
from multirunnable.logging.handler import KafkaHandler
from multirunnable.logging.config import LoggingConfig
import logging



class InfoLog:

    def __init__(self, logger: Logger):
        self.__logger = logger
        print("New class 'InfoLog'")


    def print_msg(self, msg: str):
        self.__logger.info(msg)



class DebugLog:

    def __init__(self, logger: Logger):
        self.__logger = logger
        print("New class 'DebugLog'")


    def print_msg(self, msg: str):
        self.__logger.debug(msg)



class LogObj:

    def __init__(self, logger: Logger):
        self.__logger = logger
        print("New class 'LogObj'")


    def main_run(self):
        __debug = DebugLog(logger=self.__logger)
        __info = InfoLog(logger=self.__logger)
        __debug.print_msg("This is debug level message.")
        __info.print_msg("This is info level message.")
        self.__logger.warning("This is warning level message.")
        self.__logger.error("This is error level message.")
        self.__logger.critical("This is critical level message.")



if __name__ == '__main__':

    config = LoggingConfig()
    print("[DEBUG] logging config: ", config)
    logger_instance = Logger(config=config,
                             handlers=[logging.FileHandler(filename="/Users/bryantliu/Downloads/for_testing.log"),
                                       logging.StreamHandler(),
                                       KafkaHandler(bootstrap_servers="localhost:9092", topic="logging_test", key="test")])
    log_obj = LogObj(logger=logger_instance)
    log_obj.main_run()
