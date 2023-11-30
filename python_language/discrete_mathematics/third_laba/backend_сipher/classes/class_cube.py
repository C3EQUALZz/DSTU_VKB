"""
Здесь описывается логика самого кубика, операции с ним.
Считайте, что матрица из нашего изображения - это и есть кубик
При считывании изображения у нас получается матрица, которое ещё содержит 3 матрицы
"""
from functools import cache
# Внешние библиотеки
import numpy as np
# Мои заготовки
from .class_keys_creation import KeyManager


class Cube:
    """
    Данный класс будет обрабатывать входные изображения.
    Требуется заранее открыть фото, чтобы можно было взаимодействовать.
    """

    def __init__(self, array: np.array, key_manager: KeyManager) -> None:
        # работать с изображением только можно, если это матрица
        self.rgb_array: np.array = array
        # наш другой класс, где мы будем получать наши ключи
        self.key_manager: KeyManager = key_manager

    @cache
    def roll_row(self, encryption: bool = True) -> None:
        """
        Реализует повороты по строкам кубика Рубика для шифрования, расшифрования.
        Если encryption == True, то будет проводиться шифровка, в ином случае расшифровка.
        :encryption: параметр, который определяет поведение метода.
        """
        # Если 1, то повороты идут в правую сторону, в ином случае налево
        direction: int = 1 if encryption else -1
        # Здесь уже идут повороты кубика,
        for i in np.arange(self.rgb_array.shape[0]):
            # В алгоритме описана идея, что надо смотреть на сумму четности строки
            # Если четная -1, в ином случае 1
            sign = np.where(np.sum(self.rgb_array[i, :, :], axis=1) % 2 == 0, -1, 1)
            # Вычисление количества позиций, на которое нужно сдвинуть элементы в строке
            # sign как раз задает направление сдвига
            roll_amount = direction * sign * self.key_manager.key_rows[i]
            self.rgb_array[i, :, :] = np.roll(self.rgb_array[i, :, :], roll_amount, axis=0)

    @cache
    def roll_column(self, encryption: bool = True) -> None:
        """
        Выполняем этап шифрования со сдвигом столбцов.
        :param encryption: Отвечает за то, происходит ли шифрование или нет.
        :return: Ничего не возвращает, изменяет только нашу матрицу с цветами
        """
        # Если 1, то повороты идут в правую сторону, в ином случае налево.
        # Так задумано при шифровании с использованием данного метода. 
        direction: int = 1 if encryption else -1
        # Здесь уже идут повороты кубика
        for i in np.arange(self.rgb_array.shape[1]):
            # Здесь появляется массив numpy, в котором содержится 3 числа со знаками для значения key_columns.
            # Знаки key_columns определяются вообще для этого, опять-таки так шифровал dannyi96 (GitHub).
            # key_columns у автора - KC.
            sign: np.ndarray[int] = np.where(np.sum(self.rgb_array[:, i, :], axis=1) % 2 == 0, -1, 1)
            # Здесь такая логика: направление вращения кубика (-1 или 1) * массив sign (содержит значения для
            # key_column). Массивы numpy поддерживают умножения на список (поэлементно умножаются значения),
            # не как в математике
            roll_amount: np.ndarray[int] = direction * self.key_manager.key_columns[i] * sign
            # происходит поворот
            self.rgb_array[:, i, :] = np.roll(self.rgb_array[:, i, :], roll_amount, axis=0)

    @cache
    def xor_pixels(self) -> None:
        """
        Производится шифрование каждого пикселя по 3 цветовым каналам
        Связан с классом кубика, потому что здесь есть логика поворотов граней.
        Выполняет шифрование ячеек с использованием xor.
        """
        for i in np.arange(self.rgb_array.shape[0]):
            for j in np.arange(self.rgb_array.shape[1]):
                # если строка четная, то будет разворот на 180 градусов
                xor_1 = self.key_manager.key_columns[j] if i % 2 == 1 else np.flip(self.key_manager.key_columns[j])
                xor_2 = self.key_manager.key_rows[i] if j % 2 == 0 else np.flip(self.key_manager.key_rows[i])
                self.rgb_array[i, j, :] = self.rgb_array[i, j, :] ^ xor_1 ^ xor_2
