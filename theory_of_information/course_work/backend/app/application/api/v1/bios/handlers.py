import logging
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from app.exceptions.infrastructure import UserNotFoundException

router = APIRouter(prefix="/bios", tags=["bios"], route_class=DishkaRoute)
logger = logging.getLogger(__name__)


@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_bios():
    ...


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_bio(

):
    ...


@router.patch(
    "/{bio_id}/",
    status_code=status.HTTP_200_OK
)
async def update_bio(bio_id: UUID):
    ...


@router.delete(
    "/{bio_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    },
)
async def delete(bio_id: UUID):
    ...
