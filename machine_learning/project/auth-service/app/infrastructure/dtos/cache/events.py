import json
from dataclasses import dataclass
from typing import override, Self

from app.infrastructure.dtos.cache.base import BaseCacheDTO
from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class EventCacheDTO(BaseCacheDTO):
    event: AbstractEvent

    @property
    def key(self) -> str:
        return self.event.oid

    @classmethod
    @override
    def from_cache(cls, data: bytes) -> Self:
        """
        Getting a DTO object from cache
        :param data: bytes from cache
        :return: DTO object
        """
        return cls(**json.loads(data))

    @override
    def to_cache(self) -> bytes:
        """Преобразует объект в данные для сохранения в кэше."""
        return json.dumps(self.event.to_dict()).encode()
