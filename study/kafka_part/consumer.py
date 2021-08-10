#! /anaconda/bin/python3

from multi_kafka_worker import EnterPoint, Strategy, TestKafka
from kafka_config import KAFKA_HOSTS, KAFKA_TOPIC

from kafka import KafkaConsumer, TopicPartition
from threading import get_ident
from datetime import datetime



class TestConsumer(TestKafka):

    def kafka_process(self, **kwargs) -> None:
        consumer = KafkaConsumer(bootstrap_servers=KAFKA_HOSTS)

        # # Method 1. (Deserialize)
        # consumer.subscribe(["logging_test"])
        # for message in consumer:
        #     print(f"Thread name - {get_ident()}: {message}")

        # # Method 2. (Manual)
        __topic = TopicPartition(topic=KAFKA_TOPIC, partition=0)
        consumer.assign([__topic])
        while True:
            __msg = next(consumer)
            print(f"Thread name - {get_ident()}: {__msg}")



if __name__ == '__main__':

    # Multiprocessing
    # EnterPoint.run(running_strategy=Strategy.Processing, kafka_strategy=TestConsumer(), worker_number=10)
    # Multithreading
    # EnterPoint.run(running_strategy=Strategy.Processing, kafka_strategy=TestConsumer(), worker_number=10)
    # Multi-Greenlet
    EnterPoint.get_data(running_strategy=Strategy.Greenlet, kafka_strategy=TestConsumer(), worker_number=10)
