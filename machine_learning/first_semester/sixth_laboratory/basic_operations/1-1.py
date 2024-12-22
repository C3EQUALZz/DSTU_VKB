"""
Задание 1.

1. Измените программу, задав фиксированную высоту изображения.
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
            # Читаем содержимое файла
            image_data = file.read()

            # Преобразуем байты в массив NumPy
            image_array = np.frombuffer(image_data, np.uint8)

            # Декодируем изображение
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return image


def process_image(image: np.ndarray, height: int) -> None:

    # Вычисляем коэффициент, чтобы сохранить соотношение сторон
    f = float(height) / image.shape[0]
    # Формируем кортеж (x,y) с размерами изображения
    new_size = (int(image.shape[1] * f), height)

    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

    cv2.imshow("Original Image", image)
    cv2.imshow("Resized Image", resized_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    zip_file_path = '../images_to_notebook.zip'
    image_name = 'testfile.jpeg'
    fixed_height = 250

    image = read_image_from_zip(zip_file_path, image_name)

    process_image(image, fixed_height)


if __name__ == "__main__":
    main()
