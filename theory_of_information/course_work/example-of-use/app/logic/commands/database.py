from app.logic.commands.base import AbstractCommand
from dataclasses import dataclass


@dataclass(frozen=True)
class ListAllDatabasesCommand(AbstractCommand):
    ...


@dataclass(frozen=True)
class CreateDatabaseBackupCommand(AbstractCommand):
    database_name: str
