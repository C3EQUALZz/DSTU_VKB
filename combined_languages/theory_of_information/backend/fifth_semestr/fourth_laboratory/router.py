from typing import Mapping, AnyStr

from fastapi import Depends
from fastapi.routing import APIRouter

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.dependecies import execute

router = APIRouter(
    prefix="/fifth_semester/fourth_laboratory",
    tags=["Пятый семестр", "4 лабораторная"]
)


@router.post("/")
async def process(result: Mapping[AnyStr, AnyStr] = Depends(execute)) -> Mapping[AnyStr, AnyStr]:
    return result
