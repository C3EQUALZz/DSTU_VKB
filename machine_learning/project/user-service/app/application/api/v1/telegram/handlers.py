from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status
from starlette.responses import RedirectResponse

from app.application.api.v1.auth.handlers import get_me
from app.domain.entities.user import UserEntity
from app.settings.config import Settings, get_settings

router: Final[APIRouter] = APIRouter(
    prefix="/telegram",
    tags=["telegram"],
    route_class=DishkaRoute,
)


@router.get(
    "/deep-link",
    description="HTTP URL for start telegram bot",
    status_code=status.HTTP_308_PERMANENT_REDIRECT,
    response_class=RedirectResponse,
)
async def run_bot(
        current_user: UserEntity = Depends(get_me),
        settings: Settings = Depends(get_settings)
) -> RedirectResponse:
    return RedirectResponse(
        url=f"{settings.telegram.url}?start={current_user.oid}",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )
