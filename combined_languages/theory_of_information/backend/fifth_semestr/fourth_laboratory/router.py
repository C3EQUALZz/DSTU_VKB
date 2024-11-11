from fastapi import HTTPException
from fastapi.routing import APIRouter

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.dependecies import execute
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.schemas import (
    LaboratoryRequest,
)

router = APIRouter(
    prefix="/fifth_semester/fourth_laboratory",
    tags=["Пятый семестр", "4 лабораторная"]
)


@router.post(
    "/",
)
async def process(request_body: LaboratoryRequest):
    try:
        result = execute(
            word=request_body.word,
            matrix=request_body.matrix,
            type_matrix=request_body.type_matrix
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
