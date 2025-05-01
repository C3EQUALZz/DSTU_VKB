import io
import logging
from logging import Logger
from typing import Final, Annotated, cast

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import StreamingResponse

from app.application.api.v1.dependecies import get_image_dimensions
from app.application.api.v1.dtos import FileWithDimensions
from app.domain.entities.image import ImageEntity
from app.logic.bootstrap import Bootstrap
from app.logic.commands.colorization import ConvertColorToGrayScaleCommand
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
        headers={'Content-Disposition': f'attachment; filename="{image_entity.name}"'},
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
        headers={'Content-Disposition': f'attachment; filename="{image_entity.name}"'},
        media_type="image/png",
    )
