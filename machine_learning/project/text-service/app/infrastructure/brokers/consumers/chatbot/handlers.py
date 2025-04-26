from typing import Final

from dishka import FromDishka
from faststream.kafka import KafkaRouter
from faststream.kafka.annotations import KafkaMessage
from app.logic.bootstrap import Bootstrap
from app.logic.commands.text import SendTextMessageToChatBotAndThenReplyInMessengerCommand
from app.logic.dtos.chatbot import MessageAndChatIDDTO
from app.logic.message_bus import MessageBus
from app.settings.config import get_settings, Settings

router: Final[KafkaRouter] = KafkaRouter()
settings: Final[Settings] = get_settings()


@router.subscriber(
    settings.broker.text_chatbot_topic,
    group_id=settings.broker.text_chatbot_group_id,
    auto_commit=False
)
async def handle_text_to_chatbot(
        message: str,
        chat_id: int,
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap]
):
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        SendTextMessageToChatBotAndThenReplyInMessengerCommand(
            content=message,
            chat_id=chat_id,
        )
    )

    result: MessageAndChatIDDTO = message_bus.command_result

    await msg.ack()

    return result
