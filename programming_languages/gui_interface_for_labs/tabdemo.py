from PyQt6.QtWidgets import QTabWidget, QWidget, QApplication
import sys


class MenuBarLabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_tabs(4)

    def _init_tabs(self, n):
        for i in range(1, n + 1):
            self.addTab(QWidget(), f"Лабораторная {i}")


def main():
    app = QApplication(sys.argv)
    ex = MenuBarLabs()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
