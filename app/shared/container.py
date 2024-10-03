from abc import ABC, abstractmethod

from shared.infrastructure.clickhouse import Clickhouse
from shared.infrastructure.db import DataBase


class Container(ABC):
    @abstractmethod
    def get_web_host_url(self) -> str:
        ...

    @abstractmethod
    def get_database(self) -> DataBase:
        ...

    @abstractmethod
    def get_clickhouse(self) -> Clickhouse:
        ...
