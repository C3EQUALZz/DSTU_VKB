import logging

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette.exceptions import HTTPException

from app.application.api.second_semester.fourth_laboratory.schemas import MatrixEncodeRequestSchema, \
    PolynomEncodeRequestSchema, PolynomDecodeRequestSchema
from app.exceptions.base import ApplicationException
from app.logic.commands.cyclic_codes import EncodeCyclicCodeWithMatrixCommand, EncodeCyclicCodeWithPolynomCommand, \
    DecodeCyclicCodeWithPolynomCommand
from app.logic.use_cases.cyclic_codes import EncodeCyclicCodeMatrixUseCase, EncodeCyclicCodePolynomUseCase, \
    DecodeCyclicCodePolynomUseCase

router = APIRouter(
    prefix="/second_semester/fourth_laboratory",
    tags=["second_semester", "fourth_laboratory"],
    route_class=DishkaRoute
)

logger = logging.getLogger(__name__)


@router.post("/encode-matrix")
async def encode_with_matrix(
        schemas: MatrixEncodeRequestSchema,
        use_case: FromDishka[EncodeCyclicCodeMatrixUseCase]
):
    try:

        command: EncodeCyclicCodeWithMatrixCommand = EncodeCyclicCodeWithMatrixCommand(
            data=schemas.text,
            matrix=schemas.matrix,
        )

        return await use_case(command=command)

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e.message))


@router.post("/encode-polynomials")
async def encode_with_polynomials(
        schemas: PolynomEncodeRequestSchema,
        use_case: FromDishka[EncodeCyclicCodePolynomUseCase]
):
    try:

        command: EncodeCyclicCodeWithPolynomCommand = EncodeCyclicCodeWithPolynomCommand(
            data=schemas.text,
            polynom=schemas.polynom,
            n=schemas.n,
        )

        return await use_case(command=command)

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e.message))


@router.post("/decode-polynomials")
async def decode_with_polynomials(
        schemas: PolynomDecodeRequestSchema,
        use_case: FromDishka[DecodeCyclicCodePolynomUseCase]
):
    try:
        command: DecodeCyclicCodeWithPolynomCommand = DecodeCyclicCodeWithPolynomCommand(
            data=schemas.text,
            polynom=schemas.polynom,
            n=schemas.n,
        )

        return await use_case(command=command)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e.message))