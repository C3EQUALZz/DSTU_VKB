from typing import Any, Protocol, TypeVar


class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...

    def __gt__(self, other: Any) -> bool: ...


CT = TypeVar("CT", bound=Comparable)
