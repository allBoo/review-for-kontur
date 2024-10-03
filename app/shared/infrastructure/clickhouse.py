from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from clickhouse_sqlalchemy import (
    make_session
)


class Clickhouse:
    def __init__(self, connection_string: str, ssl: bool = False, ca_certs: str | None = None):
        self.connection_string = connection_string

        connection_args = {'secure': True, 'ca_certs': ca_certs} if ssl else {}
        self.engine = create_async_engine(connection_string, echo=False, connect_args=connection_args)

    def get_connection(self) -> AsyncSession:
        return make_session(self.engine, is_async=True)
