import io
import logging
from logging import Logger
from typing import Final, Annotated, cast

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, UploadFile, File
from starlette import status
from starlette.responses import StreamingResponse

from app.application.api.v1.dependecies import get_image_dimensions
from app.application.api.v1.dtos import FileWithDimensions
from app.domain.entities.image import ImageEntity
from app.logic.bootstrap import Bootstrap
from app.logic.commands.colorization import ConvertColorToGrayScaleCommand, StylizeCommand
from app.logic.message_bus import MessageBus

router: Final[APIRouter] = APIRouter(
    prefix="/colorization",
    tags=["colorization"],
    route_class=DishkaRoute,
)

logger: Final[Logger] = logging.getLogger(__name__)


@router.post(
    path="/gray-to-color/",
    status_code=status.HTTP_202_ACCEPTED,
    description="method which colorizes photo"
)
async def convert_grayscale_to_rgb(
        file_with_dimensions: Annotated[FileWithDimensions, Depends(get_image_dimensions)],
        bootstrap: FromDishka[Bootstrap]
) -> StreamingResponse:
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        ConvertColorToGrayScaleCommand(
            data=file_with_dimensions.data,
            width=file_with_dimensions.width,
            height=file_with_dimensions.height,
            name=file_with_dimensions.name,
        )
    )

    image_entity: ImageEntity = cast(ImageEntity, message_bus.command_result)

    return StreamingResponse(
        content=io.BytesIO(image_entity.data),
        headers={'Content-Disposition': f'attachment; filename="{image_entity.name.as_generic_type()}"'},
        media_type="image/png",
    )


@router.post(
    path="/color-to-gray/",
    status_code=status.HTTP_202_ACCEPTED,
    description="method which colorizes photo"
)
async def convert_rgb_to_grayscale(
        file_with_dimensions: Annotated[FileWithDimensions, Depends(get_image_dimensions)],
        bootstrap: FromDishka[Bootstrap]
) -> StreamingResponse:
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        ConvertColorToGrayScaleCommand(
            data=file_with_dimensions.data,
            width=file_with_dimensions.width,
            height=file_with_dimensions.height,
            name=file_with_dimensions.name,
        )
    )

    image_entity: ImageEntity = cast(ImageEntity, message_bus.command_result)

    return StreamingResponse(
        content=io.BytesIO(image_entity.data),
        headers={'Content-Disposition': f'attachment; filename="{image_entity.name.as_generic_type()}"'},
        media_type="image/png",
    )


@router.post(
    path="/style-image/",
    status_code=status.HTTP_202_ACCEPTED,
    description="method which styles photo"
)
async def style_image(
        bootstrap: FromDishka[Bootstrap],
        original_image: UploadFile = File(...),
        styling_template: UploadFile = File(...),
) -> StreamingResponse:
    # Обработка первого файла
    original_image_with_dimensions = await get_image_dimensions(original_image)

    # Обработка второго файла
    styling_template = await get_image_dimensions(styling_template)

    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(
        StylizeCommand(
            original_image_data=original_image_with_dimensions.data,
            original_width=original_image_with_dimensions.width,
            original_height=original_image_with_dimensions.height,
            original_name=original_image_with_dimensions.name,
            style_image_data=styling_template.data,
            style_width=styling_template.width,
            style_height=styling_template.height,
            style_name=styling_template.name,
        )
    )

    image_entity: ImageEntity = cast(ImageEntity, message_bus.command_result)

    return StreamingResponse(
        content=io.BytesIO(image_entity.data),
        headers={'Content-Disposition': f'attachment; filename="{image_entity.name.as_generic_type()}"'},
        media_type="image/png",
    )
