from typing import Tuple

from app.domain.entities.token import AccessToken, RefreshToken
from app.domain.entities.user import UserEntity
from app.infrastructure.exceptions import UserNotFoundError
from app.infrastructure.services.users import UsersService
from app.infrastructure.uow.users.base import UsersUnitOfWork


class AuthService:
    ...