from fastapi import APIRouter, HTTPException, UploadFile, File, status, Form

from combined_languages.theory_of_information.backend.fifth_semestr.first_laboratory.model import Model

router = APIRouter(
    prefix="/fifth_semester/first_laboratory",
    tags=["Пятый семестр", "1 лабораторная"],
)


@router.post("/histogram")
async def create_histogram_and_get_entropy(
        file: UploadFile = File(...),
        ignore_pattern: str = Form(...)
):
    try:
        file_content = await file.read()

        model = Model(file_content.decode('utf-8'), ignore_pattern)
        histogram = model.create_histogram()
        return {"histogram": histogram}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/entropy")
async def calculate_entropy(
        file: UploadFile = File(...),
        ignore_pattern: str = Form(...)
) -> dict[str, float]:
    try:
        file_content = await file.read()

        model = Model(file_content.decode('utf-8'), ignore_pattern)
        entropy = model.calculate_entropy()
        return {"entropy": entropy}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
