from typing import Generic, TypeVar, Type, Union

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from shared.data.db.model import BaseModel

T = TypeVar('T', bound=BaseModel)
PK = Union[int, str]


class Repository(Generic[T]):
    def __init__(self, conn: AsyncSession, cls: Type[T]) -> None:
        self._conn = conn
        self._cls = cls

    def get_queryset(self) -> sa.sql.Select:
        return sa.select(self._cls)

    async def get_by_id(self, entity_id: PK) -> Union[T, None]:
        return await self._conn.scalar(
            sa.select(self._cls).where(self._cls.id == entity_id)
        )

    async def get_by_ids(self, entity_ids: list[PK]) -> dict[PK, T]:
        res = await self._conn.scalars(
            sa.select(self._cls).where(self._cls.id.in_(entity_ids))
        )
        return {item.id: item for item in res}
