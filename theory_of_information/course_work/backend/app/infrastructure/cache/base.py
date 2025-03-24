from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Получить значение по ключу"""
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int = 60) -> None:
        """Сохранить значение по ключу с временем жизни"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Удалить значение по ключу"""
        raise NotImplementedError

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Проверить, существует ли ключ"""
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        Закрыть подключение кэша.
        :return:
        """
        raise NotImplementedError
