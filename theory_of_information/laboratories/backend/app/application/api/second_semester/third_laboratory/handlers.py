import logging

import numpy as np
from app.application.api.second_semester.third_laboratory.dependecies import (
    convert_image_to_binary_matrix, convert_matrix_to_image)
from app.application.api.second_semester.third_laboratory.schemas import (
    DecodeCascadeCodeRequestSchema, EncodeCascadeCodeRequestSchema,
    ShowNoisyImageSchemaRequest)
from app.exceptions.base import ApplicationException
from app.logic.commands.cascade_codes import (DecodeCascadeCodeCommand,
                                              EncodeCascadeCodeCommand,
                                              ShowNoisyImageCommand)
from app.logic.use_cases.cascade_codes import (DecodeCascadeCodeUseCase,
                                               EncodeCascadeCodeUseCase,
                                               ShowNoisyImageUseCase)
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Form, HTTPException
from starlette import status
from starlette.responses import StreamingResponse

router = APIRouter(
    prefix="/second_semester/third_laboratory",
    tags=["second_semester", "third_laboratory"],
    route_class=DishkaRoute,
)

logger = logging.getLogger(__name__)


@router.post(
    "/encode",
    status_code=status.HTTP_201_CREATED,
    description="This handler is using for encode image using cascade code",
)
async def encode_cascade_code(
    use_case: FromDishka[EncodeCascadeCodeUseCase],
    schemas: EncodeCascadeCodeRequestSchema = Form(...),
    pixels: np.ndarray[tuple[str, str, str]] = Depends(convert_image_to_binary_matrix),
) -> str:
    try:
        return await use_case(
            EncodeCascadeCodeCommand(
                data=pixels,
                matrix_for_block_code=schemas.matrix,
                type_of_matrix=schemas.type_matrix,
                indexes=schemas.indexes,
                add_errors=True,
            )
        )
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.post(
    "/decode",
    status_code=status.HTTP_200_OK,
    description="This handler is using for decode image using cascade code",
)
async def decode_cascade_code(
    use_case: FromDishka[DecodeCascadeCodeUseCase],
    schemas: DecodeCascadeCodeRequestSchema,
) -> StreamingResponse:
    try:
        result = await use_case(
            DecodeCascadeCodeCommand(
                data=schemas.data,
                matrix_for_block_code=schemas.matrix,
                type_of_matrix=schemas.type_matrix,
                indexes=schemas.indexes,
            )
        )

        return StreamingResponse(
            content=await convert_matrix_to_image(
                binary_array=result,
                width=schemas.image_width,
                height=schemas.image_height,
            ),
            media_type="image/png",
        )

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.post(
    "/show-noisy",
    status_code=status.HTTP_200_OK,
    description="This handler is using for show noisy image using cascade code",
)
async def show_noisy_image(
    use_case: FromDishka[ShowNoisyImageUseCase],
    schemas: ShowNoisyImageSchemaRequest = Form(...),
    pixels: np.ndarray[tuple[str, str, str]] = Depends(convert_image_to_binary_matrix),
) -> StreamingResponse:
    try:
        result = await use_case(
            ShowNoisyImageCommand(
                data=pixels,
            )
        )

        return StreamingResponse(
            content=await convert_matrix_to_image(
                binary_array=result,
                width=schemas.image_width,
                height=schemas.image_height,
            ),
            media_type="image/png",
        )

    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))
