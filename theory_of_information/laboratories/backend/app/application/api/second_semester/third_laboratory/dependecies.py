import io
from typing import cast

import numpy as np
from PIL import Image
from fastapi import UploadFile


async def convert_image_to_binary_matrix(image: UploadFile) -> np.ndarray[tuple[str, str, str]]:
    """
    Вспомогательная функция - dependency, которая переводит из отображения файла в матрицу.
    Она примерно выглядит так: [["11111111", "11111111", "11111111"], ["11111111", "11111111", "11111111"], ...]
    """
    image_bytes: bytes = await image.read()

    with Image.open(io.BytesIO(image_bytes)) as img:
        rgb_img: Image = img.convert('RGB')
        rgb_pixels: np.ndarray[tuple[int, int, int]] = cast(np.ndarray[tuple[int, int, int]],
                                                            np.array(rgb_img.getdata()))
        return np.vectorize(lambda x: format(x, '08b'))(rgb_pixels)
