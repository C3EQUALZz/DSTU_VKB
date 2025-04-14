from typing import get_type_hints

from app.logic.commands.base import AbstractCommand


class ImageCommandFactory:
    def __init__(self, commands: dict[str, type[AbstractCommand]]) -> None:
        self._commands: dict[str, type[AbstractCommand]] = commands

    def create(self, action: str, /, **kwargs) -> AbstractCommand:
        field_names = set(get_type_hints(self._commands[action]))
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in field_names}
        return self._commands[action](**filtered_kwargs)  # type: ignore
