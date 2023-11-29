import os

from PIL import Image
from PyQt6.QtCore import QThread, pyqtSignal

from python_language.discrete_mathematics.third_laba.backend_сipher import Cypher


class CipherThread(QThread):
    encryption_finished = pyqtSignal(str)  # Сигнал для завершения операции шифрования
    decryption_finished = pyqtSignal(str)  # Сигнал для завершения операции дешифрования

    def __init__(self, file_name, target_directory, encrypt=True):
        super().__init__()
        self.file_name = file_name
        self.target_directory = target_directory
        self.encrypt = encrypt

    def run(self):
        image = Image.open(self.file_name)
        cypher = Cypher(image)

        if self.encrypt:
            encrypted_image = cypher.encrypt(key_filename=f"{self.target_directory}/trash_for_data/key_test.txt")
            encrypted_image_path = self.__save_path(self.file_name, self.target_directory, encrypted=True)
            encrypted_image.save(encrypted_image_path)
            self.encryption_finished.emit(encrypted_image_path)
        else:
            decrypted_image = cypher.decrypt(key_filename=f"{self.target_directory}/trash_for_data/key_test.txt")
            decrypted_image_path = self.__save_path(self.file_name, self.target_directory, encrypted=False)
            decrypted_image.save(decrypted_image_path)
            self.decryption_finished.emit(decrypted_image_path)

    def __save_path(self, file_name, target_directory, encrypted=True):
        word = "encrypted" if encrypted else "decrypted"
        base_name = os.path.basename(file_name)
        return f"{target_directory}/trash_for_data/{os.path.splitext(base_name)[0]}_{word}.png"
