from typing import Dict, List, Set, Any, KeysView, Union
from kafka import KafkaProducer
from kafka.client_async import selectors
from kafka.partitioner.default import DefaultPartitioner
from logging import Logger, Handler, Formatter, FileHandler, StreamHandler
import socket



class BaseConfig:

    _KAFKA_CONFIG = {}

    @property
    def config(self) -> Dict[str, Any]:
        if self._KAFKA_CONFIG:
            return self._KAFKA_CONFIG
        raise NotImplementedError("Should configure the default value of setting with variable '_KAFKA_CONFIG'.")


    def get_config_by_key(self, key: str) -> Any:
        if key in self.keys():
            return self._KAFKA_CONFIG[key]
        else:
            KeyError("'KAFKA_SENDER_CONFIG' doesn't have the keyword.")


    def keys(self) -> KeysView[Union[str, Any]]:
        return self._KAFKA_CONFIG.keys()


    def update(self, key: str, value: Any) -> None:
        if key in self.keys():
            self._KAFKA_CONFIG[key] = value
        else:
            KeyError("'KAFKA_CONFIG' doesn't have the keyword.")


    def batch_update(self, **config) -> None:
        for key, value in config.items():
            self.update(key=key, value=value)



class KafkaProducerConfig(BaseConfig):

    _KAFKA_CONFIG = {
        'bootstrap_servers': 'localhost',
        'client_id': None,
        'key_serializer': None,
        'value_serializer': None,
        'acks': 1,
        'bootstrap_topics_filter': set(),
        'compression_type': None,
        'retries': 0,
        'batch_size': 16384,
        'linger_ms': 0,
        'partitioner': DefaultPartitioner(),
        'buffer_memory': 33554432,
        'connections_max_idle_ms': 9 * 60 * 1000,
        'max_block_ms': 60000,
        'max_request_size': 1048576,
        'metadata_max_age_ms': 300000,
        'retry_backoff_ms': 100,
        'request_timeout_ms': 30000,
        'receive_buffer_bytes': None,
        'send_buffer_bytes': None,
        'socket_options': [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)],
        'sock_chunk_bytes': 4096,  # undocumented experimental option
        'sock_chunk_buffer_count': 1000,  # undocumented experimental option
        'reconnect_backoff_ms': 50,
        'reconnect_backoff_max_ms': 1000,
        'max_in_flight_requests_per_connection': 5,
        'security_protocol': 'PLAINTEXT',
        'ssl_context': None,
        'ssl_check_hostname': True,
        'ssl_cafile': None,
        'ssl_certfile': None,
        'ssl_keyfile': None,
        'ssl_crlfile': None,
        'ssl_password': None,
        'ssl_ciphers': None,
        'api_version': None,
        'api_version_auto_timeout_ms': 2000,
        'metric_reporters': [],
        'metrics_num_samples': 2,
        'metrics_sample_window_ms': 30000,
        'selector': selectors.DefaultSelector,
        'sasl_mechanism': None,
        'sasl_plain_username': None,
        'sasl_plain_password': None,
        'sasl_kerberos_service_name': 'kafka',
        'sasl_kerberos_domain_name': None,
        'sasl_oauth_token_provider': None
    }



class KafkaMsgSenderConfig(BaseConfig):

    _KAFKA_CONFIG = {
        "topic": None,
        "key": bytes(),
        "partition": None,
        "value": bytes(),
        "headers": None,
        "timestamp_ms": None
    }

    __BYTES_VALUE_NECESSARY_KEYS = ["key", "value"]


    def update(self, key: str, value: Any) -> None:
        """
        Description:
            Overwrite this method because it has some value should be saved as byte type except string or Any.
        :param key:
        :param value:
        :return:
        """
        if key in self.keys():
            if key in self.__BYTES_VALUE_NECESSARY_KEYS:
                print(f"[DEBUG] key: {key}")
                print(f"[DEBUG] value: {value}")
                self._KAFKA_CONFIG[key] = bytes(value.encode("utf-8"))
            else:
                print(f"[DEBUG] key (out): {key}")
                print(f"[DEBUG] value (out): {value}")
                self._KAFKA_CONFIG[key] = value
        else:
            KeyError("'KAFKA_CONFIG' doesn't have the keyword.")



class KafkaHandler(Handler):

    def __init__(self, producer_configs: Dict[str, Any], sender_configs: Dict[str, Any]):
        super().__init__()

        # Initialize Kafka Producer instance
        if not isinstance(producer_configs, Dict):
            raise TypeError("kafka producer configuration value should be Dict type")
        __producer_config_management = KafkaProducerConfig()
        __producer_config_management.batch_update(**producer_configs)
        self.__producer = KafkaProducer(**__producer_config_management.config)

        # Initialize Kafka Sender instance
        if not isinstance(sender_configs, Dict):
            raise TypeError("kafka sender configuration value should be Dict type")
        self.__sender_config_management = KafkaMsgSenderConfig()
        self.__sender_config_management.batch_update(**sender_configs)


    def emit(self, record):
        __msg = self.format(record)
        self.__sender_config_management.update(key="value", value=__msg)
        __sender_config = self.__sender_config_management.config
        __sender = self.__producer.send(**__sender_config)
        __sender.get()


    def close(self):
        self.__producer.close()
        Handler.close(self)
