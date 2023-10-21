from PyQt6 import QtWidgets
from .left_side_menu import TabWidget
from .tasks import TaskChooser


class DlgMain(QtWidgets.QMainWindow):

    def __init__(self):
        """
        Инициализация главного окна приложения.
        """
        super().__init__()
        # создание всех страниц, которые мы инициализируем
        self.list_widget = []
        # создание количества пунктов в боковом меню
        self._create_page(11)
        # сигнал для отслеживания изменений
        self.tabs.currentChanged.connect(self.update_condition)

    def _create_page(self, n):
        """
        Создание вертикального меню, где находятся лабораторные работы
        """
        self.tabs = TabWidget(self)
        self.tabs.setStyleSheet(self.tabs.styleSheet() + "background-color:rgb(40, 40, 40); color: rgb(255, 255, 255)")
        self.tabs.create_tabs(n)
        self.setCentralWidget(self.tabs)

    def update_condition(self):
        """
        Обновление условия задачи при изменении страницы.
        """
        widget, current_laboratory, current_number_question = self.__get_info()
        condition = TaskChooser(current_laboratory, current_number_question).condition
        widget.label.setText(condition)
        widget.input_data.clear()

    def on_ok_button_clicked(self):
        """
        Обработка сигнала нажатия "Ok"
        """
        widget, current_laboratory, current_number_question = self.__get_info()
        func = TaskChooser(current_laboratory, current_number_question).function
        text = "Выполнено" if func is None else str(func(widget.input_data.text()))
        widget.output_data.setText(text)

    def on_cancel_button_clicked(self):
        """
        Обработка сигнала нажатия "Cancel"
        """
        widget = self.__get_info()[0]
        widget.input_data.clear()
        widget.output_data.clear()

    def __get_info(self):
        """
        Вспомогательная функция, которая возвращает кортеж, состоящий из текущего номера лабораторной работы,
        номера вопроса задания
        """
        widget = self.list_widget[self.tabs.currentIndex()]
        current_laboratory = self.tabs.currentIndex() + 1
        current_number_question = widget.combobox.currentIndex() + 1
        return widget, current_laboratory, current_number_question
