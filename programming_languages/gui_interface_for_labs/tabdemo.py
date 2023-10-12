"""
Здесь описана логика создания бокового меню
Ответ, с которого получилась реализация: https://inlnk.ru/QwLLpD
"""
__all__ = ["TabWidget"]

from PyQt6 import QtGui, QtWidgets, QtCore


class TabBar(QtWidgets.QTabBar):

    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabLabel, opt)
            painter.restore()


class Widget(QtWidgets.QWidget):
    def __init__(self, num_lab):
        super().__init__()

        self.label = QtWidgets.QLabel(f"Лабораторная работа {num_lab}")
        self.label.setStyleSheet("""
            font-size: 24px;
        """)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label,
                              alignment=QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabBar(TabBar(self))

        self.setTabPosition(QtWidgets.QTabWidget.TabPosition.West)
        self.setFont(QtGui.QFont('Cantrell', 11))
        self.layout = QtWidgets.QVBoxLayout(self)

    def create_tabs(self, count):
        for i in range(1, count + 1):
            self.addTab(Widget(i), QtGui.QIcon("chemistry.png"), f"Лабораторная работа {i}")