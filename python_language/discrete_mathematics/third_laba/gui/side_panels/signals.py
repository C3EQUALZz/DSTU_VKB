import os
from PyQt6 import QtWidgets, QtGui, QtCore
from .rigth_side_panel import RightSidePanel
from .threads_signals import CipherThread

class Signals(QtCore.QObject):
    encryption_finished = QtCore.pyqtSignal(str)  # Сигнал для завершения операции шифрования
    decryption_finished = QtCore.pyqtSignal(str)  # Сигнал для завершения операции дешифрования

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.file_name = None
        self.right_panel = RightSidePanel()
        self.cipher_thread = None

    def show_file_dialog(self, photo_label: QtWidgets.QLabel):
        dialog = QtWidgets.QFileDialog(parent=self.parent)
        options = dialog.options()
        options |= QtWidgets.QFileDialog.Option.ReadOnly
        self.file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self.parent, "Выберите фото", "",
                                                                  "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)",
                                                                  options=options)

        if self.file_name:
            pixmap = QtGui.QPixmap(self.file_name)
            scaled_pixmap = pixmap.scaled(photo_label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            photo_label.setPixmap(scaled_pixmap)
            photo_label.show()

    def crypt_photo(self):
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
        if self.file_name is None:
            return

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
    def handle_finished(self, is_encryption):
        image_path = self.save_path(self.file_name, self.__get_path(), encrypted=is_encryption)
        self.right_panel.set_image(image_path)
        if is_encryption:
            self.encryption_finished.emit(image_path)
        else:
            self.decryption_finished.emit(image_path)

    @staticmethod
    def __get_path():
        current_path = os.path.dirname(__file__)
        relative_path = "../../"
        return os.path.abspath(os.path.join(current_path, relative_path))

    @staticmethod
    def save_path(file_name, target_directory, encrypted=True):
        word = "encrypted" if encrypted else "decrypted"
        base_name = os.path.basename(file_name)
        return f"{target_directory}/trash_for_data/{os.path.splitext(base_name)[0]}_{word}.png"
