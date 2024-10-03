import os
from configparser import ConfigParser
from typing import Any, TypeAlias, Self

from pydantic import Field, KafkaDsn, PostgresDsn, ClickHouseDsn, BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):

    @classmethod
    def from_config_file(cls, path: str) -> Self:
        config = ConfigParser()
        config.read(path)

        if config.has_section('app'):
            return cls(**config['app'])
        else:
            raise ValueError('Section "app" not found in config')


class Config(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    DEBUG: bool = Field(default=False)

    WEB_HOST_URL: str = Field(default='http://localhost:8001')
    ALLOWED_HOSTS: list[str] = Field(default_factory=lambda: os.getenv('ALLOWED_HOSTS', '*').split(','))

    CA_LOCATION: str = Field(default='/certificates/yc.crt')

    KAFKA_DSN: KafkaDsn = Field(default='kafka://kafka:29092')
    KAFKA_USE_SSL: bool = Field(default=False)
    KAFKA_CONSUMER_GROUP: str = Field(default='mediabox-group-1')
    KAFKA_PRODUCER_FLUSH_INTERVAL: int = Field(default=100)
    KAFKA_TOPICS_PREFIX: str = Field(default='mediabox')
    KAFKA_EVENTS_TOPIC: str = Field(default='events')
    KAFKA_DLQ_TOPIC: str = Field(default='dlq')

    DATABASE_DSN: PostgresDsn = Field(default='postgresql+asyncpg://mediaboxcms:mediaboxcmspassword@db:5432/mediabox')
    DATABASE_USE_SSL: bool = Field(default=False)

    CLICKHOUSE_DSN: ClickHouseDsn = Field(default='clickhouse+asynch://clickhouse:9000/default')
    CLICKHOUSE_USE_SSL: bool = Field(default=False)

    SENTRY_DSN: str = Field(default='')
    SENTRY_ENVIRONMENT: str = Field(default='dev')

    API_TOKEN: str = Field(default='test-your-luck')
    INCOMING_EVENTS_LIMIT: int = Field(default=100)

    CMS_API_BASE_URL: str = Field(default='http://cms:8000')
    CMS_API_TOKEN: str = Field(default='')

    LISTENER_RESTART_TIMEOUT: int = Field(default=600)

    app_config: AppConfig | None = None

    def update(self, key: str, value: Any) -> None:
        typ_ = type(self.__getattribute__(key))
        self.__setattr__(key, typ_(value))


settings = Config()
