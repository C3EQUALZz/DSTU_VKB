#!/usr/bin/env python
"""
Вариант 1 Ковалев Данил ВКБ22
"""
import npyscreen


class TerminalForm(npyscreen.ActionFormV2):
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
        # 1 запись, где 1 аргумент - вид виджета (текст), имя, параметры.
        self.add(npyscreen.TitleText, name="Выполнил Ковалев Данил ВКБ22 Вариант 1", editable=False)
        self.select_lab = self.add(npyscreen.TitleText, name="Выберите лабораторную работу: ",
                                   begin_entry_at=30, use_two_lines=False)

        # Рисуем линию, узнавая возможное пространство. Первым аргументом идет Oy, а вторым - Ox.
        # self.draw_line_at = self.useable_space()[0] - 1

    def on_ok(self):
        ...

    def on_cancel(self):
        """
        Позволяет, чтобы выходили с помощью команды Enter, а не уничтожения приложения, используя Ctrl+C
        """
        exiting = npyscreen.notify_yes_no("Вы хотите завершить работу программы? ")
        if exiting:
            self.parentApp.setNextForm(None)
        else:
            self.parentApp.setNextForm("MAIN")


class Terminal(npyscreen.NPSAppManaged):
    def onStart(self):
        """
        Создает сущность нашего приложения. Первый аргумент - главный экран, второй - наполнение, третий - название.
        """
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm('MAIN', TerminalForm)


if __name__ == '__main__':
    TestApp = Terminal().run()
