from PyQt6 import QtWidgets, QtCore, QtGui


class RightSidePanel(QtWidgets.QWidget):
    """
    Можно было унаследоваться от LeftSide, но у меня происходят циклы импорта
    """
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
        Здесь я его переопределяю при наследовании
        Метод, который добавляет layout для нашего frame
        """
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self._create_photo_label(), stretch=1, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

    def _create_photo_label(self):
        """
        Метод, который добавляет фото для отображения
        """
        self.photo_label = QtWidgets.QLabel(self)
        # Устанавливаем окантовку
        self.photo_label.setFrameShape(QtWidgets.QFrame.Shape.Box)
        # Толщина линии
        self.photo_label.setLineWidth(2)
        # Сделал фиксированные размеры, так как костыль
        self.photo_label.setFixedSize(400, 400)
        self.photo_label.isVisible()
        return self.photo_label

    def set_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(self.photo_label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.photo_label.setPixmap(scaled_pixmap)
        self.photo_label.show()

