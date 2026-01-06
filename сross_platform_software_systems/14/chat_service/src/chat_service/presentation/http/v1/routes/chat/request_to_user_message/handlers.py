from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status

router: Final[APIRouter] = APIRouter(
    tags=["Chat"],
    route_class=DishkaRoute
)


@router.post(
    "/{chat_id}/request/",
    status_code=status.HTTP_201_CREATED,
    summary="Request on a user message",
)
async def request_on_user_message(
        
):
    ...
