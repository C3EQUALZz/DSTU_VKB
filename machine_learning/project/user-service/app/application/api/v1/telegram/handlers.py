from typing import Final

from authx import TokenPayload
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status
from starlette.responses import RedirectResponse

from app.application.api.v1.auth.dependencies import RoleChecker, get_access_token_payload
from app.application.api.v1.auth.handlers import get_me
from app.domain.entities.user import UserEntity
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.views.users import UsersViews
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
    dependencies=[Depends(RoleChecker(allowed_roles=["admin", "user"]))],
)
async def run_bot(
        uow: FromDishka[UsersUnitOfWork],
        token: TokenPayload = Depends(get_access_token_payload),
        settings: Settings = Depends(get_settings)
) -> RedirectResponse:
    users_views: UsersViews = UsersViews(uow=uow)
    user: UserEntity = await users_views.get_user_by_id(token.sub)

    return RedirectResponse(
        url=f"{settings.telegram.url}?start={user.oid}",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )
