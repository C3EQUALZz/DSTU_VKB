#!/usr/bin/env python
"""
Вариант 1 Ковалев Данил ВКБ22
TODO:
Сделать реализацию выборов лабораторных в backend
Заблокировать изменять доступ, когда выбрали задание.

"""
import npyscreen
import os


class TerminalForm(npyscreen.ActionPopupWide):
    """
    Наследуемся от класса форм, чтобы наполнить наше приложение объектами
    """

    def __init__(self, *args, **keywords):
        super().__init__(args, keywords)
        self.select_lab = None

    def create(self):
        """
        Переопределенный метод, который позволяет
        """

        # Устанавливаем расположение терминала по центру
        self.show_atx, self.show_aty = map(lambda x: (x[0] - x[1]) // 2,
                                           zip(os.get_terminal_size(), self.useable_space()[::-1]))
        # Добавили текст того, кто выполнил
        self.add(npyscreen.TitleText, name="Выполнил Ковалев Данил ВКБ22 Вариант 1", editable=False)
        self.add(npyscreen.TitleText, name="Выберите лабораторную работу: ", editable=False)

        # Создаем дерево для удобного выбора лабораторной работы
        lab_tree_data = npyscreen.TreeData(content="Лабораторные работы")
        # Создаем узлы, где содержатся лабораторные работы
        for i in range(1, 6):
            parent_node = lab_tree_data.new_child(content=f"Лабораторная работа {i}")
            for j in range(1, 5):
                parent_node.new_child(content=f"Подзадача {j}")

        self.lab_tree = self.add(npyscreen.MLTree, max_height=6, name="Выберите лабораторную работу(и):",
                                 values=lab_tree_data, scroll_exit=True)
        # self.lab_tree.get_selected_objects()

    def on_ok(self):
        ...

    def on_cancel(self):
        """
        Позволяет, чтобы выходили с помощью команды Enter, а не уничтожения приложения, используя Ctrl+C
        """
        if npyscreen.notify_yes_no("Вы хотите завершить работу программы? "):
            self.parentApp.setNextForm(None)
        else:
            self.parentApp.setNextForm("MAIN")


class Terminal(npyscreen.NPSAppManaged):
    def onStart(self):
        """
        Создает сущность нашего приложения. Первый аргумент - главный экран, второй - наполнение, третий - название.
        """
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm('MAIN', TerminalForm, name="Выполнил Ковалев Данил ВКБ22 Вариант 1")


if __name__ == '__main__':
    TestApp = Terminal().run()
