#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1

Данный файл является основным, отсюда происходит запуск контента.
Version: 1.0.8
TODO:
1. Попробовать скомпилировать GUI программу по гайду: https://youtu.be/c4anm9QQV80?si=6K_sDnAQMkAdC7v1
"""

import sys

from PyQt6 import QtWidgets, QtGui

from main_part_application.main_interface import DlgMain
from other_part_application.start_menu import StartScreen


class MainWindow(QtWidgets.QWidget):
    """
    Главный класс, здесь описывается основное окно, с которым взаимодействуем.
    """

    def __init__(self):
        super().__init__()
        # Добавляем наше оформление приложения на каждое окно
        self._init_ui()
        # создаем stacked_widget для добавления нескольких окон
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        # создание стартового экрана, который появляется в самом начале
        self.start_screen = StartScreen(self)
        # основное меню, где выбор лабораторных
        self.dlg_main = DlgMain(self)
        # инициализация окон, которые видит пользователь
        self._initialize_windows()

    def _initialize_windows(self) -> None:
        """
        Создание основных виджетов, на которые остальные потом помещаются
        """
        # Создание заготовленного шаблона Linear vertical layout
        layout = QtWidgets.QVBoxLayout(self)
        # Добавление стартового меню
        self.stacked_widget.addWidget(self.start_screen)
        # Добавление основного интерфейса приложения
        self.stacked_widget.addWidget(self.dlg_main)
        # В Linear Vertical Layout добавляем наши слои приложений
        layout.addWidget(self.stacked_widget)

    def _init_ui(self) -> None:
        """
        Метод для инициализации параметров приложения
        """
        # установка названия приложения
        self.setWindowTitle("Ковалев Данил ВКБ22")
        # установка окна приложения
        self.setWindowIcon(QtGui.QIcon("icons/window_icon.png"))
        # Размеры по умолчанию при запуске
        self.setFixedSize(950, 600)
        # Центрирование приложение при запуске
        self._center()

    def switch_to_main_window(self) -> None:
        # Переключите виджет на главное окно
        self.stacked_widget.setCurrentWidget(self.dlg_main)

    def _center(self) -> None:
        """
        Метод, который центрует положения появления окна при запуске.
        """
        # Здесь qr представляет собой прямоугольник, который определяет геометрию (размер и положение)
        # главного окна (вашего QMainWindow) до того, как оно отобразится на экране.
        # Этот прямоугольник инициализируется текущими размерами и позицией окна.
        qr = self.frameGeometry()
        # Здесь вы получаете геометрию текущего доступного экрана (часть экрана, доступная для приложения)
        # и затем находите центр этой геометрии. Это определяет центр экрана.
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        # Теперь мы перемещаем прямоугольник qr так, чтобы его центр совпадал с центром экрана,
        # который мы определили в шаге 2.
        qr.moveCenter(cp)
        # Затем мы перемещаем окно (self) так, чтобы его верхний левый угол находился в верхнем левом углу
        # прямоугольника qr. Таким образом, окно становится центрированным относительно экрана.
        self.move(qr.topLeft())

    def closeEvent(self, event) -> None:
        """
        Диалоговое окно, оно появляется, когда пользователь хочет закрыть приложение
        """
        res = QtWidgets.QMessageBox.question(
            self,
            "Выход",
            "Вы точно уверены, что хотите выйти?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        try:
            if res == QtWidgets.QMessageBox.StandardButton.No:
                event.ignore()  # Игнорируем событие закрытия приложения
            else:
                sys.exit(0)
        except AttributeError:
            pass


def read_styles(filename):
    with open(filename, "r") as file:
        return file.read()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(read_styles("icons/hookmark.qss"))
    start_screen = MainWindow()
    start_screen.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
