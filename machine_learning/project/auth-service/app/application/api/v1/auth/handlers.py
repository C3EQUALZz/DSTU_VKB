from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status

from app.application.api.v1.auth.schemas import CreateUserSchemaRequest

router: Final[APIRouter] = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint for user registration"
)
async def register(
        schemas: CreateUserSchemaRequest,
        
):
    ...
