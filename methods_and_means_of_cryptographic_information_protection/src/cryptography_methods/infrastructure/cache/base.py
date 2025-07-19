from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class Key:
    value: str


@dataclass(frozen=True, slots=True)
class Prefix:
    value: str


@dataclass(frozen=True, slots=True)
class KeyWithPrefix:
    key: Key
    prefix: Prefix | None = None


class CacheStore(Protocol):
    """Абстракция для кэширования данных"""

    @abstractmethod
    async def set(
            self,
            key: KeyWithPrefix,
            value: Any,
            ttl: int = 30,
    ) -> None:
        """Сохранить данные с TTL (в секундах)"""
        ...

    @abstractmethod
    async def get(self, key: KeyWithPrefix, default: Any | None = None) -> Any:
        """Получить данные по ключу"""
        ...

    @abstractmethod
    async def delete(self, key_with_prefix: KeyWithPrefix) -> None:
        """Удалить данные по ключу"""
        ...

    @abstractmethod
    async def clear_by_prefix(self, prefix: Prefix) -> None:
        """Очистить все ключи с указанным префиксом"""
        ...

    @abstractmethod
    async def exists(self, key: KeyWithPrefix) -> bool:
        """Проверить существование ключа"""
        ...
