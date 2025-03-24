from app.domain.entities.user import UserEntity
from app.infrastructure.services.users import UsersService
from app.infrastructure.uow.users.base import UsersUnitOfWork


class UsersViews:
    """
    Views related to users, which purpose is to return information upon read requests,
    due to the fact that write requests (represented by commands) are different from read requests.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    async def get_user_by_id(self, user_id: str) -> UserEntity:
        users_service: UsersService = UsersService(self._uow)
        user: UserEntity = await users_service.get_by_id(user_id)
        return user

    async def get_all_users(self, page_number: int = 1, page_size: int = 10) -> list[UserEntity]:
        users_service: UsersService = UsersService(self._uow)
        start: int = (page_number - 1) * page_size
        limit: int = start + page_size
        users: list[UserEntity] = await users_service.get_all(start, limit)
        return users
