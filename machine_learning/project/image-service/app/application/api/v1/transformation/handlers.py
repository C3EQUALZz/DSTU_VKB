import io
import logging
from logging import Logger
from typing import Final, Annotated, cast

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.params import Query
from starlette import status
from starlette.responses import StreamingResponse

from app.application.api.v1.dependecies import get_image_dimensions
from app.application.api.v1.dtos import FileWithDimensions
from app.domain.entities.image import ImageEntity
from app.logic.bootstrap import Bootstrap
from app.logic.commands.transform import CropImageCommand, RotateImageCommand
from app.logic.message_bus import MessageBus

router: Final[APIRouter] = APIRouter(
    prefix="/transformation",
    tags=["transformation"],
    route_class=DishkaRoute,
)

logger: Final[Logger] = logging.getLogger(__name__)


@router.post(
    "/crop",
    status_code=status.HTTP_202_ACCEPTED,
    description="method which crops photo"
)
async def crop_image(
        file_with_dimensions: Annotated[FileWithDimensions, Depends(get_image_dimensions)],
        bootstrap: FromDishka[Bootstrap],
        new_width: int = Query(gt=1, description="new image width"),
        new_height: int = Query(gt=1, description="new image height"),
) -> StreamingResponse:
    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(
        CropImageCommand(
            data=file_with_dimensions.data,
            old_width=file_with_dimensions.width,
            old_height=file_with_dimensions.height,
            name=file_with_dimensions.name,
            new_width=new_width,
            new_height=new_height,
        )
    )

    image_entity: ImageEntity = cast(ImageEntity, message_bus.command_result)

    return StreamingResponse(
        content=io.BytesIO(image_entity.data),
        headers={'Content-Disposition': f'attachment; filename="{image_entity.name.as_generic_type()}"'},
        media_type="image/png",
    )


@router.post(
    "/rotate",
    status_code=status.HTTP_202_ACCEPTED,
    description="method which rotates photo"
)
async def rotate_image(
        file_with_dimensions: Annotated[FileWithDimensions, Depends(get_image_dimensions)],
        bootstrap: FromDishka[Bootstrap],
        angle: int = Query(gt=0, le=360, description="rotation angle"),
) -> StreamingResponse:
    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(
        RotateImageCommand(
            data=file_with_dimensions.data,
            angle=angle,
            name=file_with_dimensions.name,
            width=file_with_dimensions.width,
            height=file_with_dimensions.height,
        )
    )

    image_entity: ImageEntity = cast(ImageEntity, message_bus.command_result)

    return StreamingResponse(
        content=io.BytesIO(image_entity.data),
        headers={'Content-Disposition': f'attachment; filename="{image_entity.name.as_generic_type()}"'},
        media_type="image/png",
    )
