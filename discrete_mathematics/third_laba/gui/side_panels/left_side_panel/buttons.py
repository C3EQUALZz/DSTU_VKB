"""
Здесь расположены кнопки, которые находятся снизу
Здесь только описание модели, сигналы находятся в другом файле
"""
from functools import partial

from PyQt6 import QtWidgets
from discrete_mathematics.third_laba.gui.side_panels.signals import Signals


class ButtonPanel(QtWidgets.QWidget):
    """
    Реализация панели с кнопками, которые используются для выбора фото, шифрования, дешифрования
    """

    def __init__(self, parent=None):
        """
        :param parent: Родительский класс, к которому мы привязываем кнопки
        """
        super().__init__(parent)
        self.signal = Signals(parent, right_panel=parent.parent().children()[1])
        self.init_ui()

    def init_ui(self):
        """
        Здесь мы создаем layout кнопок, они будут располагаться по горизонтали в таком случае
        """
        layout = QtWidgets.QHBoxLayout(self)
        for button in (self._create_choose_button(), self._create_crypt_button(), self._create_decrypt_button()):
            layout.addWidget(button)

    def _create_choose_button(self) -> QtWidgets.QPushButton:
        """
        Метод, который добавляет кнопку для выбора фото
        """
        # Создание кнопки
        choose_button: QtWidgets.QPushButton = QtWidgets.QPushButton('Выбрать фото', self)
        # Подключение кнопки к диалоговому окну с выбором фото
        show_dialog = partial(self.signal.show_file_dialog, self.parent().photo_label)
        choose_button.clicked.connect(show_dialog)
        # Устанавливаем фиксированные размеры, мне не хочется считать по-умному, поэтому подобрал
        choose_button.setFixedSize(120, 30)
        return choose_button

    def _create_crypt_button(self) -> QtWidgets.QPushButton:
        """
        Метод, который создает кнопку для шифрования фото
        """
        # Создание кнопки
        crypt_button: QtWidgets.QPushButton = QtWidgets.QPushButton('Зашифровать', self)
        # Подключение кнопки к моему классу Crypt
        crypt_button.clicked.connect(self.signal.crypt_photo)
        # Устанавливаем фиксированные размеры, мне не хочется считать по-умному, поэтому подобрал
        crypt_button.setFixedSize(120, 30)
        return crypt_button

    def _create_decrypt_button(self) -> QtWidgets.QPushButton:
        """
        Метод, который создает кнопку для дешифрования фото
        """
        # Создание кнопки
        decrypt_button: QtWidgets.QPushButton = QtWidgets.QPushButton("Расшифровать", self)
        # Подключение кнопки к моему классу Crypt
        decrypt_button.clicked.connect(self.signal.decrypt_photo)
        # Устанавливаем фиксированные размеры, мне не хочется считать по-умному, поэтому подобрал
        decrypt_button.setFixedSize(120, 30)
        return decrypt_button
