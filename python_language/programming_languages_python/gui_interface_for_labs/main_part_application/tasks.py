"""
В данном модуле формируется словарь из заданий, где условие берется из docstring функции
"""
__all__ = ["TaskChooser"]

import pkgutil
import importlib
from number_parser import parse_ordinal
import python_language.programming_languages_python as lang_module
from typing import Callable


def clear_text_from_tabs(text: str) -> str:
    """
    Функция, которая очищает текст от \t
    :param text: docstring функции
    """
    return "\n".join(line.lstrip() for line in text.split("\n"))


def create_description(function: Callable) -> str:
    """
    Создает описание для функций
    :param function: функция, у которой есть docstring.
    :returns: Возвращает форматированную строку с docstring.
    """
    return clear_text_from_tabs(function.__doc__) if function.__doc__ else "No description available"


def key_generation(module, counter: int):
    """
    Функция, которая создает ключ для словаря, где module - это имя папки с названием лабораторной.
    :param module: Модуль с лабораторной работой.
    :param counter: Счетчик, который отвечает за номер задания
    """
    question = parse_ordinal(module.__name__.split(".")[-1].split("_")[0])
    return f"Лабораторная работа {question} Подзадача {counter}"


def info_cur_dir_modules() -> list:
    """
    Функция, благодаря которой мы можем узнать информацию о находящихся рядом папок.
    """
    package_path = lang_module.__path__[0]
    return [importlib.import_module(f"python_language.programming_languages_python.{name}") for _, name, _
            in pkgutil.walk_packages([package_path]) if name.endswith("lang")]


def fill_dictionary() -> dict:
    """
    Функция, благодаря которой мы заполняем словарь с данными
    """
    dictionary = {}
    for module in info_cur_dir_modules():
        counter = 1
        for name, func in module.__dict__.items():
            if callable(func):
                dictionary[key_generation(module, counter)] = (create_description(func), func)
                counter += 1

    return dictionary


class TaskChooser:
    __slots__ = ("number_laboratory", "number_question", "__dictionary")

    def __init__(self, number_laboratory: int, number_question: int):
        self.number_laboratory = number_laboratory
        self.number_question = number_question
        self.__dictionary = fill_dictionary()

    @property
    def condition(self) -> str:
        return self.__dictionary.get(f"Лабораторная работа {self.number_laboratory} Подзадача {self.number_question}",
                                     ("Не выполнял ещё", " "))[0]

    @property
    def function(self):
        return self.__dictionary.get(f"Лабораторная работа {self.number_laboratory} Подзадача {self.number_question}",
                                     (" ", None))[1]
