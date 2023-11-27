"""
Здесь описывается стартовое меню, которое появляется при запуске программы
"""

from PyQt6 import QtWidgets, QtCore, QtGui
from python_language.programming_languages_python.gui_interface_for_labs.main_part_application.custom_widgets.custom_button import Button


class StartScreen(QtWidgets.QWidget):
    """
    Стартовое меню с выбором: настройки, старт, выход
    """

    def __init__(self, parent):
        super().__init__()
        # создание основного layout, где мы будем помещать остальные виджеты
        self.layout = QtWidgets.QVBoxLayout(self)
        # добавили выравнивание для каждого элемента
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        # родительский класс
        self.parent = parent

        self._add_gif()
        self._create_button()

    def _create_button(self):
        """
        Метод для создания кнопок в меню
        """
        # Создание кнопки, которая перемещает в основной интерфейс программы
        start_button = Button("Начало")
        start_button.clicked.connect(self.parent.switch_to_main_window)

        exit_button = Button("Выход из программы")
        exit_button.clicked.connect(self.parent.closeEvent)

        for button in (start_button, exit_button):
            button.setMinimumSize(200, 50)
            self.layout.addWidget(button)

    def _add_gif(self):
        """
        Метод, который добавляет гиф анимацию в виде кота на главном меню
        """
        label = QtWidgets.QLabel()
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        label.setMinimumSize(QtCore.QSize(200, 200))

        movie = QtGui.QMovie("icons/feature-open-source@2x.gif")
        label.setMovie(movie)
        movie.start()

        self.layout.addWidget(label)
