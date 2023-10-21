__all__ = ["Button"]
"""
Для реализации кнопок с анимацией.
Оригинал: https://gist.github.com/ahmed4end/33183727317afd840f52385df66b4403
"""

from PyQt6 import QtWidgets, QtCore, QtGui
from colour import Color


class Button(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._shadow = QtWidgets.QGraphicsDropShadowEffect()
        self._tm = QtCore.QBasicTimer()

        self._mouse = ''

        self._expand = 0
        self._max_expand = 4

        self._shadow_settings()

    def _shadow_settings(self):
        """
        Метод для настройки тени кнопки. Задает параметры тени, такие как смещение, радиус размытия и цвет.
        """
        self.setGraphicsEffect(self._shadow)
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(20)

    def enterEvent(self, e: QtGui.QEnterEvent) -> None:
        """
        Метод, который вызывается, когда курсор мыши входит в область кнопки.
        Это начинает анимацию изменения цвета и тени.
        """
        self._mouse = 'on'
        self.setGraphicsEffect(self._shadow)
        self._tm.start(15, self)

    def leaveEvent(self, e: QtGui.QEnterEvent) -> None:
        """
        Метод, который вызывается, когда курсор мыши покидает область кнопки.
        Это завершает анимацию изменения цвета и тени.
        """
        self._mouse = 'off'

    def timerEvent(self, e: QtGui.QEnterEvent) -> None:
        """
        Метод, вызываемый таймером.
        В этом методе выполняется анимация изменения цвета и тени в зависимости от положения мыши.
        """

        if self._mouse == 'on' and self._expand < self._max_expand:
            self._expand += 1
            self.setGeometry(self.x() - 1, int(self.y() - 1), self.width() + 2, self.height() + 2)

        if self._mouse == 'off' and self._expand > 0:
            self._expand -= 1
            self.setGeometry(self.x() + 1, int(self.y() + 1), self.width() - 2, self.height() - 2)

    @staticmethod
    def grade_color(c1, c2, steps) -> list:
        """
        Статический метод, который возвращает список цветов между двумя заданными цветами c1 и c2 с
        заданным количеством steps. Это используется для создания списков цветов для анимации изменения цвета.
        """
        return [str(i) for i in Color(c1).range_to(Color(c2), steps)]
