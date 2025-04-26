from typing import (
    Final,
    List,
)

from app.domain.entities.user import UserEntity
from app.infrastructure.clients.base import BaseClient


class UsersService:
    def __init__(self, url: str, client: BaseClient) -> None:
        self._url: Final[str] = url
        self._client: Final[BaseClient] = client

    async def add(self, user: UserEntity) -> UserEntity:
        ...

    async def update(self, user: UserEntity) -> UserEntity:
        ...

    async def get_by_id(self, oid: str) -> UserEntity:
        ...

    async def get_all(
            self, start: int | None = None, limit: int | None = None
    ) -> List[UserEntity]:
        ...

    async def delete(self, oid: str) -> None:
        ...

    async def check_existence(self, oid: str) -> bool:
        ...
