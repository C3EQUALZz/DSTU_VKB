#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1

Данный файл является основным, отсюда происходит запуск контента.
Version: 1.0.0
"""

from PyQt6 import QtWidgets, QtGui, QtCore
from application import DlgMain
import sys


class MainWindow(QtWidgets.QWidget):
    """
    Главный класс, здесь описывается основное окно, с которым взаимодействуем.
    """

    def __init__(self):
        super().__init__()
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.start_screen = StartScreen(self)
        self.dlg_main = DlgMain()

        self._create_stacked_widget()

    def _create_stacked_widget(self):
        """
        Создание основных виджетов, на которые остальные потом помещаются
        """
        layout = QtWidgets.QVBoxLayout(self)

        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.dlg_main)

        layout.addWidget(self.stacked_widget)
        self.init_ui()
        self.show()

    def init_ui(self):
        """
        Метод для инициализации параметров приложения
        """
        self.setStyleSheet(self.styleSheet() + "background-color:rgb(40, 40, 40); color: rgb(255, 255, 255)")
        # установка названия приложения
        self.setWindowTitle("Ковалев Данил ВКБ22")
        # установка окна приложения
        self.setWindowIcon(QtGui.QIcon("icons8-окно-приложения-96.png"))
        # Размеры по умолчанию при запуске
        self.resize(850, 500)
        # Установка шрифта и размеров
        self.setFont(QtGui.QFont('Cantrell', 11))
        # Центрирование приложение при запуске
        self._center()

    def switch_to_main_window(self):
        # Переключите виджет на главное окно
        self.stacked_widget.setCurrentWidget(self.dlg_main)

    def _center(self):
        """
        Метод, который центрует положения появления окна при запуске.
        """
        qr = self.frameGeometry()  # размеры нашего окна
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()  # определяем размеры окна приложения
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        """
        Диалоговое окно, оно появляется, когда пользователь хочет закрыть приложение
        """
        res = QtWidgets.QMessageBox.question(self, "Выход", "Вы точно уверены, что хотите выйти? ")
        event.accept() if res == 16384 else event.ignore()


class StartScreen(QtWidgets.QWidget):
    """

    """
    def __init__(self, parent):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.parent = parent

        self._add_gif()
        self._create_button()

    def _create_button(self):
        start_button = QtWidgets.QPushButton("Начало")
        start_button.setMinimumSize(200, 50)
        start_button.clicked.connect(self.parent.switch_to_main_window)

        settings_button = QtWidgets.QPushButton("Настройки")
        settings_button.setMinimumSize(200, 50)

        exit_button = QtWidgets.QPushButton("Выход из программы")
        exit_button.setMinimumSize(200, 50)

        for widget in (start_button, settings_button, exit_button):
            self.layout.addWidget(widget)

    def _add_gif(self):
        label = QtWidgets.QLabel()
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        label.setMinimumSize(QtCore.QSize(200, 200))
        label.setMaximumSize(QtCore.QSize(200, 200))

        movie = QtGui.QMovie("feature-open-source@2x.gif")
        label.setMovie(movie)
        movie.start()

        self.layout.addWidget(label)


def main():
    app = QtWidgets.QApplication(sys.argv)
    start_screen = MainWindow()
    start_screen.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
