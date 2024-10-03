import os
import json

import yandexcloud

from typing import Any

from yandex.cloud.lockbox.v1.payload_service_pb2 import GetPayloadRequest
from yandex.cloud.lockbox.v1.payload_service_pb2_grpc import PayloadServiceStub

from config import settings


ENTRY_KEY = 'config'

LOCKBOX_VARS = [
    'DEBUG',
    'WEB_HOST_URL',
    'KAFKA_DSN',
    'KAFKA_USE_SSL',
    'KAFKA_CONSUMER_GROUP',
    'KAFKA_PRODUCER_FLUSH_INTERVAL',
    'DATABASE_DSN',
    'DATABASE_USE_SSL',
    'CLICKHOUSE_DSN',
    'CLICKHOUSE_USE_SSL',
    'SENTRY_DSN',
    'SENTRY_ENVIRONMENT',
    'API_TOKEN',
    'INCOMING_EVENTS_LIMIT',
    'CMS_API_BASE_URL',
    'CMS_API_TOKEN',
]


def setup_lockbox() -> None:
    sa_key = os.environ.get('LOCKBOX_SA_KEY')
    secret_id = os.environ.get('LOCKBOX_SECRET_ID')

    if sa_key and secret_id:
        secret = _load_secret(sa_key, secret_id)
        for key, value in secret.items():
            if key.upper() in LOCKBOX_VARS:
                os.environ[key.upper()] = str(value)
                settings.update(key.upper(), value)


def _load_secret(sa_key: str, secret_id: str) -> dict[str, Any]:
    secret = dict()
    yc_sdk = yandexcloud.SDK(service_account_key=json.loads(sa_key))
    lockbox = yc_sdk.client(PayloadServiceStub)
    response = lockbox.Get(GetPayloadRequest(secret_id=secret_id))
    for entry in response.entries:
        if entry.key == ENTRY_KEY:
            secret = json.loads(entry.binary_value.decode())
    return secret
