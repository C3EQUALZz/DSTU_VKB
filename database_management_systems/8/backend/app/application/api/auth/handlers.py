from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status

from app.application.api.auth.schemas import UserLoginSchemaRequest

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute
)


@router.post(
    "/login/",
    status_code=status.HTTP_201_CREATED
)
async def login(schema: UserLoginSchemaRequest):
    ...


@router.post("/register/")
async def register(schema):
    ...
