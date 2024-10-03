from __future__ import annotations

from typing import Generic, TypeVar, Type, Union, Any, Iterable

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from load.data.dto import Dto
from load.data.dto.base import StateMixin, STATE_ACTIVE, STATE_DELETE
from shared.data.click.model import BaseModel, CollapseMixin

T = TypeVar('T', bound=BaseModel)
DT = TypeVar('DT', bound=Dto, covariant=True)
PK = Union[int, str]


class Repository(Generic[T]):
    def __init__(self, conn: AsyncSession, cls: Type[T], dto_cls: Type[DT] | None = None) -> None:
        self._conn = conn
        self._cls = cls
        self._dto_cls = dto_cls

    async def add(self, entity: Union) -> None:
        return self._conn.add(entity)

    async def add_dto(self, entity: DT) -> None:
        await self._conn.execute(
            self._cls.__table__.insert(), [self._cls.from_dto(entity)]
        )

    async def bulk_insert(self, entities: Iterable[T]) -> None:
        if not entities:
            return
        return self._conn.add_all(entities)

    async def bulk_insert_dtos(self, entities: Iterable[DT]) -> None:
        if not entities:
            return
        await self._conn.execute(
            self._cls.__table__.insert(), [self._cls.from_dto(e) for e in entities]
        )

    async def update(self, entity_id: PK, values: dict) -> int:
        res = await self._conn.execute(
            self._cls.__table__.update().where(self._cls.id == entity_id).values(**values)
        )
        return res.rowcount()

    async def get_by_id(self, entity_id: PK) -> Union[T, None]:
        return await self._conn.scalar(
            sa.select(self._cls).where(self._cls.id == entity_id)
        )

    async def delete_by(self, where: dict[str, Any]) -> int:
        res = await self._conn.execute(
            self._cls.__table__.delete().filter_by(**where)
        )
        return res.rowcount

    async def get_list_final(self, where: dict[str, Any]) -> Iterable[T]:
        clauses = []
        for key, value in where.items():
            if isinstance(value, list):
                clauses.append(getattr(self._cls, key).in_(value))
            else:
                clauses.append(getattr(self._cls, key) == value)

        await self._conn.execute(sa.text('SET final = 1'))

        results = await self._conn.scalars(
            sa.select(self._cls).filter(*clauses)
        )

        await self._conn.execute(sa.text('SET final = 0'))

        return results

    async def bulk_upsert_dtos(self, entities: list[DT], where: dict[str, Any]) -> None:
        assert issubclass(self._cls, CollapseMixin)
        assert self._dto_cls and issubclass(self._dto_cls, (Dto, StateMixin))

        to_upsert: list[DT] = []

        exists_records = await self.get_list_final(where)
        for record in exists_records:
            delete_entity = self._dto_cls.model_validate(record, from_attributes=True)
            delete_entity.State = STATE_DELETE

            to_upsert.append(delete_entity)

        for entity in entities:
            entity.State = STATE_ACTIVE
            to_upsert.append(entity)

        await self.bulk_insert_dtos(to_upsert)
