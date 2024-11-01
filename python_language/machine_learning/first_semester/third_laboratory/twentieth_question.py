"""
Дан трёхмерный массив "Цветное изображение", содержащий изображение, размера (height, width, numChannels),
а также вектор коэффициентов длины numChannels.
Сложить каналы изображения с указанными весами, и вернуть результат в виде матрицы размера (height, width).
Реальное изображение не считываем, заполняем трехмерный массив случайными значениями.
Преобразуйте цветное изображение в оттенки серого, использовав коэффициенты np.array([0.299, 0.587, 0.114]).
"""
import numpy as np
from typing import Final

HEIGHT: Final[int] = 100
WIDTH: Final[int] = 100
NUMBER_OF_CHANNELS: Final[int] = 3
ARRAY_WITH_COEFFICIENTS: Final[np.ndarray] = np.array([0.299, 0.587, 0.114], dtype=np.float64)


def main() -> None:
    color_image = np.random.randint(0, 256, size=(HEIGHT, WIDTH, NUMBER_OF_CHANNELS))
    grayscale_image = np.dot(color_image, ARRAY_WITH_COEFFICIENTS)

    print(grayscale_image.shape)


if __name__ == '__main__':
    main()
