from typing import cast

import boto3
from app.infrastructure.compressors.factory import CompressorFactory
from app.infrastructure.database.base import BaseDatabaseCLIService
from app.infrastructure.database.postgres import (PostgresCLIService,
                                                  PostgresConfig)
from app.infrastructure.repositories.database.base import \
    DatabaseDumpRepository
from app.infrastructure.repositories.database.boto3 import \
    DatabaseDumpBoto3Repository
from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.compression import (CompressFileCommand,
                                            DecompressFileCommand)
from app.logic.commands.database import (CreateDatabaseBackupCommand,
                                         ListAllDatabasesCommand)
from app.logic.commands.s3 import CreateFileInS3Command, ListFilesInS3Command
from app.logic.commands.stats import GetFileFullStatsCommand
from app.logic.handlers.compression.commands import (
    CompressFileCommandHandler, DecompressFileCommandHandler)
from app.logic.handlers.database.commands import (
    CreateDatabaseBackupCommandHandler, ListAllDatabasesCommandHandler)
from app.logic.handlers.s3.commands import (CreateFileInS3CommandHandler,
                                            ListFilesInS3CommandHandler)
from app.logic.handlers.stats.commands import GetFileFullStatsCommandHandler
from app.logic.types.handlers import (UT, CommandHandlerMapping,
                                      EventHandlerMapping)
from app.settings.config import Settings, get_settings
from botocore.client import BaseClient
from botocore.config import Config
from dishka import Provider, Scope, from_context, make_container, provide


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_mapping_and_command_handlers(self) -> CommandHandlerMapping:
        """
        Here you have to link commands and command handlers for future inject in Bootstrap
        """
        return cast(
            "CommandHandlerMapping",
            {
                CompressFileCommand: CompressFileCommandHandler,
                DecompressFileCommand: DecompressFileCommandHandler,
                ListAllDatabasesCommand: ListAllDatabasesCommandHandler,
                CreateDatabaseBackupCommand: CreateDatabaseBackupCommandHandler,
                CreateFileInS3Command: CreateFileInS3CommandHandler,
                ListFilesInS3Command: ListFilesInS3CommandHandler,
                GetFileFullStatsCommand: GetFileFullStatsCommandHandler,
            },
        )

    @provide(scope=Scope.APP)
    def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast("EventHandlerMapping", {})


class S3Provider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_s3_client(self, settings: Settings) -> BaseClient:
        return boto3.client(
            "s3",
            endpoint_url=settings.s3.url,
            aws_access_key_id=settings.s3.user,
            aws_secret_access_key=settings.s3.password,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_compression_uow(self) -> CompressionUnitOfWork:
        return CompressionUnitOfWork()

    @provide(scope=Scope.APP)
    def get_database_cli_service(self, settings: Settings) -> BaseDatabaseCLIService:
        return PostgresCLIService(
            psql_bin_path=settings.database.psql_bin_path,
            postgres_config=PostgresConfig(
                user=settings.database.user,
                password=settings.database.password,
                host=settings.database.host,
                port=settings.database.port,
                database_name=settings.database.name,
            ),
        )

    @provide(scope=Scope.APP)
    def get_dump_repository(self, client: BaseClient, settings: Settings) -> DatabaseDumpRepository:
        return DatabaseDumpBoto3Repository(
            client=client, bucket_name=settings.s3.bucket_name, bucket_path=settings.s3.bucket_backup_path
        )

    @provide(scope=Scope.APP)
    def get_bootstrap(
        self,
        events: EventHandlerMapping,
        commands: CommandHandlerMapping,
        database_cli_service: BaseDatabaseCLIService,
        repo: DatabaseDumpRepository,
        uow: UT,
    ) -> Bootstrap[UT]:
        return Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={
                "factory": CompressorFactory(),
                "database_cli_service": database_cli_service,
                "s3_dump_repository": repo,
            },
        )


container = make_container(
    HandlerProvider(),
    S3Provider(),
    AppProvider(),
    context={
        Settings: get_settings(),
    },
)
