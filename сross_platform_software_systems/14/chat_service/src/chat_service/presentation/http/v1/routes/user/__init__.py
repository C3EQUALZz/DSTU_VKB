from typing import Final, Iterable

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from chat_service.presentation.http.v1.routes.user.change_openrouter_api_key.handlers import (
    change_openrouter_api_key_router
)

user_router: Final[APIRouter] = APIRouter(
    prefix="/user/",
    route_class=DishkaRoute,
    tags=["User"],
)

user_sub_routers: Final[Iterable[APIRouter]] = (
    change_openrouter_api_key_router,
)

for sub_router in user_sub_routers:
    user_router.include_router(sub_router)
