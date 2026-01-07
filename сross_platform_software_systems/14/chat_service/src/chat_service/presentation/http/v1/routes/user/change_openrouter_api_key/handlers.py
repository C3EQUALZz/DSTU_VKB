import logging
from typing import Final

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from starlette import status

from chat_service.application.commands.user.change_openrouter_api_key import (
    ChangeOpenRouterAPIKeyCommandHandler,
    ChangeOpenRouterAPIKeyCommand
)
from chat_service.infrastructure.auth.headers_params import header_params
from chat_service.presentation.http.v1.routes.user.change_openrouter_api_key.schemas import (
    ChangeOpenRouterAPIRequestSchema
)

change_openrouter_api_key_router: Final[APIRouter] = APIRouter(
    tags=["User"],
    route_class=DishkaRoute,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@change_openrouter_api_key_router.patch(
    path="/openrouter/api_key/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Change OpenRouter API Key",
    dependencies=[Depends(header_params)]
)
async def change_openrouter_api_key_handler(
        request_schema: ChangeOpenRouterAPIRequestSchema,
        interactor: FromDishka[ChangeOpenRouterAPIKeyCommandHandler]
) -> None:
    logger.info(
        "Started changing openrouter API key",
    )

    command: ChangeOpenRouterAPIKeyCommand = ChangeOpenRouterAPIKeyCommand(
        new_openrouter_api_key=request_schema.new_openrouter_api_key
    )

    await interactor(command)

    logger.info(
        "Finished changing openrouter API key",
    )
