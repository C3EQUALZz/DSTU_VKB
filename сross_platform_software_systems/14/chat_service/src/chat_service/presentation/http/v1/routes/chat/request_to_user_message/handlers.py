from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Depends
from starlette import status

from chat_service.application.commands.chat.request_to_message import (
    RequestOnUserMessageInChatCommandHandler,
    RequestOnUserMessageInChatCommand
)
from chat_service.application.common.views.chat.request_on_user_message import RequestOnUserMessageView
from chat_service.infrastructure.auth.headers_params import header_params
from chat_service.presentation.http.v1.routes.chat.request_to_user_message.schemas import (
    RequestToUserMessageRequestSchema,
    RequestToUserMessageResponseSchema
)

request_on_user_message_router: Final[APIRouter] = APIRouter(
    tags=["Chat"],
    route_class=DishkaRoute
)

ChatIDPathParameter = Path(
    title="The ID of the chat to update",
    description="The ID of the chat to update. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@request_on_user_message_router.post(
    "/{chat_id}/request/",
    status_code=status.HTTP_201_CREATED,
    summary="Request on a user message",
    response_model=RequestToUserMessageResponseSchema,
    dependencies=[Depends(header_params)]
)
async def request_on_user_message(
        chat_id: Annotated[UUID, ChatIDPathParameter],
        request_schema: RequestToUserMessageRequestSchema,
        interactor: FromDishka[RequestOnUserMessageInChatCommandHandler]
) -> RequestToUserMessageResponseSchema:
    command: RequestOnUserMessageInChatCommand = RequestOnUserMessageInChatCommand(
        content=request_schema.content,
        chat_id=chat_id,
    )

    view: RequestOnUserMessageView = await interactor(command)

    return RequestToUserMessageResponseSchema(
        user_message_id=view.user_message_id,
        assistant_message_id=view.assistant_message_id,
        assistant_message_content=view.assistant_message_content
    )
