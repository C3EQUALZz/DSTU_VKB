"""
Здесь описывается стартовое меню, которое появляется при запуске программы
"""

from PyQt6 import QtWidgets, QtCore, QtGui


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
        start_button = QtWidgets.QPushButton("Начало")
        start_button.clicked.connect(self.parent.switch_to_main_window)

        settings_button = QtWidgets.QPushButton("Настройки")

        exit_button = QtWidgets.QPushButton("Выход из программы")
        exit_button.clicked.connect(self.parent.closeEvent)

        for button in (start_button, settings_button, exit_button):
            button.setMinimumSize(200, 50)
            button.setStyleSheet(button.styleSheet() +
                                 """
                                 border-style: outset;
                                 border-width: 1px;
                                 border-radius: 15px;
                                 border-color: rgb(20, 20, 20);
                                 padding: 4px;
                                 """)
            self.layout.addWidget(button)

    def _add_gif(self):
        label = QtWidgets.QLabel()
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        label.setMinimumSize(QtCore.QSize(200, 200))

        movie = QtGui.QMovie("icons/feature-open-source@2x.gif")
        label.setMovie(movie)
        movie.start()

        self.layout.addWidget(label)
