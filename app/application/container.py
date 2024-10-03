from typing import Any

from shared.container import Container
from shared.infrastructure.clickhouse import Clickhouse
from shared.infrastructure.db import DataBase
from config import Config


class ApplicationContainer(Container):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.services: dict[str, Any] = {}

    def get_web_host_url(self) -> str:
        return self.config.WEB_HOST_URL

    def get_database(self) -> DataBase:
        if 'database' not in self.services:
            self.services['database'] = DataBase(str(self.config.DATABASE_DSN))

        return self.services['database']

    def get_clickhouse(self) -> Clickhouse:
        if 'clickhouse' not in self.services:
            self.services['clickhouse'] = Clickhouse(
                str(self.config.CLICKHOUSE_DSN),
                self.config.CLICKHOUSE_USE_SSL,
                self.config.CA_LOCATION
            )

        return self.services['clickhouse']
