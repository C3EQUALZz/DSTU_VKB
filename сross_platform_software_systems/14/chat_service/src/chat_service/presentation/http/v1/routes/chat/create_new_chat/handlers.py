from typing import Final

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from chat_service.application.commands.chat.create_new_chat import (
    CreateNewChatCommandHandler,
    CreateNewChatCommand
)
from chat_service.application.common.views.chat.create_chat_view import CreateChatView
from chat_service.presentation.http.v1.routes.chat.create_new_chat.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema
)

create_new_chat_router: Final[APIRouter] = APIRouter(
    tags=["Chat"],
    route_class=DishkaRoute
)


@create_new_chat_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create new chat handler",
    response_model=CreateChatResponseSchema
)
async def create_chat_handler(
        request_schema: CreateChatRequestSchema,
        interactor: FromDishka[CreateNewChatCommandHandler],
) -> CreateChatResponseSchema:
    command: CreateNewChatCommand = CreateNewChatCommand(
        llm_provider=request_schema.llm_provider.value if request_schema.llm_provider else None,
    )

    view: CreateChatView = await interactor(command)

    return CreateChatResponseSchema(
        chat_id=view.chat_id,
    )
