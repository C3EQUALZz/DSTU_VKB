"""
Задание 6

1. Загрузите произвольное изображение с дорожными знаками и подберите параметры low_color, high_color для выделения
 одного из знаков или каких-либо ярких объектов. Возьмите файл с названием dorZnak1.jpg
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


def process_image(image: np.ndarray) -> None:
    # задаем границы диапазона:
    # нижнюю
    low_color = (200, 30, 0)
    # и верхнюю
    high_color = (255, 70, 15)
    # наложение цветовой маски на исходное изображение,
    # результат присваиваем переменной only_object
    only_object = cv2.inRange(image, low_color, high_color)

    cv2.imshow("Original", image)
    cv2.imshow("Result Image", only_object)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    zip_file_path = '../images_to_notebook.zip'
    image_name = 'DorZnak1.jpg'
    image = read_image_from_zip(zip_file_path, image_name)
    process_image(image)


if __name__ == '__main__':
    main()
