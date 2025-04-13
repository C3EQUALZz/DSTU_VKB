import logging
from functools import lru_cache
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

from app.infrastructure.integrations.llm.message.text.base import LLMTextMessageModel
from app.infrastructure.integrations.llm.message.text.open_ai import OpenAITextMessageModek
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
    async def get_openai_provider(self, settings: Settings) -> LLMTextMessageModel:
        client: AsyncOpenAI = AsyncOpenAI(
            base_url=settings.openai.base_url,
            api_key=settings.openai.api_key,
        )

        return OpenAITextMessageModek(
            client=client,
            model=settings.openai.default_model,
        )

    @provide(scope=Scope.APP)
    async def get_bootstrap(
        self, events: EventHandlerMapping, commands: CommandHandlerMapping, uow: UT, text_llm: LLMTextMessageModel
    ) -> Bootstrap[UT]:
        return Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={"text_llm": text_llm},
        )


@lru_cache(maxsize=1)
def get_container() -> AsyncContainer:
    return make_async_container(
        HandlerProvider(), DatabaseProvider(), AppProvider(), context={Settings: get_settings()}
    )
