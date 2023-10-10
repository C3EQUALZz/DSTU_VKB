#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1
TODO:
Отцентровать экран по середине экрана
"""
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import qdarktheme
import os


class DlgMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_characteristics_window()
        self.create_menu_bar()

    def set_characteristics_window(self):
        self.setWindowTitle("Ковалев Данил ВКБ22")  # добавляем виджеты и свойства приложения
        # screen_geometry = QtWidgets.QSplashScreen.geometry()
        self.setGeometry(QtGui.QDesktopWidget().screenGeometry(), 500, 300)
        # self.resize(500, 300)
        self.setFont(QtGui.QFont('Cantrell', 11))

    def create_menu_bar(self):
        menubar = self.menuBar()  # Создаем менюбар
        lab_menu = menubar.addMenu('Лабораторные работы')  # Добавляем меню с выбором лабораторных работ

        lab_action_1 = QtGui.QAction('Лабораторная работа 1', self)  # Создаем действие для первой лабораторной работы
        lab_action_1.triggered.connect(self.on_lab_1_selected)  # Подключаем обработчик события

        lab_action_2 = QtGui.QAction('Лабораторная работа 2', self)  # Создаем действие для второй лабораторной работы
        lab_action_2.triggered.connect(self.on_lab_2_selected)  # Подключаем обработчик события

        lab_menu.addAction(lab_action_1)  # Добавляем действие в меню
        lab_menu.addAction(lab_action_2)  # Добавляем действие в меню

    def on_lab_1_selected(self):
        # Обработка выбора первой лабораторной работы
        self.statusBar().showMessage("Выбрана Лабораторная работа 1")

    def on_lab_2_selected(self):
        # Обработка выбора второй лабораторной работы
        self.statusBar().showMessage("Выбрана Лабораторная работа 2")

    def closeEvent(self, event):
        res = QtWidgets.QMessageBox.question(self, "Выход", "Вы точно уверены, что хотите выйти? ")
        event.accept() if res == 16384 else event.ignore()


if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QtWidgets.QApplication(sys.argv)  # создаем приложение
    qdarktheme.setup_theme()
    dlg_window = DlgMain()
    dlg_window.show()
    sys.exit(app.exec())  # цикл событий, который отображает виджеты