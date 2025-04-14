import importlib
import logging
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import cast

from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.application.jobs.factory import JobFactory
from app.application.telegram.keyboards.callbacks.images import ImageCLickAction
from app.infrastructure.factories.image import ImageCommandFactory
from app.infrastructure.integrations.llm.image.gray_to_color.base import LLMImageMessageColorizationModel
from app.infrastructure.integrations.llm.image.gray_to_color.custom import KerasImageMessageColorizationModel
from app.infrastructure.integrations.llm.message.text.base import LLMTextMessageModel
from app.infrastructure.integrations.llm.message.text.open_ai import OpenAITextMessageModel
from app.infrastructure.services.image import ImageService
from app.infrastructure.services.text import TextMessageService
from app.infrastructure.uow.users.alchemy import SQLAlchemyUsersUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.images import ColorizeImageCommand
from app.logic.commands.texts import SendTextMessageToChatBotCommand
from app.logic.handlers.images.commands import ColorizeImageCommandHandler
from app.logic.handlers.texts.commands import SendTextMessageToChatBotCommandHandler
from app.logic.types.handlers import (
    UT,
    CommandHandlerMapping,
    EventHandlerMapping,
)
from app.settings.config import (
    Settings,
    get_settings,
)

logger = logging.getLogger(__name__)


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_mapping_and_command_handlers(self) -> "CommandHandlerMapping":
        """
        Here you have to link commands and command handlers for future inject in Bootstrap
        """
        return cast(
            "CommandHandlerMapping",
            {
                SendTextMessageToChatBotCommand: SendTextMessageToChatBotCommandHandler,
                ColorizeImageCommand: ColorizeImageCommandHandler
            },
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> "EventHandlerMapping":
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(
            "EventHandlerMapping",
            {},
        )


class DatabaseProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_engine_client(self, settings: Settings) -> AsyncEngine:
        engine: AsyncEngine = create_async_engine(
            url=settings.database.url,
            pool_pre_ping=settings.alchemy_settings.pool_pre_ping,
            pool_recycle=settings.alchemy_settings.pool_recycle,
            echo=settings.alchemy_settings.echo,
        )

        logger.debug("Successfully connected to Database")

        return engine

    @provide(scope=Scope.APP)
    async def get_session_maker(self, engine: AsyncEngine, settings: Settings) -> async_sessionmaker[AsyncSession]:
        session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            autoflush=settings.alchemy_settings.auto_flush,
            expire_on_commit=settings.alchemy_settings.expire_on_commit,
        )

        return session_maker


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_users_uow(self, session_maker: async_sessionmaker[AsyncSession]) -> UsersUnitOfWork:
        return SQLAlchemyUsersUnitOfWork(session_factory=session_maker)

    @provide(scope=Scope.APP)
    async def get_colorization_model(self, settings: Settings) -> LLMImageMessageColorizationModel:
        return KerasImageMessageColorizationModel(
            Path(settings.models.path_to_colorization_model)
        )

    @provide(scope=Scope.APP)
    async def get_image_factory(self) -> ImageCommandFactory:
        return ImageCommandFactory(
            {ImageCLickAction.gray_to_color: ColorizeImageCommand}
        )

    @provide(scope=Scope.APP)
    async def get_openai_provider(self, settings: Settings) -> LLMTextMessageModel:
        client: AsyncOpenAI = AsyncOpenAI(
            base_url=settings.openai.base_url,
            api_key=settings.openai.api_key,
        )

        return OpenAITextMessageModel(
            client=client,
            model=settings.openai.default_model,
        )

    @provide(scope=Scope.APP)
    async def get_text_service(self, message_model: LLMTextMessageModel) -> TextMessageService:
        return TextMessageService(chat_bot_model=message_model)

    @provide(scope=Scope.APP)
    async def get_image_service(self, image_colorization_model: LLMImageMessageColorizationModel) -> ImageService:
        return ImageService(colorize_image_model=image_colorization_model)

    @provide(scope=Scope.APP)
    async def get_job_factory(self) -> JobFactory:
        images_tasks_module: ModuleType = importlib.import_module("app.application.jobs.images.tasks")

        return JobFactory(
            {ColorizeImageCommand: getattr(images_tasks_module, "colorize_photo")},
        )

    @provide(scope=Scope.APP)
    async def get_bootstrap(
        self,
        events: EventHandlerMapping,
        commands: CommandHandlerMapping,
        uow: UT,
        text_service: TextMessageService,
        image_service: ImageService,
        job_factory: JobFactory,
    ) -> Bootstrap[UT]:
        return Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={"text_service": text_service, "image_service": image_service, "job_factory": job_factory},
        )


@lru_cache(maxsize=1)
def get_container() -> AsyncContainer:
    return make_async_container(
        HandlerProvider(), DatabaseProvider(), AppProvider(), context={Settings: get_settings()}
    )
