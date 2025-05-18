from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.api.v1 import router_v1

router: Final[APIRouter] = APIRouter(
    prefix="/api",
    tags=["api"],
    route_class=DishkaRoute,
)

router.include_router(
    router_v1
)
