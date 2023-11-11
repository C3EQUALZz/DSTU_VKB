__all__ = ["TaskChooser"]

from programming_languages_python.first_laba_lang.tutor import first_question as first_laboratory_first_question
from programming_languages_python.first_laba_lang.tutor import second_question as first_laboratory_second_question
from programming_languages_python.first_laba_lang.tutor import third_question as first_laboratory_third_question
from programming_languages_python.first_laba_lang.tutor import last_question as first_laboratory_fourth_question

from programming_languages_python.second_laba_lang.main import first_question as second_laboratory_first_question
from programming_languages_python.second_laba_lang.main import second_question as second_laboratory_second_question
from programming_languages_python.second_laba_lang.main import third_question as second_laboratory_third_question
from programming_languages_python.second_laba_lang.main import fourth_question as second_laboratory_fourth_question

from programming_languages_python.third_laba_lang.main import first_question as third_laboratory_first_question
from programming_languages_python.third_laba_lang.main import second_question as third_laboratory_second_question
from programming_languages_python.third_laba_lang.main import third_question as third_laboratory_third_question
from programming_languages_python.third_laba_lang.main import fourth_question as third_laboratory_fourth_question

from programming_languages_python.fourth_laba_lang.main import first_question as fourth_laboratory_first_question
from programming_languages_python.fourth_laba_lang.main import second_question as fourth_laboratory_second_question
from programming_languages_python.fourth_laba_lang.main import third_question as fourth_laboratory_third_question
from programming_languages_python.fourth_laba_lang.main import fourth_question as fourth_laboratory_fourth_question

from programming_languages_python.fifth_laba_lang.main import first_question as fifth_laboratory_first_question
from programming_languages_python.fifth_laba_lang.main import second_question as fifth_laboratory_second_question
from programming_languages_python.fifth_laba_lang.main import third_question as fifth_laboratory_third_question
from programming_languages_python.fifth_laba_lang.main import fourth_question as fifth_laboratory_fourth_question

from programming_languages_python.seventh_laba_lang.main import first_question as seventh_laboratory_first_question
from programming_languages_python.seventh_laba_lang.main import second_question as seventh_laboratory_second_question
from programming_languages_python.seventh_laba_lang.main import third_question as seventh_laboratory_third_question
from programming_languages_python.seventh_laba_lang.main import fourth_question as seventh_laboratory_fourth_question

from programming_languages_python.eigth_laba_lang.main import first_question as eigth_laboratory_first_question
from programming_languages_python.eigth_laba_lang.main import second_question as eigth_laboratory_second_question
from programming_languages_python.eigth_laba_lang.main import third_question as eigth_laboratory_third_question

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
                                          "сохранения новых данных обратно в файл", fifth_laboratory_fourth_question),
    "Лабораторная работа 6 Подзадача 1": ("Реализовать лабораторные в виде приложения", None),
    "Лабораторная работа 6 Подзадача 2": ("Реализовать лабораторные в виде приложения", None),
    "Лабораторная работа 6 Подзадача 3": ("Реализовать лабораторные в виде приложения", None),
    "Лабораторная работа 6 Подзадача 4": ("Реализовать лабораторные в виде приложения", None),
    "Лабораторная работа 7 Подзадача 1": ("Пусть дан словарь. Посчитайте и выведите сколько в словаре ключей",
                                          seventh_laboratory_first_question),
    "Лабораторная работа 7 Подзадача 2": ("""
    Пусть дан файл, в котором содержится информация о студентах в виде:
        1;Иванов Иван Иванович;23;БО-111111
        2;Сидоров Семен Семенович;23;БО-111111
    Считайте информацию из файла в структуру: {№: [ФИО, Возраст, Группа], №: [....], №: [....]}
    """, seventh_laboratory_second_question),
    "Лабораторная работа 7 Подзадача 3": ("Добавьте к задаче №2 возможность увеличить возраст всех студентов на 1",
                                          seventh_laboratory_third_question),
    "Лабораторная работа 7 Подзадача 4": ("Добавьте к пользовательскому интерфейсу из задачи №3 возможность "
                                          "сохранения новых данных в файл.", seventh_laboratory_fourth_question),
    "Лабораторная работа 8 Подзадача 1": (
        "Пусть список студентов представлен в виде структуры [[№, ФИО, Возраст, Группа]...]. "
        "Преобразовать список в словарь вида: {№:[ФИО, Возраст, Группа], ....}", eigth_laboratory_first_question),
    "Лабораторная работа 8 Подзадача 2": (
        "Добавить к задаче №1 для словаря возможность (без преобразования словаря обратно в список)\n"
        "1.Увеличить возраст конкретного студента на 1;\n"
        "2.Изменить ФИО студента;\n3.Увеличить возраст студента по номеру\n4.Изменить группу студента. Поиск по ФИО\n"
        "5.Удалить запись о студенте. Поиск по №;\n6.Если возраст студента больше 22 уменьшить его на 1\n"
        "7.Если возраст студента равен 23, удалить его из списка;\n"
        "8.У всех студентов с фамилией Иванов увеличить возраст на 1;\n"
        "9.У студентов с фамилией Иванов изменить фамилию на Сидоров;\n"
        "10.Поменять ФИО и Группа местами;",
        eigth_laboratory_second_question),
    "Лабораторная работа 8 Подзадача 3": (
        "1.Вывести список студентов группы БО - 111111;\n"
        "2.Вывести список студентов с номерами от 1 до 10;\n"
        "3.Списка студентов в возрасте 22 лет\n"
        "4.Список студентов с фамилией Иванов;\n"
        "5.Списка студентов, чьи фамилии заканчиваются на 'a';\n"
        "6.Список студентов, чей возраст - это четное число;\n"
        "7.Список студентов, если в возрасте студента встречается число 5;\n"
        "8.Список студентов, если их номера группы длиннее 7 символов;\n"
        "9.Список студентов (а также информацию о них), если их № - четное число;\n"
        "10.Список студентов, если их номер группы заканчивается на '1'",
        eigth_laboratory_third_question),
    "Лабораторная работа 8 Подзадача 4": ("Задания нет, сделано с целью осуществления заглушки", None)
}


class TaskChooser:
    __slots__ = ("number_laboratory", "number_question")

    def __init__(self, number_laboratory: int, number_question: int):
        self.number_laboratory = number_laboratory
        self.number_question = number_question

    @property
    def condition(self):
        return dictionary.get(f"Лабораторная работа {self.number_laboratory} Подзадача {self.number_question}",
                              ("Не выполнял ещё", " "))[0]

    @property
    def function(self):
        return dictionary.get(f"Лабораторная работа {self.number_laboratory} Подзадача {self.number_question}",
                              (" ", None))[1]
