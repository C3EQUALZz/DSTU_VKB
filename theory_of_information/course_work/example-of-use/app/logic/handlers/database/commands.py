from app.infrastructure.services.database import DatabaseService
from app.logic.commands.database import ListAllDatabasesCommand
from app.logic.handlers.database.base import DatabaseCLICommandHandler


class ListAllDatabasesCommandHandler(DatabaseCLICommandHandler[ListAllDatabasesCommand]):
    def __call__(self, command: ListAllDatabasesCommand) -> None:
        service: DatabaseService = DatabaseService(self._cli_service)
        return service.list_all_databases()
