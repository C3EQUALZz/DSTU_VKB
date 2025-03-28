from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class ListAllDatabasesCommand(AbstractCommand): ...


@dataclass(frozen=True)
class CreateDatabaseBackupCommand(AbstractCommand):
    database_name: str
