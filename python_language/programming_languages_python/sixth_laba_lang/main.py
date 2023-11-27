#!/usr/bin/env python
# export PYTHONPATH=$PYTHONPATH:$(pwd)
"""
Вариант 1 Ковалев Данил ВКБ22
"""
import npyscreen
import os

from python_language.programming_languages_python.first_laba_lang.tutor import first_question as first_laboratory_first_question
from python_language.programming_languages_python.first_laba_lang.tutor import second_question as first_laboratory_second_question
from python_language.programming_languages_python.first_laba_lang.tutor import third_question as first_laboratory_third_question
from python_language.programming_languages_python.first_laba_lang.tutor import last_question as first_laboratory_fourth_question

from python_language.programming_languages_python.second_laba_lang.main import first_question as second_laboratory_first_question
from python_language.programming_languages_python.second_laba_lang.main import second_question as second_laboratory_second_question
from python_language.programming_languages_python.second_laba_lang.main import third_question as second_laboratory_third_question
from python_language.programming_languages_python.second_laba_lang.main import fourth_question as second_laboratory_fourth_question

from python_language.programming_languages_python.third_laba_lang.main import first_question as third_laboratory_first_question
from python_language.programming_languages_python.third_laba_lang.main import second_question as third_laboratory_second_question
from python_language.programming_languages_python.third_laba_lang.main import third_question as third_laboratory_third_question
from python_language.programming_languages_python.third_laba_lang.main import fourth_question as third_laboratory_fourth_question

from python_language.programming_languages_python.fourth_laba_lang.main import first_question as fourth_laboratory_first_question
from python_language.programming_languages_python.fourth_laba_lang.main import second_question as fourth_laboratory_second_question
from python_language.programming_languages_python.fourth_laba_lang.main import third_question as fourth_laboratory_third_question
from python_language.programming_languages_python.fourth_laba_lang.main import fourth_question as fourth_laboratory_fourth_question

from python_language.programming_languages_python.fifth_laba_lang.main import first_question as fifth_laboratory_first_question
from python_language.programming_languages_python.fifth_laba_lang.main import second_question as fifth_laboratory_second_question
from python_language.programming_languages_python.fifth_laba_lang.main import third_question as fifth_laboratory_third_question
from python_language.programming_languages_python.fifth_laba_lang.main import fourth_question as fifth_laboratory_fourth_question

dictionary = {
    "Лабораторная работа 1 Подзадача 1": (
        "Напишите программу для решения примера. Есть переменные: a,b,c,k: Предусмотрите деление на 0. "
        "\nВсе необходимые переменные вводите ниже. ", first_laboratory_first_question),
    "Лабораторная работа 1 Подзадача 2": ("Дан произвольный список, содержащий и строки, и числа. \n"
                                          "Выведите все четные элементы построчно. ", first_laboratory_second_question),
    "Лабораторная работа 1 Подзадача 3": ("Дан произвольный список, содержащий только числа. \n "
                                          "Выведите результат сложения чисел больше 10. ",
                                          first_laboratory_third_question),
    "Лабораторная работа 1 Подзадача 4": ("Дан произвольный список, содержащий только числа. \n"
                                          "Выведите максимальное число", first_laboratory_fourth_question),
    "Лабораторная работа 2 Подзадача 1": ("Пусть задано некоторое число my_number. \n"
                                          "Запрашивайте у пользователя вводить число user_number до тех пор, "
                                          "пока оно не будет меньше my_number", second_laboratory_first_question),
    "Лабораторная работа 2 Подзадача 2": ("Пусть задан список, содержащий строки. \n"
                                          "Выведите построчно все строки размером от 5 до 10 символов. ",
                                          second_laboratory_second_question),
    "Лабораторная работа 2 Подзадача 3": ("Сгенерируйте и выведите случайную строку, состоящую из 5 символов, \n"
                                          "содержащую только заглавные буквы русского алфавита",
                                          second_laboratory_third_question),
    "Лабораторная работа 2 Подзадача 4": ("Пусть дана строка. На основе данной строки сформируйте новую, "
                                          "содержащую только цифры \nВыведите новую строку. ",
                                          second_laboratory_fourth_question),
    "Лабораторная работа 3 Подзадача 1": ("Пусть дана строка, состоящая из слов, пробелов и знаков препинания. "
                                          "\n"
                                          "На основании этой строки создайте новую (и выведите её на консоль) \n"
                                          "Содержащую только слова больше 5 символов.",
                                          third_laboratory_first_question),
    "Лабораторная работа 3 Подзадача 2": ("Пусть дана строковая переменная, содержащая информацию о студентах: "
                                          "\n"
                                          "my_string='Ф;И;О;Возраст;Категория;_Иванов;Иван;Иванович;23 года'",
                                          third_laboratory_second_question),
    "Лабораторная работа 3 Подзадача 3": ("Дана строка из прошлого задания. Выведите построчно информацию о "
                                          "студентах, чья фамилия 'Петров'", third_laboratory_third_question),
    "Лабораторная работа 3 Подзадача 4": ("Пусть дана строка произвольной длины. Выведите информацию о том, "
                                          "сколько в ней символов и сколько строк.", third_laboratory_fourth_question),
    "Лабораторная работа 4 Подзадача 1": ("Пусть дана матрица чисел размером NxN. Представьте данную матрицу в "
                                          "виде списка.\nВыведите результат сложения всех элементов матрицы.",
                                          fourth_laboratory_first_question),
    "Лабораторная работа 4 Подзадача 2": ("Пусть дан список из 10 элементов. Удалите первые 2 элемента и "
                                          "добавьте 2 новых.\nВыведите список на экран",
                                          fourth_laboratory_second_question),
    "Лабораторная работа 4 Подзадача 3": ("Пусть журнал по предмету 'Информационные технологии' представлен в "
                                          "Пусть дан журнал по предмету 'Информационные технологии' "
                                          "представлен в виде списка my_len."
                                          "Выведите список студентов конкретной группы построчно в "
                                          "виде:\n<Название группы>\n\t<ФИО>\n\t<ФИО>",
                                          fourth_laboratory_third_question),
    "Лабораторная работа 4 Подзадача 4": ("Пусть журнал по предмету 'Информационные технологии' представлен в "
                                          "виде списка my_len."
                                          "Выведите всех студентов (и их группы), если фамилия студента "
                                          "начинается на букву А.", fourth_laboratory_fourth_question),
    "Лабораторная работа 5 Подзадача 1": ("Пусть дана некоторая директория. Посчитайте количество файлов в "
                                          "данной директории и выведите на экран", fifth_laboratory_first_question),
    "Лабораторная работа 5 Подзадача 2": ("Пусть дан файл students.csv, в котором содержится информация о "
                                          "студентах в группе \n №;ФИО;Возраст;Группа\nВыведите информацию о "
                                          "студентах, отсортировав их по фамилии.", fifth_laboratory_second_question),
    "Лабораторная работа 5 Подзадача 3": ("Добавить к задаче 2 пользовательский интерфейс.\nПо увеличению "
                                          "возраста всех студентов на 1", fifth_laboratory_third_question),
    "Лабораторная работа 5 Подзадача 4": ("Добавьте к пользовательскому интерфейсу из задачи возможность "
                                          "сохранения новых данных обратно в файл", fifth_laboratory_fourth_question)
}


class TerminalForm(npyscreen.ActionPopupWide):

    def create(self):
        self.show_atx, self.show_aty = map(lambda x: (x[0] - x[1]) // 2,
                                           zip(os.get_terminal_size(), self.useable_space()[::-1]))
        self.add(npyscreen.TitleText, name="Выберите лабораторную работу: ", editable=False)

        lab_tree_data = npyscreen.TreeData(content="Лабораторные работы")
        for i in range(1, 6):
            parent_node = lab_tree_data.new_child(content=f"Лабораторная работа {i}")
            for j in range(1, 5):
                parent_node.new_child(content=f"Подзадача {j}")

        self.lab_tree = self.add(npyscreen.MLTreeMultiSelect, max_height=8, name="Выберите лабораторную работу:",
                                 values=lab_tree_data, scroll_exit=True)

        self.description = self.add(npyscreen.MultiLineEdit, value=" ", editable=False, rely=1, relx=-130)
        self.input_data = self.add(npyscreen.TitleText, value=" ", rely=5, relx=-130, name="Input data: ")

    def on_ok(self):
        question_value = (selected_node := list(self.lab_tree.get_selected_objects())[0]).content
        parent_value = selected_node.get_parent().content
        self.description.value = dictionary[parent_value + ' ' + question_value][0]
        if not self.input_data.value.isspace():
            self.description.value += f"Ответ: {dictionary[parent_value + ' ' + question_value][1](self.input_data.value)}"
        self.input_data.value = " "
        self.display()

    def on_cancel(self):
        if npyscreen.notify_yes_no("Вы хотите завершить работу программы? "):
            self.parentApp.setNextForm(None)
        else:
            self.parentApp.setNextForm("MAIN")


class Terminal(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm('MAIN', TerminalForm, name="Выполнил Ковалев Данил ВКБ22 Вариант 1")


if __name__ == '__main__':
    TestApp = Terminal().run()