from __future__ import annotations

import logging
from typing import Any, TypeVar, Self, AsyncGenerator

from pydantic import BaseModel
from sqlalchemy import ColumnExpressionArgument

from shared.data.db.repository import Repository
from shared.data.source.interfaces import Reader

TR = TypeVar('TR', bound=BaseModel, covariant=True)

logger = logging.getLogger(__name__)


class DatabaseReader(Reader[TR]):
    def __init__(self, repository: Repository, model: TR):
        self.repository = repository
        self.model = model
        self.query = self.repository.get_queryset()

    def filter(self, criteria: ColumnExpressionArgument) -> Self:
        self.query = self.query.where(criteria)
        return self

    async def read(self, fail_on_error=False, silent=False) -> AsyncGenerator[TR, None]:
        async with self.repository._conn.begin():
            for item in await self.repository._conn.scalars(self.query):
                yield self.model.model_validate(item, from_attributes=True)

    async def read_one(self) -> TR | None:
        async with self.repository._conn.begin():
            result = await self.repository._conn.execute(self.query)
            item = result.first()
            if item:
                return self.model.model_validate(item.first(), from_attributes=True)
            return None

    async def close(self) -> None:
        pass
