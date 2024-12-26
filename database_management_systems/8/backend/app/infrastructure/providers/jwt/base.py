from abc import (
    ABC,
    abstractmethod,
)
from typing import Generic, TypeVar

from app.domain.entities.token import Token

T = TypeVar("T", bound=Token)


class TokenProvider(ABC, Generic[T]):
    @abstractmethod
    def create_token(self, token: T) -> str:
        """Создаёт токен на основе переданного payload"""
        pass

    @abstractmethod
    def decode_token(self, token: str) -> T:
        """Декодирует токен и возвращает payload"""
        pass

    @abstractmethod
    def validate_token(self, token: str) -> bool:
        """Проверяет валидность токена"""
        pass
