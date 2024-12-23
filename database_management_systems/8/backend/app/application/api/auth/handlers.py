from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login/")
async def login(schema):
    ...


@router.post("/register/")
async def register(schema):
    ...
