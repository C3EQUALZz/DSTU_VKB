import logging
from app.domain.entities.user import UserEntity
from app.domain.values.user import Email, Password, Role
from app.infrastructure.services.users import UsersService
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.infrastructure.utils.security import hash_password
from app.settings.config import Settings

logger = logging.getLogger(__name__)


async def setup_admin(uow: UsersUnitOfWork, settings: Settings) -> None:
    logger.info('Setting up admin user')
    service = UsersService(uow=uow)

    if not await service.check_existence(email=settings.admin.email):
        logger.info('Admin user does not exist in database, creating...')

        first_admin = UserEntity(
            surname=settings.admin.surname,
            name=settings.admin.name,
            patronymic=settings.admin.patronymic,
            email=Email(settings.admin.email),
            password=Password(hash_password(settings.admin.password)),
            role=Role("admin")
        )

        await service.add(first_admin)

        logger.info('Admin user created!')
