# Project Structure

```
src/
  domain/
  application/
  infrastructure/
  presentation/
  setup/
tests/
  unit/
  integration/
  e2e/
```

Rules:
- Dependencies flow inward: presentation → application → domain
- `domain` contains only business logic, no external dependencies
- `infrastructure` implements interfaces defined in `application`

## Application layer

Application folder has these directories:
```
commands/
queries/
common/
event_handlers/
```

In commands folder and queries folder we have folders with domain name. In folders with domain name we have different interactors (command handlers and queries).
For example, we have domain which represents user. So, we creating `application/commands/user/create_user.py`. And writing code like this:

```
@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserCommand:
    email: str
    name: str
    password: str
    role: UserRole = UserRole.USER


@final
class CreateUserCommandHandler:
    def __init__(
        self,
        transaction_manager: TransactionManager,
        user_command_gateway: UserCommandGateway,
        user_service: UserService,
        event_bus: EventBus,
        current_user_service: CurrentUserService,
        access_service: AccessService,
    ) -> None:
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._event_bus: Final[EventBus] = event_bus
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._access_service: Final[AccessService] = access_service

    async def __call__(self, data: CreateUserCommand) -> CreateUserView:
        logger.info(
            "Create user: started. Username: '%s'.",
            data.name,
        )

        current_user: User = await self._current_user_service.get_current_user()

        self._access_service.authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=data.role,
            ),
        )

        new_user: User = self._user_service.create(
            email=UserEmail(data.email),
            name=Username(data.name),
            raw_password=RawPassword(data.password),
            role=data.role,
        )

        if (await self._user_command_gateway.read_by_email(new_user.email)) is not None:
            msg: str = f"user with this email: {new_user.email} already exists"
            raise UserAlreadyExistsError(msg)

        await self._user_command_gateway.add(new_user)
        await self._transaction_manager.flush()
        await self._event_bus.publish(self._user_service.pull_events())
        await self._transaction_manager.commit()

        logger.info("Create user: done. Username: '%s'.", new_user.name)

        return CreateUserView(
            user_id=new_user.id,
        )
```

Example of code in `queries/users/read_all.py`:

```
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.query_params.pagination import Pagination
from pix_erase.application.common.query_params.sorting import SortingOrder
from pix_erase.application.common.query_params.user_filters import UserListParams, UserListSorting, UserQueryFilters
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.user.read_user_by_id import ReadUserByIDView
from pix_erase.application.errors.query_params import SortingError
from pix_erase.domain.user.services.access_service import AccessService

if TYPE_CHECKING:
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadAllUsersQuery:
    limit: int
    offset: int
    sorting_field: str
    sorting_order: SortingOrder


@final
class ReadAllUsersQueryHandler:
    """
    - Open to everyone.
    - Retrieves a paginated list of existing users with relevant information.
    """

    def __init__(
        self,
        user_query_gateway: UserQueryGateway,
        current_user_service: CurrentUserService,
        access_service: AccessService,
    ) -> None:
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._access_service: Final[AccessService] = access_service

    async def __call__(self, data: ReadAllUsersQuery) -> list[ReadUserByIDView]:
        logger.info("List users started")

        logger.debug("Started got current user")
        current_user: User = await self._current_user_service.get_current_user()
        logger.debug("Got current user, user id: %s", current_user.id)

        logger.debug("Retrieving list of users.")

        user_list_params: UserListParams = UserListParams(
            pagination=Pagination(
                limit=data.limit,
                offset=data.offset,
            ),
            sorting=UserListSorting(
                sorting_field=UserQueryFilters(data.sorting_field),
                sorting_order=data.sorting_order,
            ),
        )

        users: list[User] | None = await self._user_query_gateway.read_all_users(user_list_params)

        if users is None:
            logger.error(
                "Retrieving list of users failed: invalid sorting column '%s'.",
                data.sorting_field,
            )
            msg = f"Invalid sorting field: {data.sorting_field}"
            raise SortingError(msg)

        response: list[ReadUserByIDView] = [
            ReadUserByIDView(id=user.id, email=str(user.email), name=str(user.name), role=user.role) for user in users
        ]

        return response
```

All ports to infrastructure things create in application/common/ports. For example, `application/common/ports/event_bus.py`:

```
from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from pix_erase.domain.common.events import BaseDomainEvent


class EventBus(Protocol):
    @abstractmethod
    async def publish(self, events: Iterable[BaseDomainEvent]) -> None:
        raise NotImplementedError
```

## Domain layer

Example of structure for domain which represents user:

```
domain/
    user/
        entities/
            user.py
        value_objects/
            username.py
        services/
            user_service.py
        ports/
            id_generator.py
        event.py
```

In domain layer we have domain entities, aggregates. All entities and aggregates must inherit from `BaseEntity` and `BaseAggregateRoot`. 
All Value objects must inherit from `BaseValueObject`.
All domain services must inherit from `BaseDomainService`.

All ports in domain has adapters in infrastructure. For example ID generator in `user/ports/id_generator`:

```
from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.user.values.user_id import UserID


class UserIdGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> UserID:
        raise NotImplementedError
```


---

## Architecture Principles (if applicable)

- Follow Clean Architecture by default
- Depend on abstractions, not concrete implementations
- Extend behavior via composition, not modification
- Keep modules small with a single responsibility
- Use Dependency Injection
- Also use SOLID and GRASP
