#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ковалев Данил ВКБ22 Вариант 1
"""
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import qdarktheme
from tabdemo import MenuBarLabs


class DlgMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._create_tabs()

    def _create_tabs(self):
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QtWidgets.QVBoxLayout(self.central_widget)

        menu_bar = MenuBarLabs(self)
        layout.addWidget(menu_bar)

    def _init_ui(self):
        """
        Определение визуальной части интерфейса.
        Здесь добавляются виджеты и свойства приложения.
        """
        self.setWindowTitle("Ковалев Данил ВКБ22")
        self.resize(500, 300)
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
