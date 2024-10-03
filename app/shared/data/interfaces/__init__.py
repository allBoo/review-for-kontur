from typing import TypeVar, Callable

T = TypeVar("T")
type Validator[T] = Callable[[T], bool]  # type: ignore
type Mutator[T] = Callable[[T], T]  # type: ignore


__all__ = ['Validator', 'Mutator']
