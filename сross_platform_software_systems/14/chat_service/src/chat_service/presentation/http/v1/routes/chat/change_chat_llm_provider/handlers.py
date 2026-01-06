from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path
from starlette import status

from chat_service.application.commands.chat.change_chat_llm_provider import (
    ChangeLLMProviderCommandHandler,
    ChangeLLMProviderCommand
)
from chat_service.presentation.http.v1.routes.chat.change_chat_llm_provider.schemas import (
    ChangeChatLLMProviderRequestSchema
)

change_chat_llm_provider_router: Final[APIRouter] = APIRouter(
    tags=["Chat"],
    route_class=DishkaRoute
)

ChatIDPathParameter = Path(
    title="The ID of the chat to update",
    description="The ID of the chat to update. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@change_chat_llm_provider_router.patch(
    "/llm_provider/{chat_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_chat_llm_provider_handler(
        chat_id: Annotated[UUID, ChatIDPathParameter],
        request_schema: ChangeChatLLMProviderRequestSchema,
        interactor: FromDishka[ChangeLLMProviderCommandHandler]
) -> None:
    command: ChangeLLMProviderCommand = ChangeLLMProviderCommand(
        chat_id=chat_id,
        llm_provider=request_schema.llm_provider.value
    )

    await interactor(command)
