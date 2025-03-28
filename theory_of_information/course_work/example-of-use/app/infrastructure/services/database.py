from app.infrastructure.database.base import BaseDatabaseCLIService


class DatabaseService:
    def __init__(self, cli_service: BaseDatabaseCLIService) -> None:
        self._cli_service = cli_service

    def list_all_databases(self) -> None:
        self._cli_service.list_all_databases()

