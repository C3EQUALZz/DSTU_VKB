"""
Задание 6

2. Подберите и запишите параметры low_color, high_color для различных дорожных знаков, ярких объектов из различных
изображений. Выполните вывод на экран
"""

import cv2
import numpy as np


def process_image(image: np.ndarray) -> None:
    # задаем границы диапазона:
    # нижнюю
    low_color = (45, 45, 240)
    # и верхнюю
    high_color = (180, 190, 255)
    # наложение цветовой маски на исходное изображение,
    # результат присваиваем переменной only_object
    only_object = cv2.inRange(image, low_color, high_color)
    # вывод отф only_object)
    cv2.imshow("Result", only_object)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    image_name = 'depositphotos-3030544-original.jpg'
    image = cv2.imread(image_name)
    process_image(image)


if __name__ == '__main__':
    main()
