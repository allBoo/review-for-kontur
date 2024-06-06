import os


class ApiConfig:
    API_TOKEN: str = os.environ.get('API_TOKEN', 'test-your-luck')
    INCOMING_EVENTS_LIMIT: int = int(os.environ.get('INCOMING_EVENTS_LIMIT', 100))


class ExternalPortsConfig:
    CMS_API_BASE_URL: str = os.environ.get('CMS_API_BASE_URL', 'http://cms:8000')
    CMS_API_TOKEN: str = os.environ.get('CMS_API_TOKEN', '')


class KafkaConfig:
    KAFKA_SERVERS: str = os.environ.get('KAFKA_SERVERS', 'kafka:29092')
    KAFKA_RAW_EVENTS_TOPIC: str = os.environ.get('KAFKA_RAW_EVENTS_TOPIC', 'raw_events')
    KAFKA_RAW_EVENTS_CONSUMER_GROUP: str = os.environ.get('KAFKA_RAW_EVENTS_CONSUMER_GROUP', 'raw_events_group')
    KAFKA_RAW_EVENTS_CONSUMER_GROUP_VERSION: str = os.environ.get('KAFKA_RAW_EVENTS_CONSUMER_GROUP_VERSION', '0')
    KAFKA_PRODUCER_FLUSH_INTERVAL: int = int(os.environ.get('KAFKA_PRODUCER_FLUSH_INTERVAL', 10))   # highly recommended to use higher value


class ListenerConfig:
    LISTENER_RESTART_TIMEOUT: int = int(os.environ.get('LISTENER_RESTART_TIMEOUT', 300))


class Config(ExternalPortsConfig, ApiConfig, KafkaConfig):
    DEBUG: bool = bool(os.environ.get('DEBUG', False))
    ALLOWED_HOSTS: list[str] = os.environ.get('ALLOWED_HOSTS', '*').split(',')
