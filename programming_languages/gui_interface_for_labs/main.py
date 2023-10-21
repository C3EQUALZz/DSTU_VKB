#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1

Данный файл является основным, отсюда происходит запуск контента.
Version: 1.0.1
"""

from PyQt6 import QtWidgets, QtGui
from programming_languages.gui_interface_for_labs.main_part_application.main_interface import DlgMain
from programming_languages.gui_interface_for_labs.other_part_application.start_menu import StartScreen
import sys


class MainWindow(QtWidgets.QWidget):
    """
    Главный класс, здесь описывается основное окно, с которым взаимодействуем.
    """

    def __init__(self):
        super().__init__()
        # создаем stacked_widget для добавления нескольких окон
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        # создание стартового экрана, который появляется в самом начале
        self.start_screen = StartScreen(self)
        # основное меню, где выбор лабораторных
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
        self.setWindowIcon(QtGui.QIcon("icons/window_icon.png"))
        # Размеры по умолчанию при запуске
        self.setFixedSize(850, 500)
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
        # размеры нашего окна
        qr = self.frameGeometry()
        # определяем размеры окна приложения
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        """
        Диалоговое окно, оно появляется, когда пользователь хочет закрыть приложение
        """
        res = QtWidgets.QMessageBox.question(self, "Выход", "Вы точно уверены, что хотите выйти? ")
        # при нажатии на кнопку event становится bool, поэтому сделан такой костыль
        if isinstance(event, bool):
            sys.exit(0)
        # при нажатии на крестик сверху приходится реализовать такую логику
        event.accept() if res == 16384 else event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)
    start_screen = MainWindow()
    start_screen.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()