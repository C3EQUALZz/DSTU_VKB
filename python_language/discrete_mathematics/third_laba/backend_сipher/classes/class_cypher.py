"""
Файл, где описан интерфейс для взаимодействия с шифром Рубика для изображения

https://github.com/dannyi96/Image-Cryptography
https://github.com/klanec/RubiksCipher/blob/master/rubikscipher.py
https://klanec.github.io/rgbctf/2020/07/22/rgbctf-RubiksCBC.html
"""
import numpy as np
from PIL import Image

from .class_keys_creation import KeyManager
from .class_cube import Cube

__all__ = ["Cypher"]


class Cypher:
    """
    Класс, который реализует логику шифрования. Является интерфейсом к пользователю.
    """

    def __init__(self, image: Image) -> None:
        # работать с изображением только можно, если это матрица
        self._rgb_array = np.array(image.convert('RGB'))
        # наш другой класс, где мы будем получать наши ключи
        self._key_manager = KeyManager(*self._rgb_array.shape[:2])
        self._cube = Cube(self._rgb_array, self._key_manager)

    def encrypt(self, key_filename: str = 'trash_for_data/key.txt') -> Image:
        """
        Осуществляет шифрование фото.
        :param key_filename: Название или путь к файлу
        :return: возвращает объект Pillow изображения
        """
        self._key_manager.create_key_file(key_filename)
        for _ in range(10):
            self._cube.roll_row(encryption=True)
            self._cube.roll_column(encryption=True)
            self._cube.xor_pixels()

        return Image.fromarray(self._cube.rgb_array.astype(np.uint8))

    def decrypt(self, key_filename: str = 'trash_for_data/key.txt') -> Image:
        """
        Осуществляет расшифровку фото.
        :param key_filename: Название или путь к файлу
        :return: возвращает объект Pillow изображения
        """
        self._key_manager.load_key_file(key_filename)
        for _ in range(10):
            self._cube.xor_pixels()
            self._cube.roll_column(encryption=False)
            self._cube.roll_row(encryption=False)

        return Image.fromarray(self._cube.rgb_array.astype(np.uint8))
