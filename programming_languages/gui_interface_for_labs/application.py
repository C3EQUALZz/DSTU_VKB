#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1
"""
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from tabdemo import TabWidget


class DlgMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._create_tabs_vertical()
        self._create_combobox()
        self._create_label()

    def _init_ui(self):
        self.setWindowTitle("Ковалев Данил ВКБ22")
        self.setWindowIcon(QtGui.QIcon("icons8-окно-приложения-96.png"))
        self.resize(800, 500)
        self.setFont(QtGui.QFont('Cantrell', 11))
        self._center()

    def _center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _create_tabs_vertical(self):
        self.tabs = TabWidget()
        self.tabs.create_tabs(4)

        # Создаем левое меню с помощью QSplitter
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self.tabs)
        splitter.setSizes([200, self.width() - 200])

        self.setCentralWidget(splitter)

    def _create_combobox(self):
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(["Задание 1", "Задание 2", "Задание 3", "Задание 4"])
        self.combobox.currentIndexChanged.connect(self.update_label)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.combobox, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        # Создаем компоновщик для правой части
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(container)  # Добавляем QComboBox
        right_layout.addStretch(1)  # Добавляем пространство для выравнивания внизу

        # Создаем контейнер для правой части
        right_container = QtWidgets.QWidget()
        right_container.setLayout(right_layout)

        # Добавляем контейнер правой части в левую часть
        self.centralWidget().addWidget(right_container)

    def _create_label(self):
        self.label = QtWidgets.QLabel("Выбрано задание: Задание 1")
        self.update_label()  # Установим начальное значение

        label_layout = QtWidgets.QVBoxLayout()
        label_layout.addWidget(self.label)

        label_container = QtWidgets.QWidget()
        label_container.setLayout(label_layout)

        layout = QtWidgets.QHBoxLayout()
        layout.addStretch(1)  # Добавляем пространство для выравнивания внизу и справа
        layout.addWidget(label_container)  # Добавляем QLabel

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        self.centralWidget().addWidget(container)

    def update_label(self):
        selected_task = self.combobox.currentText()
        selected_lab = self.tabs.tabText(self.tabs.currentIndex())
        self.label.setText(f"Выбрано задание: {selected_task} в лабораторной: {selected_lab}")

    def closeEvent(self, event):
        res = QtWidgets.QMessageBox.question(self, "Выход", "Вы точно уверены, что хотите выйти? ")
        event.accept() if res == 16384 else event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)
    dlg_window = DlgMain()
    dlg_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
