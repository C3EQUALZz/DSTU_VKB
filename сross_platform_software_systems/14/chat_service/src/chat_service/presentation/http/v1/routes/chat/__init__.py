from typing import Final, Iterable

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from chat_service.presentation.http.v1.routes.chat.change_chat_llm_provider.handlers import (
    change_chat_llm_provider_router
)
from chat_service.presentation.http.v1.routes.chat.create_new_chat.handlers import create_new_chat_router
from chat_service.presentation.http.v1.routes.chat.request_to_user_message.handlers import (
    request_on_user_message_router
)

chat_router: Final[APIRouter] = APIRouter(
    prefix="/chat/",
    route_class=DishkaRoute,
    tags=["Chat"],
)

chat_sub_routers: Final[Iterable[APIRouter]] = (
    create_new_chat_router,
    change_chat_llm_provider_router,
    request_on_user_message_router
)

for sub_router in chat_sub_routers:
    chat_router.include_router(sub_router)
