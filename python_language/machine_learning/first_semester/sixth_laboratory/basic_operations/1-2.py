"""
Задание 1.

2. Измените программу для уменьшения / увеличения изображения в 2 раза.
"""
import cv2
import zipfile
import numpy as np
from typing import Optional


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
    wide = int(image.shape[1] / 2)
    height = int(image.shape[0] / 2)

    resized_image = cv2.resize(image, (wide, height), interpolation=cv2.INTER_AREA)

    cv2.imshow("Original Image", image)
    cv2.imshow("Resized Image", resized_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    zip_file_path = '../images_to_notebook.zip'
    image_name = 'testfile.jpeg'

    image = read_image_from_zip(zip_file_path, image_name)

    process_image(image)


if __name__ == '__main__':
    main()
