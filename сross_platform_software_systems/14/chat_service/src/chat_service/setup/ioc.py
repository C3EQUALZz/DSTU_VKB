from typing import Final, Iterable

from bazario.asyncio import Registry, Dispatcher
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import Provider, Scope, WithParents
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from chat_service.application.commands.chat.change_chat_llm_provider import ChangeLLMProviderCommandHandler
from chat_service.application.commands.chat.create_new_chat import CreateNewChatCommandHandler
from chat_service.application.commands.chat.request_to_message import RequestOnUserMessageInChatCommandHandler
from chat_service.application.commands.user.change_username import ChangeUserNameCommandHandler
from chat_service.application.commands.user.create_user import CreateUserCommandHandler
from chat_service.application.commands.user.delete_user_by_id import DeleteUserByIDCommandHandler
from chat_service.application.common.ports.chat.chat_command_gateway import ChatCommandGateway
from chat_service.application.common.ports.chat.chat_query_gateway import ChatQueryGateway
from chat_service.application.common.ports.chat.openrouter_gateway import OpenRouterGateway
from chat_service.application.common.ports.event_bus import EventBus
from chat_service.application.common.ports.identity_provider import IdentityProvider
from chat_service.application.common.ports.transaction_manager import TransactionManager
from chat_service.application.common.ports.user.user_command_gateway import UserCommandGateway
from chat_service.application.common.ports.user.user_query_gateway import UserQueryGateway
from chat_service.application.common.services.current_user_service import CurrentUserService
from chat_service.domain.chat.ports.chat_id_generator import ChatIDGenerator
from chat_service.domain.chat.ports.message_id_generator import MessageIDGenerator
from chat_service.domain.chat.services.chat_service import ChatService
from chat_service.domain.chat.services.message_service import MessageService
from chat_service.domain.user.services.access_service import AccessService
from chat_service.domain.user.services.user_service import UserService
from chat_service.infrastructure.adapters.auth.header_identity_provider import HeaderIdentityProvider
from chat_service.infrastructure.adapters.common.bazario_event_bus import BazarioEventBus
from chat_service.infrastructure.adapters.common.uuid4_chat_id_generator import UUID4ChatIDGenerator
from chat_service.infrastructure.adapters.common.uuid4_message_id_generator import UUID4MessageIDGenerator
from chat_service.infrastructure.adapters.openrouter_api.chat_message_formatter import ChatMessageFormatter
from chat_service.infrastructure.adapters.openrouter_api.openai_openrouter_gateway import OpenAIOpenRouterGateway
from chat_service.infrastructure.adapters.openrouter_api.provider import get_openrouter_client
from chat_service.infrastructure.adapters.persistence.alchemy_chat_command_gateway import SqlAlchemyChatCommandGateway
from chat_service.infrastructure.adapters.persistence.alchemy_chat_query_gateway import SqlAlchemyChatQueryGateway
from chat_service.infrastructure.adapters.persistence.alchemy_transaction_manager import SqlAlchemyTransactionManager
from chat_service.infrastructure.adapters.persistence.alchemy_user_command_gateway import SqlAlchemyUserCommandGateway
from chat_service.infrastructure.adapters.persistence.alchemy_user_query_gateway import SqlAlchemyUserQueryGateway
from chat_service.infrastructure.persistence.provider import get_session, get_sessionmaker, get_engine
from chat_service.setup.config.asgi import ASGIConfig
from chat_service.setup.config.database import PostgresConfig, SQLAlchemyConfig
from chat_service.setup.config.openrouter import OpenRouterConfig


def configs_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.from_context(provides=ASGIConfig)
    provider.from_context(provides=PostgresConfig)
    provider.from_context(provides=SQLAlchemyConfig)
    provider.from_context(provides=OpenRouterConfig)
    return provider


def db_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, provides=AsyncSession)
    return provider


def auth_ports_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.from_context(provides=Request, scope=Scope.REQUEST)
    provider.provide_all(CurrentUserService)
    provider.provide(source=HeaderIdentityProvider, provides=IdentityProvider)
    return provider


def gateways_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(source=SqlAlchemyTransactionManager, provides=TransactionManager)
    provider.provide(source=SqlAlchemyUserCommandGateway, provides=UserCommandGateway)
    provider.provide(source=SqlAlchemyUserQueryGateway, provides=UserQueryGateway)
    provider.provide(source=SqlAlchemyChatCommandGateway, provides=ChatCommandGateway)
    provider.provide(source=SqlAlchemyChatQueryGateway, provides=ChatQueryGateway)
    return provider


def openrouter_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(get_openrouter_client)
    provider.provide(source=OpenAIOpenRouterGateway, provides=OpenRouterGateway)
    provider.provide(source=ChatMessageFormatter)
    return provider


def domain_ports_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(source=UUID4MessageIDGenerator, provides=MessageIDGenerator)
    provider.provide(source=UUID4ChatIDGenerator, provides=ChatIDGenerator)

    provider.provide_all(
        UserService,
        AccessService,
        ChatService,
        MessageService
    )

    return provider

def registry_provider() -> Registry:
    registry: Final[Registry] = Registry()
    return registry


def event_bus_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(registry_provider)
    provider.provide(BazarioEventBus, provides=EventBus)
    provider.provide(WithParents[Dispatcher])
    provider.provide(WithParents[DishkaResolver])
    return provider


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)

    provider.provide_all(
        ChangeLLMProviderCommandHandler,
        CreateNewChatCommandHandler,
        RequestOnUserMessageInChatCommandHandler,
        ChangeUserNameCommandHandler,
        CreateUserCommandHandler,
        DeleteUserByIDCommandHandler
    )

    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        configs_provider(),
        domain_ports_provider(),
        openrouter_provider(),
        auth_ports_provider(),
        gateways_provider(),
        event_bus_provider(),
        interactors_provider(),
    )
