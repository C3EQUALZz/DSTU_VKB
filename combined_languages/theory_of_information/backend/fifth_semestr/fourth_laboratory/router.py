from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/fifth_semester/fourth_laboratory",
    tags=["Пятый семестр", "4 лабораторная"]
)


@router.post("/")
async def process(text: str, type_matrix: str):
    ...
