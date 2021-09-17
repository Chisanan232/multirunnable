import logging as Ocean_Logging
from multirunnable.logger.config import LogLevel, LoggingConfigDefaultValue, LoggingConfig
from multirunnable.logger.color import TerminalColor
from multirunnable.logger.level import OceanLogger
from multirunnable.logger.kafka import KafkaMsgSenderConfig, KafkaProducerConfig, KafkaHandler
from logging import StreamHandler, FileHandler


# # Initialize Logger configuration
__logging_config = LoggingConfig()
__logging_config.level = LogLevel.DEBUG

# # Initialize Logger handler
sys_stream_hdlr = StreamHandler()
file_io_hdlr = FileHandler(filename="/Users/bryantliu/Downloads/test_new.log")
__producer_config = {"bootstrap_servers": "localhost:9092"}
__sender_config = {"topic": "logging_test", "key": "test"}
# kafka_stream_hdlr = KafkaHandler(producer_configs=__producer_config, sender_configs=__sender_config)

# # Initialize Logger instance
ocean_logger = OceanLogger(config=__logging_config, handlers=[sys_stream_hdlr])
ocean_logger.debug(f"Initialize logging at concurrent.__init__. Level is {__logging_config.level}")

