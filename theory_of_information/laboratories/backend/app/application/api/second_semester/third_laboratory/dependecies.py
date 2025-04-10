import io
from typing import cast

import numpy as np
from fastapi import UploadFile
from PIL import Image


async def convert_image_to_binary_matrix(
    image: UploadFile,
) -> np.ndarray[tuple[str, str, str]]:
    """
    Вспомогательная функция - dependency, которая переводит из отображения файла в матрицу.
    Она примерно выглядит так: [["11111111", "11111111", "11111111"], ["11111111", "11111111", "11111111"], ...]
    """
    image_bytes: bytes = await image.read()

    with Image.open(io.BytesIO(image_bytes)) as img:
        rgb_img: Image = img.convert("RGB")

        rgb_pixels: np.ndarray[tuple[int, int, int]] = cast(
            np.ndarray[tuple[int, int, int]], np.array(rgb_img.getdata())
        )

        return np.vectorize(lambda x: format(x, "08b"))(rgb_pixels)


async def convert_matrix_to_image(
    binary_array: np.ndarray[tuple[str, str, str]], width: int, height: int
) -> io.BytesIO:
    """
    Вспомогательная функция, которая переводит из массива обратно в изображение.
    Тут пришлось вводить такие параметры, как ширина и высота, потому что без этого Pillow выдает ValueError/
    """
    numeric_pixels: np.ndarray[np.ndarray[int]] = np.vectorize(
        lambda b: int(b, 2), otypes=[np.uint8]
    )(binary_array)

    reshaped: np.ndarray[np.ndarray[int]] = numeric_pixels.reshape((width, height, 3))

    image: Image = Image.fromarray(reshaped, "RGB")

    img_bytes: io.BytesIO = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes
