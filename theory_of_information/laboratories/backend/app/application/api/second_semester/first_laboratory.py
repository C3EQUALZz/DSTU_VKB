from fastapi import APIRouter

router = APIRouter(
    prefix="/second_semester/first_laboratory",
    tags=["second_semester", "first_laboratory"]
)


@router.post("/encode/{data}")
async def encode(data: str) -> str:
    ...


@router.post("/decode/{data}")
async def decode(data: str) -> str:
    ...
