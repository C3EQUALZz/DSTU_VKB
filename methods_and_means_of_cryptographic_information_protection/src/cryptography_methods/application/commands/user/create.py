from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    first_name: str
    second_name: str | None = None
    middle_name: str | None = None
    phone_number: str | None = None
    telegram_id: int | None = None


class CreateUserCommandHandler:
    def __init__(self) -> None:
        ...

    async def __call__(self, data: CreateUserCommand):
        ...
