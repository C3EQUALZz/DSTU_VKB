"""
В данном модуле реализована логика левого frame приложения.
Решил описать в отдельном классе для соблюдения модульности и расширяемости
"""

from PyQt6 import QtCore, QtWidgets

from .buttons import ButtonPanel


class LeftSidePanel(QtWidgets.QWidget):
    """
    Класс, который отвечает за левое окно приложения (выбор фото, кнопки)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем frame, на который будем располагать все свои виджеты
        self.frame = QtWidgets.QFrame()
        # Добавляем всевозможные элементы на левое окно
        self.init_ui()

    def init_ui(self) -> None:
        """
        Метод, который инициализирует левый frame, здесь добавляются все виджеты
        """
        # Устанавливаем тип фрейма, тут он неподвижный, фиксированный
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        # Толщина линии frame
        self.frame.setLineWidth(2)
        self._add_layout()

    def _add_layout(self) -> None:
        """
        Метод, который добавляет layout для нашего frame
        """
        # Элементы будут укладываться вертикально в наш компоновщик (layout)
        layout = QtWidgets.QVBoxLayout(self)
        # Добавляю окно, где высвечивается наше фото, второй аргумент - толщина линии
        layout.addWidget(self._create_photo_label(), stretch=1)
        # Здесь добавляю свою группу кнопок
        layout.addWidget(
            ButtonPanel(self), alignment=QtCore.Qt.AlignmentFlag.AlignBottom
        )

    def _create_photo_label(self) -> QtWidgets.QLabel:
        """
        Метод, который добавляет фото для отображения.
        :return: Возвращает место, на которое мы можем разместить фото.
        """
        # Создаем Label, где мы будем размещать фото
        self.photo_label = QtWidgets.QLabel(self)
        # Устанавливаем окантовку, здесь будет видна толщина. Сильно с этой темой не разбирался
        self.photo_label.setFrameShape(QtWidgets.QFrame.Shape.Box)
        # Устанавливаем толщину линии
        self.photo_label.setLineWidth(2)
        # Ставим фиксированные размеры данного окошка с белой окантовкой
        self.photo_label.setFixedSize(400, 400)
        return self.photo_label
