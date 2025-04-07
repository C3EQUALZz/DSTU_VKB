import logging

import numpy as np
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Form, HTTPException
from starlette import status

from app.application.api.second_semester.third_laboratory.dependecies import convert_image_to_binary_matrix
from app.application.api.second_semester.third_laboratory.schemas import EncodeCascadeCodeRequestSchema, \
    DecodeCascadeCodeRequestSchema
from app.exceptions.base import ApplicationException
from app.logic.commands.block_codes import EncodeCascadeCodeCommand, DecodeCascadeCodeCommand
from app.logic.use_cases.cascade_codes import EncodeCascadeCodeUseCase, DecodeCascadeCodeUseCase

router = APIRouter(
    prefix="/second_semester/third_laboratory",
    tags=["second_semester", "third_laboratory"],
    route_class=DishkaRoute
)

logger = logging.getLogger(__name__)


@router.post(
    "/encode",
    status_code=status.HTTP_201_CREATED,
    description="This handler is using for encode image using cascade code"
)
async def encode_cascade_code(
        use_case: FromDishka[EncodeCascadeCodeUseCase],
        schemas: EncodeCascadeCodeRequestSchema = Form(...),
        pixels: np.ndarray[tuple[str, str, str]] = Depends(convert_image_to_binary_matrix),
):
    try:
        return await use_case(EncodeCascadeCodeCommand(
            data=pixels,
            matrix_for_block_code=schemas.matrix,
            type_of_matrix=schemas.type_matrix,
        ))
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.post(
    "/decode",
    status_code=status.HTTP_200_OK,
    description="This handler is using for decode image using cascade code"
)
async def decode_cascade_code(
        use_case: FromDishka[DecodeCascadeCodeUseCase],
        schemas: DecodeCascadeCodeRequestSchema,
):
    try:
        return await use_case(DecodeCascadeCodeCommand(
            data=schemas.data,
            matrix_for_block_code=schemas.matrix,
            type_of_matrix=schemas.type_matrix,
        ))

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))
