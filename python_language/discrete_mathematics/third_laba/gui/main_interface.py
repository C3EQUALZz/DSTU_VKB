#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1

Данный файл является основным, отсюда происходит запуск контента.
Version: 1.0.0
"""

import sys

from PyQt6 import QtWidgets, QtGui, QtCore

from .side_panels import LeftSidePanel, RightSidePanel


class MainWindow(QtWidgets.QMainWindow):
    """
    Главный класс, здесь описывается основное окно, с которым взаимодействуем.
    """

    def __init__(self):
        super().__init__()
        # Добавляем наше оформление приложения на каждое окно
        self._init_ui()

    def _create_splitter(self) -> None:
        """
        Создание основных виджетов, на которые остальные потом помещаются
        """
        # Создаем QSplitter
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)

        # Создаем виджет для левой части
        left_panel = LeftSidePanel(self)

        # Создаем виджет для правой части
        right_panel = RightSidePanel(self)

        # Добавляем виджеты в Splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        splitter.setSizes([self.width() // 2, self.width() // 2])
        splitter.setHandleWidth(0)
        splitter.setCollapsible(0, False)

        # Устанавливаем Splitter в качестве центрального виджета
        self.setCentralWidget(splitter)

    def _init_ui(self) -> None:
        """
        Метод для инициализации параметров приложения
        """
        # установка названия приложения
        self.setWindowTitle("Ковалев Данил ВКБ22")
        # установка окна приложения
        self.setWindowIcon(QtGui.QIcon("icons/window_icon.png"))
        # Размеры по умолчанию при запуске
        self.setFixedSize(850, 500)
        # Центрирование приложение при запуске
        self._center()

        self._create_splitter()

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
