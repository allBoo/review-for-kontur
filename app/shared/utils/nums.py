from __future__ import annotations

from typing import TypeVar

MAX_UINT32 = 4294967295
MAX_UINT16 = 65535


T = TypeVar('T', int, float)


def limit(value: T, limit: T) -> T:
    return value if value <= limit else limit


def uint32(value: int) -> int:
    return limit(value, MAX_UINT32)


def uint16(value: int) -> int:
    return limit(value, MAX_UINT16)
