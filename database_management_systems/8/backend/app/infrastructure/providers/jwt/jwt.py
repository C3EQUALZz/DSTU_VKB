import jwt
from datetime import datetime, UTC
from typing import Type

from app.infrastructure.providers.jwt.base import TokenProvider, T


class JWTTokenProvider(TokenProvider[T]):
    def __init__(self, secret: str, algorithm: str, token_type: Type[T]):
        self.secret = secret
        self.algorithm = algorithm
        self.token_type = token_type  # Класс токена (например, AccessToken)

    def create_token(self, token: T) -> str:
        """Создаёт токен на основе объекта токена"""
        payload = token.to_dict()
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> T:
        """Декодирует токен и возвращает объект токена"""
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        return self.token_type.from_dict(payload)

    def validate_token(self, token: str) -> bool:
        """Проверяет валидность токена"""
        try:
            decoded_token = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            exp = datetime.fromtimestamp(decoded_token["exp"], tz=UTC)
            return exp > datetime.now(UTC)
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
