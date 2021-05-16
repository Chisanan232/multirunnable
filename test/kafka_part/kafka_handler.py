from typing import Any
from kafka import KafkaClient, KafkaProducer
import logging
import getpass
import sys



class KafkaHandler(logging.Handler):

    def __init__(self, bootstrap_servers: str, topic: str, key: str = None, partition: Any = None, headers: Any = None, timestamp_ms: Any = None):
        super().__init__()
        # KafkaClient()
        self.__producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.__topic = topic
        self.__key = key
        self.__partition = partition
        self.__headers = headers
        self.__timestamp_ms = timestamp_ms


    def emit(self, record):
        # drop kafka logging to avoid infinite recursion
        # if record.name == 'kafka':
        #     return
        # try:

        # use default formatting
        msg = self.format(record)
        # produce message
        print("[DEBUG] msg: ", msg)
        # self.__producer.send(topic=self.__topic, key=bytes(self.__key.encode("utf-8")), value=bytes(msg.encode("utf-8")))

        # sender = self.__producer.send(topic=self.__topic, key=bytes(self.__key.encode("utf-8")), value=bytes(msg.encode("utf-8")))
        sender = self.__producer.send(topic=self.__topic,
                                      key=bytes(self.__key.encode("utf-8")),
                                      partition=self.__partition,
                                      value=bytes(msg.encode("utf-8")),
                                      headers=self.__headers,
                                      timestamp_ms=self.__timestamp_ms)
        sender.get()
        # val = sender.value
        # args = sender.args
        # success = sender.succeeded()
        # fail = sender.failed()
        # exception = sender.exception
        # is_done = sender.is_done
        # retriable = sender.retriable()
        # print(f"[DEBUG] sender.value: {val}")
        # print(f"[DEBUG] sender.args: {args}")
        # print(f"[DEBUG] sender.success: {success}")
        # print(f"[DEBUG] sender.fail: {fail}")
        # print(f"[DEBUG] sender.exception: {exception}")
        # print(f"[DEBUG] sender.is_done: {is_done}")
        # print(f"[DEBUG] sender.retriable: {retriable}")

        # self.__producer.send(self.__topic, bytes(msg.encode("utf-8")))
        # self.__producer.send(topic=self.__topic, value=msg.encode("utf-8"))

        # except:
        #     print("[DEBUG] error handle ...")
        #     import traceback
        #     ei = sys.exc_info()
        #     traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
        #     del ei


    def close(self):
        print("[DEBUG] close Kafka logging streaming ")
        self.__producer.close()
        logging.Handler.close(self)



if __name__ == '__main__':

    kafka_handler = KafkaHandler(bootstrap_servers="localhost:9092", topic="logging_test", key="test")
    kafka_handler.setFormatter(logging.Formatter(f"%(asctime)s - %(threadName)s - %(levelname)s : %(message)s"))
    logger = logging.getLogger(getpass.getuser())
    logger.setLevel(logging.DEBUG)
    logger.addHandler(kafka_handler)
    logger.info("The %s boxing wizards jump %s", 5, "quickly")
    logger.info("Testing for producing testing message to Kafka")
    logger.debug("The quick brown %s jumps over the lazy %s", "fox",  "dog")
    # try:
    #     import math
    #     math.exp(10000)
    # except Exception as e:
    #     logger.exception("Problem with %s", "math.exp")
    # finally:
    #     logger.info("All done.")

    logger.info("All done.")

