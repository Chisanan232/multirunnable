import pathlib
import sys

__package_pyocean = str(pathlib.Path(__file__).parent.parent.parent.absolute())
print("Package path: ", __package_pyocean)
sys.path.append(__package_pyocean)

from multirunnable.logging.level import OceanLogger
from multirunnable.logging.config import LogLevel
from multirunnable.logging.kafka import KafkaProducerConfig, KafkaMsgSenderConfig, KafkaHandler
from multirunnable.logging.config import LoggingConfig

__logging_config = LoggingConfig()


def test_1():
    __logging_config.level = LogLevel.DEBUG
    # sys_stream_hdlr = SysStreamHandler(config=__logging_config)
    # file_hdlr = FileIOHandler(config=__logging_config, file_path="/Users/bryantliu/Downloads/test_new.log")
    # kafka_stream_hdlr = KafkaStreamHandler(config=__logging_config, bootstrap_servers="localhost:9092",
    #                                        topic="logging_test", key="test")
    # test_kafka_handler = kafka_stream_hdlr.generate()
    # __logger = Logger(config=__logging_config, handlers=[sys_stream_hdlr, file_hdlr, kafka_stream_hdlr])
    test_kafka_handler = KafkaHandler(bootstrap_servers="localhost:9092", topic="logging_test", key="test")
    __logger = OceanLogger(config=__logging_config, handlers=test_kafka_handler)
    __logger.info("This is INFO level message.")
    __logger.debug("This is DEBUG level message.")
    __logger.warning("This is WARNING level message.")
    __logger.error("This is ERROR level message.")
    __logger.critical("This is CRITICAL level message.")



def test_2():
    # # Only for testing Kafka features

    # # Method 1-1
    # __kafka_producer_config = KafkaProducerConfig()
    # __kafka_producer_config.update(key="bootstrap_servers", value="localhost:9092")
    # __kafka_msg_sender_config = KafkaMsgSenderConfig()
    # __sender_config = {"topic": "logging_test", "key": "test"}
    # __kafka_msg_sender_config.batch_update(**__sender_config)
    # test_kafka_handler = KafkaHandler(producer_configs=__kafka_producer_config.config,
    #                                   sender_configs=__kafka_msg_sender_config.config)
    # # Method 1-2
    __producer_config = {"bootstrap_servers": "localhost:9092"}
    __sender_config = {"topic": "logging_test", "key": "test"}
    test_kafka_handler = KafkaHandler(producer_configs=__producer_config,
                                      sender_configs=__sender_config)
    test_kafka_handler.setFormatter(fmt=LoggingConfig().formatter)

    # # Method 2
    # test_kafka_handler = KafkaTestHandler(config=LoggingConfig())
    # test_kafka_handler = test_kafka_handler.generate()

    __logger = OceanLogger(config=__logging_config, handlers=test_kafka_handler)
    __logger.info("This is INFO level message.")
    __logger.debug("This is DEBUG level message.")
    __logger.warning("This is WARNING level message.")
    __logger.error("This is ERROR level message.")
    __logger.critical("This is CRITICAL level message.")



if __name__ == '__main__':

    # test_1()
    test_2()
