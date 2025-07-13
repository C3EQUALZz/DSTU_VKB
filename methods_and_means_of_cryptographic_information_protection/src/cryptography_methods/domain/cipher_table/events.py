from dataclasses import dataclass
from typing import Iterable

from cryptography_methods.domain.common.events import BaseDomainEvent


@dataclass(frozen=True, slots=True)
class TableCreatedAndFilledSuccessfullyEvent(BaseDomainEvent):
    table: Iterable[Iterable[str]]
    fill_by_column: bool


@dataclass(frozen=True, slots=True)
class SwappedSpacesOnSymbolsEvent(BaseDomainEvent):
    old_string: str
    new_string: str
