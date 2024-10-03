from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from clickhouse_sqlalchemy import get_declarative_base

from load.data.dto import Dto

metadata = sa.MetaData()
Base = get_declarative_base(metadata=metadata)


class BaseModel(Base):
    __abstract__ = True

    metadata = metadata

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    @classmethod
    def from_dto(cls, dto: Dto) -> dict[str, Any]:
        return dto.model_dump()


class CollapseMixin:
    State: Mapped[int] = mapped_column(sa.Integer, nullable=False)
