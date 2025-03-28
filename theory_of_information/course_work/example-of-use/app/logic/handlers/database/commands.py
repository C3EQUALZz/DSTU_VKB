from app.infrastructure.services.database import DatabaseService
from app.logic.commands.database import (
    CreateDatabaseBackupCommand,
    ListAllDatabasesCommand,
)
from app.logic.handlers.database.base import DatabaseCLICommandHandler


class ListAllDatabasesCommandHandler(DatabaseCLICommandHandler[ListAllDatabasesCommand]):
    def __call__(self, command: ListAllDatabasesCommand) -> None:
        service: DatabaseService = DatabaseService(self._cli_service)
        return service.list_all_databases()


class CreateDatabaseBackupCommandHandler(DatabaseCLICommandHandler[CreateDatabaseBackupCommand]):
    def __call__(self, command: CreateDatabaseBackupCommand) -> None:
        service: DatabaseService = DatabaseService(self._cli_service)
        return service.create_backup()
