"""
В данном модуле реализованы отдельно сигналы, которые используются для обработки нажатия кнопок.
"""

import os

from PyQt6 import QtCore, QtGui, QtWidgets

from .threads_signals import CipherThread


class Signals(QtCore.QObject):
    """
    Класс, который осуществляет за реализацию нажатия кнопок.
    """

    encryption_finished = QtCore.pyqtSignal(
        str
    )  # Сигнал для завершения операции шифрования
    decryption_finished = QtCore.pyqtSignal(
        str
    )  # Сигнал для завершения операции дешифрования

    def __init__(self, parent, right_panel):
        super().__init__(parent)
        self.parent = parent
        self.right_panel = right_panel

        self.file_name = self.cipher_thread = None

    def show_file_dialog(self, photo_label: QtWidgets.QLabel) -> None:
        """
        Данный метод отвечает за отображение окна выбора фотографий.
        Будет запущен стандартный файловый менеджер, который выбран в ОС.
        """
        # Создание диалогового окна
        dialog = QtWidgets.QFileDialog(parent=self.parent)
        # Данные параметры взял с Интернета, пояснить не могу
        options = dialog.options()
        options |= QtWidgets.QFileDialog.Option.ReadOnly
        self.file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent,
            "Выберите фото",
            "",
            "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)",
            options=options,
        )
        # Если все-таки нашел файл, то будет запущена обработка по сжатию фото
        if self.file_name:
            # Создание объекта Pixmap, который умеет сжимать фотографии (более подробно в doc PyQt6)
            pixmap = QtGui.QPixmap(self.file_name)
            scaled_pixmap = pixmap.scaled(
                photo_label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )
            photo_label.setPixmap(scaled_pixmap)
            photo_label.show()

    def crypt_photo(self) -> None:
        """
        Метод, который отвечает за шифрование фото
        Отсюда происходит запуск потока для шифрования
        """
        if self.file_name is None:
            return

        target_directory = self.__get_path()

        # Проверяем, завершен ли предыдущий поток
        if self.cipher_thread and self.cipher_thread.isRunning():
            self.cipher_thread.quit()  # Прерываем предыдущий поток

        # Создаем экземпляр CipherThread
        self.cipher_thread = CipherThread(self.file_name, target_directory, True)
        # Соединяем сигнал завершения операции шифрования с методом обработки в Signals
        self.cipher_thread.finished.connect(lambda: self.handle_finished(True))
        # Запускаем поток
        self.cipher_thread.start()

    def decrypt_photo(self):
        """
        Расшифровка фото. Здесь происходит запуск логики по дешифрованию с использованием кубика Рубика
        """
        if self.file_name is None:
            return
        # получаем путь, к которому
        target_directory = self.__get_path()

        # Проверяем, завершен ли предыдущий поток
        if self.cipher_thread and self.cipher_thread.isRunning():
            self.cipher_thread.quit()  # Прерываем предыдущий поток

        # Создаем экземпляр CipherThread
        self.cipher_thread = CipherThread(self.file_name, target_directory, False)
        # Соединяем сигнал завершения операции дешифрования с методом обработки в Signals
        self.cipher_thread.finished.connect(lambda: self.handle_finished(False))
        # Запускаем поток
        self.cipher_thread.start()

    # Добавляем метод обработки сигнала завершения операции
    def handle_finished(self, is_encryption: bool) -> None:
        image_path = self.save_path(
            self.file_name, self.__get_path(), encrypted=is_encryption
        )
        print(image_path)
        self.right_panel.set_image(image_path)

        if is_encryption:
            self.encryption_finished.emit(image_path)
        else:
            self.decryption_finished.emit(image_path)

    @staticmethod
    def __get_path() -> str:
        current_path = os.path.dirname(__file__)
        relative_path = "../../"
        return os.path.abspath(os.path.join(current_path, relative_path))

    @staticmethod
    def save_path(file_name, target_directory, encrypted=True) -> str:
        word = "encrypted" if encrypted else "decrypted"
        base_name = os.path.basename(file_name)
        return f"{target_directory}/trash_for_data/{os.path.splitext(base_name)[0]}_{word}.png"
