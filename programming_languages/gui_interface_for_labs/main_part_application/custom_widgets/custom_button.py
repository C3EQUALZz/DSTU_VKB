"""
Для реали
"""

from PyQt6 import QtWidgets, QtCore, QtGui
from colour import Color


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QPushButton{height: 30px;width: 200px;}")

        layout = QtWidgets.QHBoxLayout()
        btn = Button("2020 is an interesting year.")
        layout.addStretch()
        layout.addWidget(btn)
        layout.addStretch()
        self.setLayout(layout)


class Button(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect()

        self.tm = QtCore.QBasicTimer()

        self.mouse = ''

        self.change_color(color="black")

        self.expand = 0
        self.maxExpand = 4
        self.init_s_color = self.end_s_color = "black"
        self.garding_s_seq = self.grade_color(c1=self.init_s_color,
                                              c2=self.end_s_color,
                                              steps=self.maxExpand)

        self.grade = 0
        self.maxGrade = 15
        self.init_bg_color = self.end_bg_color = self.init_s_color
        self.gradding_bg_seq = self.grade_color(c1=self.init_bg_color,
                                                c2=self.end_bg_color,
                                                steps=self.maxGrade)

        self.shadow_settings()

    def shadow_settings(self):
        self.setGraphicsEffect(self.shadow)
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QtGui.QColor("#3F3F3F"))

    def change_color(self, color: str) -> None:
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(color))
        self.setPalette(palette)

    def enterEvent(self, e) -> None:
        self.mouse = 'on'
        self.setGraphicsEffect(self.shadow)
        self.tm.start(15, self)

    def leaveEvent(self, e) -> None:
        self.mouse = 'off'

    def timerEvent(self, e) -> None:

        if self.mouse == 'on' and self.grade < self.maxGrade:
            self.grade += 1
            self.change_color(color=self.gradding_bg_seq[self.grade - 1])

        elif self.mouse == 'off' and self.grade > 0:
            self.change_color(color=self.gradding_bg_seq[self.grade - 1])
            self.grade -= 1

        if self.mouse == 'on' and self.expand < self.maxExpand:
            self.expand += 1
            self.shadow.setColor(QtGui.QColor(self.garding_s_seq[self.expand - 1]))
            self.setGeometry(self.x() - 1, int(self.y() - 1), self.width() + 2, self.height() + 2)

        elif self.mouse == 'off' and self.expand > 0:
            self.expand -= 1
            self.setGeometry(self.x() + 1, int(self.y() + 1), self.width() - 2, self.height() - 2)

        elif self.mouse == 'off' and self.expand in [0, self.maxExpand] and self.grade in [0, self.maxGrade]:
            self.shadow.setColor(QtGui.QColor(self.init_s_color))
            self.tm.stop()

    @staticmethod
    def grade_color(c1, c2, steps) -> list:
        return [str(i) for i in Color(c1).range_to(Color(c2), steps)]


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    main = Main()
    main.show()
    app.exec()
