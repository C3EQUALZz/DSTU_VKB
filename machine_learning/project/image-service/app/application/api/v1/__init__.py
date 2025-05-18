from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.api.v1.colorization.handlers import router as router_colorization_v1
from app.application.api.v1.transformation.handlers import router as router_handlers_v1

router_v1: Final[APIRouter] = APIRouter(prefix="/v1/image", tags=["v1"], route_class=DishkaRoute)
router_v1.include_router(router_colorization_v1)
router_v1.include_router(router_handlers_v1)
