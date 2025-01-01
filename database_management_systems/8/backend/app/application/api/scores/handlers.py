from fastapi import APIRouter
from starlette import status

from dishka.integrations.fastapi import DishkaRoute


router = APIRouter(
    prefix="/scores",
    tags=["scores"],
    route_class=DishkaRoute,
)


@router.post(
    "/{user_id}/",
    status_code=status.HTTP_201_CREATED,
    responses={

    },
    summary="Creates or adds a new score for the player",
)
async def create_score(user_id: str):
    ...


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Gets all scores for each player",
)
async def get_all_scores(page_number: int = 1, page_size: int = 10):
    ...


@router.get(
    "/{score_id}/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Gets a score by his id",
)
async def get_score_by_id(score_id: str):
    ...


@router.patch(
    "/{score_id}/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Updates a score by his id",
)
async def update_score(score_id: str):
    ...


@router.delete(
    "/{score_id}/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Deletes a score by his id",
)
async def delete_score(score_id: str):
    ...


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Gets a user's score by his id",
)
async def get_user_score(user_id: str):
    ...
