from typing import Annotated

import cv2
import numpy as np
from fastapi import UploadFile, File

from app.application.api.v1.dtos import FileWithDimensions
from app.exceptions.application import WrongFileFormatError, CantDecodeImageError, ImageProcessingError


async def get_image_dimensions(
        file: Annotated[UploadFile, File(description="A file read as UploadFile")]
) -> FileWithDimensions:
    if not file.content_type.startswith("image/"):
        raise WrongFileFormatError("content type must be image/, not {}".format(file.content_type))

    try:
        contents: bytes = await file.read()

        # Конвертация байтов в numpy array
        np_arr: np.ndarray = np.frombuffer(contents, np.uint8)

        # Декодирование изображения
        img: cv2.typing.MatLike = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise CantDecodeImageError("can't decode image")

        height, width = img.shape[:2]

        _, encoded_img = cv2.imencode(".jpg", img)

        return FileWithDimensions(
            data=encoded_img.tobytes(),
            width=width,
            height=height,
            name=file.filename,
        )

    except Exception as e:
        raise ImageProcessingError(e.args[0])
