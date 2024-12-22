"""
ЗАДАНИЕ 7

1. Загрузите изображения с дорожными знаками из предыдущего задания и подберите параметры color_low, color_high для
выделения одного из знаков или каких-либо ярких объектов.
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
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # нижняя граница — это темный ненасыщенный цвет
    color_low = (50, 160, 160)
    # верхняя граница — это яркий насыщенный цвет
    color_high = (245, 255, 255)
    # наложение цветовой маски на HSV-изображение,
    # результат присваиваем переменной only_object
    only_object = cv2.inRange(hsv_img, color_low, color_high)
    # вывод отфильтрованного изображения на экран
    cv2.imshow("Original", image)
    cv2.imshow("Result", only_object)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    zip_file_path = '../images_to_notebook.zip'
    image_name = 'DorZnak1.jpg'
    image = read_image_from_zip(zip_file_path, image_name)
    process_image(image)


if __name__ == '__main__':
    main()
