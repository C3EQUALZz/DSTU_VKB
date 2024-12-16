"""
Задание 3

1. Поверните исходное изображение на 45°, 90°, 120°.
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


def process_image(image: np.ndarray, angles: list[int]) -> None:
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)

    rotated_images = []

    for angle in angles:
        # Подготовим объект для поворота изображения
        prepared_obj = cv2.getRotationMatrix2D(center, angle, 1.0)
        # Повернем изображение
        rotated = cv2.warpAffine(image, prepared_obj, (w, h))
        rotated_images.append(rotated)

    cv2.imshow("Original Image", image)

    for idx, rotated in enumerate(rotated_images):
        cv2.imshow(f"Rotated Image {angles[idx]} degrees", rotated)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    zip_file_path = '../images_to_notebook.zip'
    image_name = 'testfile.jpeg'

    image = read_image_from_zip(zip_file_path, image_name)

    process_image(image, [45, 90, 120])


if __name__ == '__main__':
    main()
