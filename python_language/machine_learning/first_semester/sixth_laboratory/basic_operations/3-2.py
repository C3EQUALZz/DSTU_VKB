"""
Задание 3

2. Выведите на экран уменьшенное перевернутое изображение.
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


def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """Поворачивает изображение на заданный угол.

    Args:
        image (np.ndarray): Исходное изображение.
        angle (float): Угол поворота в градусах.

    Returns:
        np.ndarray: Повернутое изображение.
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
    return rotated_image


def resize_image(image: np.ndarray, scale: float) -> np.ndarray:
    """Изменяет размер изображения.

    Args:
        image (np.ndarray): Исходное изображение.
        scale (float): Коэффициент изменения размера.

    Returns:
        np.ndarray: Измененное по размеру изображение.
    """
    new_width = int(image.shape[1] * scale)
    new_height = int(image.shape[0] * scale)
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized_image


def process_image(image: np.ndarray) -> None:
    rotated_image = rotate_image(image, 180)
    resized_image = resize_image(rotated_image, 0.5)

    cv2.imshow("Original Image", image)
    cv2.imshow("Inverted and reduces image", resized_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    zip_file_path = '../images_to_notebook.zip'
    image_name = 'testfile.jpeg'

    image = read_image_from_zip(zip_file_path, image_name)

    process_image(image)


if __name__ == '__main__':
    main()
