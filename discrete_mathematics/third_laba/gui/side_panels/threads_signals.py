"""
Здесь модуль направлен для реализации потоков.
Сама обработка фото занимает достаточно много процессорного времени на один поток.
"""

import os

from PIL import Image
from PyQt6.QtCore import QThread, pyqtSignal
from python_language.discrete_mathematics.third_laba.backend_сipher import \
    Cypher


class CipherThread(QThread):
    """
    Отдельный поток, где мы взаимодействуем с шифрованием для нашего приложения
    """

    encryption_finished = pyqtSignal(str)  # Сигнал для завершения операции шифрования
    decryption_finished = pyqtSignal(str)  # Сигнал для завершения операции дешифрования

    def __init__(self, file_name: str, target_directory: str, encrypt: bool = True):
        super().__init__()
        # название нашего файла, который передал пользователь
        self.file_name = file_name
        # абсолютный путь до точки сохранения
        self.target_directory = target_directory
        # Решим шифрования, по умолчанию шифрует
        self.encrypt = encrypt

    def run(self) -> None:
        """
        Метод, который запускает наш поток на обработку изображения
        """
        # Открываем наше изображение с помощью Pillow
        image: Image = Image.open(self.file_name)
        # Создаем объект шифровальщика, который будем обрабатывать изображения
        cypher: Cypher = Cypher(image)

        if self.encrypt:
            # Шифруем изображение наше
            encrypted_image: Image = cypher.encrypt(
                key_filename=f"{self.target_directory}/trash_for_data/key_test.txt"
            )
            # Создаем путь к нашему изображению
            encrypted_image_path: str = self.__save_path(
                self.file_name, self.target_directory, encrypted=True
            )
            # Сохраняем фото после обработок
            encrypted_image.save(encrypted_image_path)
            # Передаем сигнал, что работа закончилась
            self.encryption_finished.emit(encrypted_image_path)
        else:
            # Расшифровываем наше изображение
            decrypted_image: Image = cypher.decrypt(
                key_filename=f"{self.target_directory}/trash_for_data/key_test.txt"
            )
            # Создаем путь к нашему изображению
            decrypted_image_path: str = self.__save_path(
                self.file_name, self.target_directory, encrypted=False
            )
            # Сохраняем фото после обработок
            decrypted_image.save(decrypted_image_path)
            # Передаем сигнал, что работа закончилась
            self.decryption_finished.emit(decrypted_image_path)

    @staticmethod
    def __save_path(file_name: str, target_directory: str, encrypted=True):
        """
        Метод, который создает путь для сохранения фото после всех обработок
        """
        word = "encrypted" if encrypted else "decrypted"
        # достаем имя файла, потому что в file_name лежит ещё расширение (.png, .jpg)
        base_name = os.path.basename(file_name)
        return f"{target_directory}/trash_for_data/{os.path.splitext(base_name)[0]}_{word}.png"
