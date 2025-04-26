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

from faststream.kafka import KafkaBroker
from openai import AsyncOpenAI

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.factory import EventHandlerTopicFactory
from app.infrastructure.brokers.publishers.faststream import FastStreamKafkaMessageBroker
from app.infrastructure.integrations.text_large_learning_models.base import LLMTextMessageModel
from app.infrastructure.integrations.text_large_learning_models.openai import OpenAITextMessageModel
from app.infrastructure.integrations.translation.base import Translator
from app.infrastructure.integrations.translation.google import GoogleTranslation
from app.infrastructure.services.text import TextMessageService
from app.logic.bootstrap import Bootstrap
from app.logic.commands.text import SendTextMessageToChatBotCommand, \
    SendTextMessageToChatBotAndThenReplyInMessengerCommand
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.text.commands import SendTextMessageToChatBotCommandHandler, \
    SendTextMessageToChatBotAndThenReplyInMessengerCommandHandler
from app.logic.types.handlers import (
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
                SendTextMessageToChatBotAndThenReplyInMessengerCommand: SendTextMessageToChatBotAndThenReplyInMessengerCommandHandler
            },
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> "EventHandlerMapping":
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(
            "EventHandlerMapping",
            {

            },
        )


class BrokerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_kafka_broker(self, settings: Settings) -> KafkaBroker:
        return KafkaBroker(settings.broker.url)

    @provide(scope=Scope.APP)
    async def get_mapping_events_and_topic(self, settings: Settings) -> EventHandlerTopicFactory:
        return EventHandlerTopicFactory(
            mapping={

            }
        )

    @provide(scope=Scope.APP)
    async def get_producer(
            self,
            settings: Settings,
            broker: KafkaBroker,
    ) -> BaseMessageBroker:

        return FastStreamKafkaMessageBroker(
            broker=broker,
            producers={
                settings.broker.text_translate_topic: broker.publisher(settings.broker.text_translate_topic),
                settings.broker.text_chatbot_topic: broker.publisher(settings.broker.text_chatbot_topic),
            }
        )


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

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
    async def get_translator(self) -> Translator:
        return GoogleTranslation()

    @provide(scope=Scope.APP)
    async def get_text_service(self, message_model: LLMTextMessageModel, translator: Translator) -> TextMessageService:
        return TextMessageService(chat_bot_model=message_model, translator=translator)

    @provide(scope=Scope.APP)
    async def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            text_service: TextMessageService,
    ) -> Bootstrap:
        return Bootstrap(
            event_buffer=EventBuffer(),
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={"text_service": text_service},
        )


@lru_cache(maxsize=1)
def get_container() -> AsyncContainer:
    return make_async_container(
        HandlerProvider(), AppProvider(), BrokerProvider(), context={Settings: get_settings()}
    )
