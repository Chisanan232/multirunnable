#! /anaconda/bin/python3

from multi_kafka_worker import EnterPoint, Strategy, TestKafka
from kafka_config import KAFKA_HOSTS, KAFKA_TOPIC

from kafka import KafkaProducer
from threading import get_ident
from gevent.lock import Semaphore
from datetime import datetime


greenlet_semaphore = Semaphore(value=1)


class TestProducer(TestKafka):

    def kafka_process(self, **kwargs) -> None:
        with greenlet_semaphore:
            producer = KafkaProducer(bootstrap_servers=KAFKA_HOSTS)
            msg = f"Hello Kafka, I'm Python 3.7 - thread name is {get_ident()}! Mr. Worldwide! - time: {datetime.now()}"
            # producer.send(topic="logging_test", value=b"Hello Kafka, I'm Python 3.7! Mr. Worldwide!")
            # producer.send(topic="logging_test", value=msg.encode("utf-8"))
            # producer.send(topic="logging_test", value=bytes(msg.encode("utf-8")))
            producer.send(topic=KAFKA_TOPIC, value=bytes(msg, "utf-8"))
            producer.close()



if __name__ == '__main__':

    # Multiprocessing
    # EnterPoint.run(running_strategy=Strategy.Processing, kafka_strategy=TestProducer(), worker_number=10)
    # Multithreading
    # EnterPoint.run(running_strategy=Strategy.Processing, kafka_strategy=TestProducer(), worker_number=10)
    # Multi-Greenlet
    EnterPoint.get_data(running_strategy=Strategy.Greenlet, kafka_strategy=TestProducer(), worker_number=10)
    # Async
    # EnterPoint.run(running_strategy=Strategy.Async, kafka_strategy=TestProducer(), worker_number=10)
