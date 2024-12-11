from fastapi import APIRouter, HTTPException

from combined_languages.theory_of_information.backend.fifth_semestr.fifth_laboratory.dependecies import execute
from combined_languages.theory_of_information.backend.fifth_semestr.fifth_laboratory.schemas import LaboratoryRequest

router = APIRouter(
    prefix="/fifth_semester/fifth_laboratory",
    tags=["Пятый семестр", "5 лабораторная"]
)


@router.post("/")
async def process(request_body: LaboratoryRequest):
    try:
        result = execute(
            request_body.algorithm,
            request_body.matrix,
            request_body.type_matrix,
            request_body.indexes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
