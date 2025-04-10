"""
Точка входа лабораторной работы
"""

import sys

from gui import MainWindow
from PyQt6 import QtWidgets


def read_styles(filename: str) -> str:
    """
    Функция, которая считывает стили файла
    """
    with open(filename, "r") as file:
        return file.read()


def main():
    """
    Точка входа в лабораторную работу
    """
    app = QtWidgets.QApplication(sys.argv)
    styles = read_styles("gui/icons/styles.qss")
    app.setStyleSheet(styles)
    main_frame = MainWindow()
    main_frame.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
