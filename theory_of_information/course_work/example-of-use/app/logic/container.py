import boto3
from botocore.client import BaseClient
from botocore.config import Config
from dishka import Provider, provide, Scope, from_context, make_container

from app.infrastructure.compressors.factory import CompressorFactory
from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.compression import CompressFileCommand, DecompressFileCommand
from app.logic.handlers.compression.commands import CompressFileCommandHandler, DecompressFileCommandHandler
from app.logic.types.handlers import EventHandlerMapping, CommandHandlerMapping, UT
from app.settings.config import Settings, get_settings
from typing import cast


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_mapping_and_command_handlers(self) -> CommandHandlerMapping:
        """
        Here you have to link commands and command handlers for future inject in Bootstrap
        """
        return cast(
            CommandHandlerMapping,
            {
                CompressFileCommand: CompressFileCommandHandler,
                DecompressFileCommand: DecompressFileCommandHandler,
            },
        )

    @provide(scope=Scope.APP)
    def get_mapping_event_and_event_handlers(self) -> EventHandlerMapping:
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(
            EventHandlerMapping,
            {

            }
        )


class S3Provider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_s3_client(self, settings: Settings) -> BaseClient:
        return boto3.client(
            's3',
            endpoint_url=settings.s3.url,  # или https для SSL
            aws_access_key_id=settings.s3.host,  # Логин MinIO
            aws_secret_access_key=settings.s3.password,  # Пароль MinIO
            config=Config(signature_version='s3v4'),  # Требуется для MinIO
            region_name='us-east-1'  # Может быть любым для MinIO
        )


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_compression_uow(self) -> CompressionUnitOfWork:
        return CompressionUnitOfWork()

    @provide(scope=Scope.APP)
    def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            uow: UT
    ) -> Bootstrap[UT]:
        return Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={"factory": CompressorFactory}
        )


container = make_container(
    HandlerProvider(),
    S3Provider(),
    AppProvider(),
    context={
        Settings: get_settings(),
    }
)
