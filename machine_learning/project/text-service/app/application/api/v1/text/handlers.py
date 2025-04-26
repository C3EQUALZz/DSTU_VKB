from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status

from app.application.api.v1.text.schemas import TextMessageResponseSchemas, TextMessageRequestSchema
from app.logic.bootstrap import Bootstrap
from app.logic.commands.text import SendTextMessageToChatBotCommand
from app.logic.message_bus import MessageBus

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
    route_class=DishkaRoute
)


@router.post(
    "/text/",
    description="Handler for sending info for chat model",
    status_code=status.HTTP_200_OK,
)
async def send_message_to_chat_bot(
        schemas: TextMessageRequestSchema,
        bootstrap: FromDishka[Bootstrap]
) -> TextMessageResponseSchemas:
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        SendTextMessageToChatBotCommand(content=schemas.text)
    )

    return TextMessageResponseSchemas.from_entity(message_bus.command_result)
