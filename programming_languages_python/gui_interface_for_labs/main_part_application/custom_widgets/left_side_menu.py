"""
Здесь описана логика создания бокового меню
Ответ, с которого получилась реализация: https://inlnk.ru/QwLLpD
"""

__all__ = ["TabWidget"]

from PyQt6 import QtCore, QtGui, QtWidgets

from ..page_logic import Page


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        """
        Перегруженный метод, который позволяет настроить размер закладки по индексу
        """
        # Получаем стандартный размер закладки с помощью метода базового класса
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        # Переворачиваем размер, меняя ширину на высоту и наоборот, чтобы сделать вертикальные закладки.
        s.transpose()
        return s

    def paintEvent(self, event):
        """
        Этот метод определяет кастомную отрисовку виджета
        """
        # Создаем объект QStylePainter, который позволит нам рисовать элементы с учетом текущего стиля.
        painter = QtWidgets.QStylePainter(self)
        # Создаем объект QStyleOptionTab, который будет хранить настройки стиля для закладки.
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            # инициализируем объект opt настройками стиля для закладки с индексом i.
            self.initStyleOption(opt, i)
            # Рисуем форму закладки, используя текущие настройки стиля.
            painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabShape, opt)
            # Сохраняем текущее состояние рисования, чтобы его можно было восстановить позже.
            painter.save()
            # Получаем размер текущей закладки.
            s = opt.rect.size()
            # Переворачиваем размер, как и ранее, для вертикальных закладок.
            s.transpose()
            # Создаем новый прямоугольник с заданными размерами s.
            r = QtCore.QRect(QtCore.QPoint(), s)
            # Перемещаем новый прямоугольник так, чтобы его центр совпадал с центром исходного opt.rect.
            r.moveCenter(opt.rect.center())
            # Обновляем настройки стиля opt новым прямоугольником r.
            opt.rect = r
            # Находим центр текущей закладки.
            c = self.tabRect(i).center()
            # Перемещаем "перо" рисования в точку c.
            painter.translate(c)
            # Поворачиваем "перо" на 90 градусов, чтобы вертикальные закладки стали горизонтальными.
            painter.rotate(90)
            # Перемещаем "перо" обратно в исходную позицию.
            painter.translate(-c)
            # Рисуем текст метки закладки с учетом измененных настроек стиля.
            painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabLabel, opt)
            # Восстанавливаем ранее сохраненное состояние рисования.
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Сохраняем ссылку на родительский объект
        self.setTabBar(TabBar(self))  # Устанавливаем кастомный виджет для закладок

        self.setTabPosition(
            QtWidgets.QTabWidget.TabPosition.West
        )  # Устанавливаем положение закладок слева
        self.layout = QtWidgets.QVBoxLayout(
            self
        )  # Создаем вертикальный макет для данного виджета

    def create_tabs(self, count):
        # Инициализируем список list_widget в родительском объекте
        self.parent.list_widget = []
        for i in range(1, count + 1):
            # Создаем объект Page с номером лабораторной работы
            widget = Page(i)
            # Привязываем сигналы изменения индекса выпадающего списка, кнопки "Ok" и "Cancel" к методам
            # родительского объекта
            widget.combobox.currentIndexChanged.connect(self.parent.update_condition)
            widget.ok_button.clicked.connect(self.parent.on_ok_button_clicked)
            widget.cancel_button.clicked.connect(self.parent.on_cancel_button_clicked)
            # Добавляем созданный виджет с лабораторной работой как закладку в TabWidget (не отображается почему-то...)
            self.addTab(
                widget, QtGui.QIcon("icons/chemistry.png"), f"Лабораторная работа {i}"
            )
            # Добавляем объект Page в список list_widget
            self.parent.list_widget.append(widget)
