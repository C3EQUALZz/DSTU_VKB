import logging

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, HTTPException

from app.application.api.second_semester.second_laboratory.schemas import ConvolutionalCodeSchemaRequest
from app.exceptions.base import ApplicationException
from app.logic.commands.convolutional_codes import EncodeConvolutionalCodeCommand, DecodeConvolutionalCodeCommand
from app.logic.use_cases.convolutional_codes import EncodeConvolutionalCodeUseCase, DecodeConvolutionalCodeUseCase

router = APIRouter(
    prefix="/second_semester/second_laboratory",
    tags=["second_semester", "second_laboratory"],
    route_class=DishkaRoute
)

logger = logging.getLogger(__name__)


@router.post(
    "/encode",
    status_code=200,
    summary="This handler for encode data using viterbi algorithm",
)
async def encode(
        schema: ConvolutionalCodeSchemaRequest,
        use_case: FromDishka[EncodeConvolutionalCodeUseCase]
):
    try:
        command = EncodeConvolutionalCodeCommand(**schema.model_dump())
        return await use_case(command)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.post(
    "/decode",
    status_code=200,
    summary="This handler for decode data using viterbi algorithm",
)
async def decode(
        schema: ConvolutionalCodeSchemaRequest,
        use_case: FromDishka[DecodeConvolutionalCodeUseCase]
):
    try:
        command = DecodeConvolutionalCodeCommand(**schema.model_dump())
        return await use_case(command)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))
