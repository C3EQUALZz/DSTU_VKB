from typing import (
    Dict,
    List,
    Type,
)

from app.logic.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,

)

from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
    AbstractHandler,
    CT,
    ET,
)

from app.logic.handlers.users.commands import CreateUserCommandHandler

EVENTS_HANDLERS_FOR_INJECTION: Dict[Type[ET], List[Type[AbstractEventHandler[ET]]]] = {}

COMMANDS_HANDLERS_FOR_INJECTION: Dict[Type[CT], Type[AbstractCommandHandler[CT]]] = {
    CreateUserCommand: CreateUserCommandHandler,
}
