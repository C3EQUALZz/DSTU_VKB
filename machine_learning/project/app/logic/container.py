import logging
from functools import lru_cache
from typing import cast

from dishka import (
    AsyncContainer,
    from_context,
    make_async_container,
    provide,
    Provider,
    Scope,
)
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.infrastructure.integrations.llm.message.text.base import LLMTextMessageProvider
from app.infrastructure.integrations.llm.message.text.open_ai import OpenAITextMessageProvider
from app.infrastructure.uow.users.alchemy import SQLAlchemyUsersUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.messages import SendTextMessageToChatBot
from app.logic.handlers.messages.commands import SendTextMessageCommandHandler
from app.logic.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
    UT,
)
from app.settings.config import (
    get_settings,
    Settings,
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
                SendTextMessageToChatBot: SendTextMessageCommandHandler,
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
    async def get_openai_provider(self, settings: Settings) -> LLMTextMessageProvider:
        client: AsyncOpenAI = AsyncOpenAI(
            base_url=settings.openai.base_url,
            api_key=settings.openai.api_key,
        )

        return OpenAITextMessageProvider(
            client=client,
            model=settings.openai.default_model,
        )

    @provide(scope=Scope.APP)
    async def get_bootstrap(
        self, events: EventHandlerMapping, commands: CommandHandlerMapping, uow: UT, text_llm: LLMTextMessageProvider
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
