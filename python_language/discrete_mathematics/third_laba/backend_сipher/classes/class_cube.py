"""
Здесь описывается логика самого кубика, операции с ним.
Считайте, что матрица из нашего изображения - это и есть кубик
При считывании изображения у нас получается матрица, которое ещё содержит 3 матрицы
"""
# Внешние библиотеки
import numpy as np
# Мои заготовки
from python_language.discrete_mathematics.third_laba.backend_сipher.help_functions import rotate180
from .class_keys_creation import KeyManager


class Cube:
    """
    Данный класс будет обрабатывать входные изображения.
    Требуется заранее открыть фото, чтобы можно было взаимодействовать.
    """

    def __init__(self, array: np.array, key_manager: KeyManager) -> None:
        # работать с изображением только можно, если это матрица
        self.rgb_array = array
        # наш другой класс, где мы будем получать наши ключи
        self.key_manager = key_manager

    def roll_row(self, encryption: bool = True) -> None:
        """
        Реализует повороты по строкам кубика Рубика для шифрования, расшифрования.
        Если encryption == True, то будет проводиться шифровка, в ином случае расшифровка.
        :encryption: параметр, который определяет поведение метода.
        """
        # Если 1, то повороты идут в правую сторону, в ином случае налево
        direction = 1 if encryption else -1
        # Здесь уже идут повороты кубика,
        for i in range(self.rgb_array.shape[0]):
            # У нас 3 цветовых канала
            for j in range(3):
                # Для каждой строки изображения
                # вычисляются остатки от деления суммы значений пикселей по каждому цветовому каналу на 2
                # Все вопросы к автору, у которого я переделываю код, сам не знаю такое
                sign = (1, -1)[np.sum(self.rgb_array[i, :, j]) % 2 == 0]
                self.rgb_array[i, :, j] = np.roll(self.rgb_array[i, :, j],
                                                  direction * sign * self.key_manager.key_columns[i])

    def roll_column(self, encryption: bool = True) -> None:
        """
        Выполняем этап шифрования со сдвигом столбцов.
        :param encryption: Отвечает за то, происходит ли шифрование или нет.
        :return: Ничего не возвращает, изменяет только нашу матрицу с цветами
        """
        # Если 1, то повороты идут в правую сторону, в ином случае налево
        direction = 1 if encryption else -1
        # Здесь уже идут повороты кубика
        for i in range(self.rgb_array.shape[1]):
            # У нас 3 цветовых канала
            for j in range(3):
                # Для каждой строки изображения
                # вычисляются остатки от деления суммы значений пикселей по каждому цветовому каналу на 2
                # Все вопросы к автору, у которого я переделываю код, сам не знаю такое
                sign = (1, -1)[np.sum(self.rgb_array[:, i, j]) % 2 == 0]
                self.rgb_array[:, i, j] = np.roll(self.rgb_array[:, i, j],
                                                  direction * sign * self.key_manager.key_columns[i])

    def xor_pixels(self) -> None:
        """
        Производится шифрование каждого пикселя по 3 цветовым каналам
        Связан с классом кубика, потому что здесь есть логика поворотов граней.
        Выполняет шифрование ячеек с использованием xor.
        """
        for i in range(self.rgb_array.shape[0]):
            for j in range(self.rgb_array.shape[1]):
                # если строка четная, то будет разворот на 180 градусов
                xor_1 = self.key_manager.key_columns[j] if i % 2 == 1 else rotate180(self.key_manager.key_columns[j])
                xor_2 = self.key_manager.key_rows[i] if j % 2 == 0 else rotate180(self.key_manager.key_rows[i])
                for k in range(3):
                    self.rgb_array[i, j, k] ^= xor_1 ^ xor_2
