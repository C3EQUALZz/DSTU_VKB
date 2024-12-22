"""
Задание 4

1. Выполните оставшиеся способы зеркального отражения.
"""
import zipfile
from typing import Optional

import cv2
import numpy as np


def read_image_from_zip(zip_file_path: str, image_name: str) -> Optional[np.ndarray]:
    """Читает изображение из ZIP-файла.

    Args:
        zip_file_path (str): Путь к ZIP-файлу.
        image_name (str): Имя изображения внутри ZIP-файла.

    Returns:
        Optional[np.ndarray]: Декодированное изображение или None, если не удалось загрузить.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        with zip_ref.open(image_name) as file:
            image_data = file.read()
            image_array = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


def process_image(image: np.ndarray, flip_codes: tuple[int, int, int]) -> None:
    images = []

    for flip_code in flip_codes:
        flipped_image = cv2.flip(image, flip_code)
        images.append(flipped_image)

    for idx, flipped_image in enumerate(images):
        cv2.imshow(f"Flipped image {idx}", flipped_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    zip_file_path = '../images_to_notebook.zip'
    image_name = 'testfile.jpeg'

    image = read_image_from_zip(zip_file_path, image_name)
    process_image(image, (1, 0, -1))


if __name__ == '__main__':
    main()

