#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1

Данный файл является основным, отсюда происходит запуск контента.
Version: 1.0.0
"""
import sys

from PyQt6 import QtGui, QtWidgets
from tabdemo import TabWidget
from tasks import TaskChooser


class DlgMain(QtWidgets.QMainWindow):
    """
    Главный класс, здесь описывается основное окно, с которым взаимодействуем.
    """

    def __init__(self):
        """
        Инициализация главного окна приложения.
        """
        super().__init__()
        # создание всех страниц, которые мы инициализируем
        self.list_widget = []
        # установка параметров для приложения
        self._init_ui()
        # создание количества пунктов в боковом меню
        self._create_page(11)
        # сигнал для отслеживания изменений
        self.tabs.currentChanged.connect(self.update_condition)

    def _init_ui(self):
        """
        Метод для инициализации параметров приложения
        """
        self.setStyleSheet(self.styleSheet() + "background-color:rgb(40, 40, 40)")
        # установка названия приложения
        self.setWindowTitle("Ковалев Данил ВКБ22")
        # установка окна приложения
        self.setWindowIcon(QtGui.QIcon("icons8-окно-приложения-96.png"))
        # Размеры по умолчанию при запуске
        self.resize(800, 500)
        # Установка шрифта и размеров
        self.setFont(QtGui.QFont('Cantrell', 11))
        # Центрирование приложение при запуске
        self._center()

    def _center(self):
        """
        Метод, который центрует положения появления окна при запуске.
        """
        qr = self.frameGeometry()  # размеры нашего окна
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()  # определяем размеры окна приложения
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _create_page(self, n):
        """
        Создание вертикального меню, где находятся лабораторные работы
        """
        self.tabs = TabWidget(self)
        self.tabs.setStyleSheet(self.tabs.styleSheet() + "background-color:rgb(40, 40, 40); color: rgb(255, 255, 255)")
        self.tabs.create_tabs(n)
        self.setCentralWidget(self.tabs)

    def update_condition(self):
        """
        Обновление условия задачи при изменении страницы.
        """
        widget, current_laboratory, current_number_question = self.__get_info()
        condition = TaskChooser(current_laboratory, current_number_question).condition
        widget.label.setText(condition)
        widget.input_data.clear()

    def on_ok_button_clicked(self):
        """
        Обработка сигнала нажатия "Ok"
        """
        widget, current_laboratory, current_number_question = self.__get_info()
        func = TaskChooser(current_laboratory, current_number_question).function
        text = "Выполнено" if func is None else str(func(widget.input_data.text()))
        widget.output_data.setText(text)

    def on_cancel_button_clicked(self):
        """
        Обработка сигнала нажатия "Cancel"
        """
        widget = self.__get_info()[0]
        widget.input_data.clear()
        widget.output_data.clear()

    def __get_info(self):
        """
        Вспомогательная функция, которая возвращает кортеж, состоящий из текущего номера лабораторной работы,
        номера вопроса задания
        """
        widget = self.list_widget[self.tabs.currentIndex()]
        current_laboratory = self.tabs.currentIndex() + 1
        current_number_question = widget.combobox.currentIndex() + 1
        return widget, current_laboratory, current_number_question

    def closeEvent(self, event):
        """
        Диалоговое окно, оно появляется, когда пользователь хочет закрыть приложение
        """
        res = QtWidgets.QMessageBox.question(self, "Выход", "Вы точно уверены, что хотите выйти? ")
        event.accept() if res == 16384 else event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)
    dlg_window = DlgMain()
    dlg_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
