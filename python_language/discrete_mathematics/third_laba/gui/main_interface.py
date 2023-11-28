import sys

from Custom_Widgets.Widgets import QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def _init_ui(self):
        self.setWindowTitle("Ковалев Данил ВКБ22")
        # установка окна приложения
        self.setWindowIcon(QtGui.QIcon("icons/software-application.png"))
        # Размеры по умолчанию при запуске
        self.setFixedSize(850, 500)
        # Центрирование приложение при запуске
        self._center()

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


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    start_screen = MainWindow()
    start_screen.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
