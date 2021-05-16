"""
Description:
    Test for Kafka features:
        1. Kafka Topic and Topic key
        2. Kafka Partitions
"""

from kafka import KafkaConsumer, TopicPartition, KafkaAdminClient

__consumer = KafkaConsumer(bootstrap_servers="localhost:9092")
con_topics = __consumer.topics()
part_of_topic = __consumer.partitions_for_topic(topic="logging_test")
print(f"All topics: {con_topics}")
print(f"All topics partition: {part_of_topic}")
# __test_topic = TopicPartition(topic="test", partition=1)

__admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092")
list_topics = __admin_client.list_topics()
list_consumer_groups = __admin_client.list_consumer_groups()
print(f"list_topics: {list_topics}")
print(f"list_consumer_groups: {list_consumer_groups}")
