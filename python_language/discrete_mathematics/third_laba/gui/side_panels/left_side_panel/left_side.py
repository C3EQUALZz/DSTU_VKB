from PyQt6 import QtWidgets, QtCore
from .buttons import ButtonPanel


class LeftSidePanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.frame = QtWidgets.QFrame()

        self.init_ui()

    def init_ui(self):
        """
        Метод, который инициализирует окно, здесь добавляются все виджеты
        """
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setLineWidth(2)
        self._add_layout()

    def _add_layout(self):
        """
        Метод, который добавляет layout для нашего frame
        """
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self._create_photo_label(), stretch=1)
        layout.addWidget(ButtonPanel(self), alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

    def _create_photo_label(self):
        """
        Метод, который добавляет фото для отображения
        """
        self.photo_label = QtWidgets.QLabel(self)
        # Устанавливаем окантовку
        self.photo_label.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.photo_label.setLineWidth(2)
        self.photo_label.setMaximumSize(400, 400)
        self.photo_label.setMinimumSize(400, 400)
        return self.photo_label
