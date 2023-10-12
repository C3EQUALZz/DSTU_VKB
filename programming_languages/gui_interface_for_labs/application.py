#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1
TODO:
Поставить хендлер на обновление меню

"""
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from tabdemo import TabWidget


class DlgMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._create_tabs_vertical(6)
        self._create_combobox()

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

    def _create_tabs_vertical(self, n):
        self.tabs = TabWidget()
        self.tabs.create_tabs(n)

        # Создаем левое меню с помощью QSplitter
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self.tabs)
        splitter.setSizes([200, self.width() - 200])

        self.setCentralWidget(splitter)

    def _create_combobox(self):
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(["Задание 1", "Задание 2", "Задание 3", "Задание 4"])

        self.tabs.layout.addWidget(self.combobox,
                                   alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)

    def _create_question(self):
        self.label = QtWidgets.QLabel(" ")
        self.update_label()

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
