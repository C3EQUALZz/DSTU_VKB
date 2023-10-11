#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1
"""
import sys
import qdarktheme

from PyQt6 import QtCore, QtGui, QtWidgets
from tabdemo import TabWidget


class DlgMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._create_tabs_vertical()
        self._create_combobox()

    def _init_ui(self):
        """
        Определение визуальной части интерфейса.
        Здесь добавляются виджеты и свойства приложения.
        """
        self.setWindowTitle("Ковалев Данил ВКБ22")
        self.setWindowIcon(QtGui.QIcon("icons8-окно-приложения-96.png"))
        self.resize(800, 500)
        self.setFont(QtGui.QFont('Cantrell', 11))
        self._center()

    def _center(self):
        """
        Метод, который центрует появление приложения по центру экрана.
        """
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _create_tabs_vertical(self):
        """
        Метод, который создает боковое меню для выбора лабораторных работ
        """
        self.tabs = TabWidget()
        self.tabs.create_tabs(4)
        self.setCentralWidget(self.tabs)

    def _create_combobox(self):
        """
        Метод, который создает выпадающий список
        """
        self.combobox = QtWidgets.QComboBox()
        self.combobox.setFixedSize(180, 180)
        self.combobox.addItems(["Задание 1", "Задание 2", "Задание 3", "Задание 4"])

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.combobox, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        # Создаем контейнер для размещения элементов
        container = QtWidgets.QWidget()
        container.setLayout(layout)

        self.setMenuWidget(container)

    # def _create_label(self):
    #     self.label = QtWidgets.QLabel("Выбрано задание: Задание 1")
    #     self.update_label()  # Установим начальное значение
    #
    #     label_layout = QtWidgets.QVBoxLayout()
    #     label_layout.addWidget(self.label)
    #
    #     label_container = QtWidgets.QWidget()
    #     label_container.setLayout(label_layout)
    #
    #     layout = QtWidgets.QHBoxLayout()
    #     layout.addStretch(1)  # Добавляем пространство для выравнивания внизу и справа
    #     layout.addWidget(label_container)
    #
    #     container = QtWidgets.QWidget()
    #     container.setLayout(layout)
    #     self.setCentralWidget(container)
    #
    # def update_label(self):
    #     selected_task = self.combobox.currentText()
    #     selected_lab = self.tabs.tabText(self.tabs.currentIndex())
    #     self.label.setText(f"Выбрано задание: {selected_task} в лабораторной: {selected_lab}")

    def closeEvent(self, event):
        """
        Метод, который отвечает за диалоговое окно при закрытии приложения.
        Перегруженный метод класса.
        """
        res = QtWidgets.QMessageBox.question(self, "Выход", "Вы точно уверены, что хотите выйти? ")
        event.accept() if res == 16384 else event.ignore()


def main():
    qdarktheme.enable_hi_dpi()
    app = QtWidgets.QApplication(sys.argv)  # создаем приложение
    qdarktheme.setup_theme()
    dlg_window = DlgMain()
    dlg_window.show()
    sys.exit(app.exec())  # цикл событий, который отображает виджеты


if __name__ == "__main__":
    main()
