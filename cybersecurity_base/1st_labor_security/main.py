"""
Данный модуль помогает работать с шифрованием файлов для дальнейшего использования.
К сожалению, он изменяет файлы визуально, так как у меня нет доступ к API данного сервиса.
# word_license = aw.License()
# word_license.set_license("Aspose.Total.lic")
Вышеописанный код помогает исправить ситуацию, если у Вас на ПК скачана лицензия.

TODO:
1. Запрос пути для файла у пользователя
2. Защита файла, используя пароль от пользователя
"""

from typing import NoReturn

from realisation_classes.excel_class import ExcelBlock
from realisation_classes.word_class import WordBlock


class BlockFile:
    """
    Основной класс, где происходит вся логика программы.
    Атрибут path - путь к файлу, есть проверка на существование файла.
    Атрибут password - пароль, который вы задаете для вашего файла.
    Атрибут key - ключ для способа изменения файла
    """

    def __new__(cls, path: str, key: str = "full"):
        if any(path.endswith(x) for x in ("docx", "doc")):
            res = WordBlock(path, key)
        else:
            res = ExcelBlock(path, key)
        return res


def block_docx(path: str, password: str) -> NoReturn:
    key_for_property = "1" if any(path.endswith(x) for x in ("docx", "doc")) else "2"

    match key_for_property:
        case "1":
            key_for_property = input("Введите ключ доступа к файлу."
                                     "\n'full' - пароль на весь документ;"
                                     "\n'read_only' - сделать документ только для чтения;"
                                     "\n'allow_only_comments' -  разрешить доступ только к полям формы; "
                                     "\n'allow_only_revisions' - разрешить только исправления;\n ")
        case "2":
            key_for_property = input("Введите ключ доступа к файлу. "
                                     "\n'full' - пароль на весь документ"
                                     "\n'all' - полностью блокировка;"
                                     "\n'contents' - не может вводить данные;"
                                     "\n'objects' - пользователь не может изменять объекты чертежа;"
                                     "\n'scenarios' - пользователь не может изменять сохраненные сценарии;"
                                     "\n'structure' - пользователь не может изменять сохраненную структуру;"
                                     "\n'windows' - пользователь не может изменять сохраненные окна; ")

    docx_file = BlockFile(path, key_for_property)
    docx_file.block_file(password)


def unblock_all(path: str, password: str) -> NoReturn:
    any_file = BlockFile(path)
    any_file.unblock_file(password)


def block_list(path: str, number: int, password: str, _key="block", _comment=None) -> NoReturn:
    if _comment is None:
        _comment = "Заблокировать лист можно только у Excel файла "

    if not any(path.endswith(x) for x in ("xlsx", "xls")):
        raise ValueError(_comment)

    excel_file = BlockFile(path)

    try:
        if _key == "block":
            excel_file.block_list(number, password)
        else:
            excel_file.unblock_list(number, password)

    except Exception as e:
        print("Вы выбрали лист, который и так был разблокирован либо он не был создан. ")


def unblock_list(path: str, number, password):
    block_list(path, number, password, _key="unblock", _comment="Разблокировать лист можно только у Excel файла ")


def block_range(path: str, number: int, range_for_block: str, _key="block", _comment=None):
    if _comment is None:
        _comment = "Заблокировать диапазон можно только у Excel файла "

    if not any(path.endswith(x) for x in ("xlsx", "xls")):
        raise ValueError(_comment)

    excel_file = BlockFile(path)

    try:
        if _key == "block":
            excel_file.block_range(number, range_for_block)
        else:
            excel_file.unblock_range(number, range_for_block)

    except Exception as e:
        print("Вы выбрали лист, который не был создан. ")


def unblock_range(path: str, number: int, range_for_block: str):
    block_range(path, number, range_for_block, _key="unblock",
                _comment="Разблокировать диапазон можно только у Excel файла")


def interact_with_user():
    path_gl = input("Введите путь к файлу ")

    password_gl = input(
        "Введите пароль к вашему файлу. \n Должен удовлетворять признакам: \n1.Длина больше 5;\n2.Есть цифры. \n ")

    question_for_user = """
    Что вы хотите сделать? 
    Блокировать файл (1)?
    Разблокировать файл (2)?
    Защитить лист (3)?
    Разблокировать лист (4)?
    Заблокировать диапазон (5)?
    Разблокировать диапазон (6)?
    """

    match input(question_for_user):
        case "1":
            block_docx(path_gl, password_gl)
        case "2":
            unblock_all(path_gl, password_gl)
        case "3":
            number = int(input("Введите номер листа, который вы хотите заблокировать. Нумерация начинается с 1. "))
            block_list(path_gl, number - 1, password_gl)
        case "4":
            number = int(input("Введите номер листа, который вы хотите разблокировать. Нумерация начинается с 1. "))
            unblock_list(path_gl, number - 1, password_gl)
        case "5":
            number_list = int(
                input("Введите номер листа, где вы хотите заблокировать диапазон. Нумерация начинается с 1. "))
            range_for_block = input(
                f"Введите ваш диапазон, который вы хотите заблокировать на странице {number_list}. Например, 'A1:C3'. ")
            block_range(path_gl, number_list, range_for_block)

        case "6":
            number_list = int(
                input("Введите номер листа, где вы хотите заблокировать диапазон. Нумерация начинается с 1. "))
            range_for_unblock = input(
                f"Введите ваш диапазон, который вы хотите разблокировать на странице {number_list}. Например, 'A1:C3'. ")
            unblock_range(path_gl, number_list, range_for_unblock)


if __name__ == "__main__":
    interact_with_user()
