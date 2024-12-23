from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
)


@router.post("/")
async def create_user():
    ...


@router.get("/")
async def get_users():
    ...


@router.get("/{user_id}")
async def get_user(user_id: int):
    ...


@router.patch("/{user_id}")
async def update_user(user_id: int):
    ...


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    ...
