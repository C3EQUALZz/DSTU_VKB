"""
Является вторичным файлом, где реализуется блокировка всех функций для Excel
"""
from string import ascii_letters
from typing import NoReturn

import aspose.cells as ac

from .word_class import WordBlock


class ExcelBlock(WordBlock):
    """
    Данный класс создан для взаимодействия с Excel файлами
    """

    def __init__(self, path: str, key: str = "full"):
        super().__init__(path, key)
        self.__workbook = ac.Workbook(self.path)

    def save_workbook(self) -> NoReturn:
        """
        Метод, который сохраняет книгу Excel
        :return: ничего не возвращает, только сохраняет xlsx файл
        """
        self.__workbook.save(self.path)

    def block_file(self, password: str) -> NoReturn:
        """
        Метод для блокировки файла с заданным паролем в аргументах
        :param password: пароль в строковом виде
        :return: ничего не возвращает, только устанавливает пароль на файл
        """
        # Обращаемся к родительскому методу, чтобы проверить пароль
        password = super()._check_password(password)
        if self.key == "FULL":
            self.__workbook.set_encryption_options(ac.EncryptionType.STRONG_CRYPTOGRAPHIC_PROVIDER, 128)
            self.__workbook.settings.password = password
        else:
            self.__workbook.protect(eval(f"ac.ProtectionType.{self._key}"), password)
        self.save_workbook()

    def unblock_file(self, password: str) -> NoReturn:
        """
        Метод, чтобы снять все ограничения с xlsx файла
        :param password: пароль в строковом виде
        :return: ничего не возвращает, только снимает все ограничения с файла
        """
        load = ac.LoadOptions()
        load.password = password
        self.__workbook = ac.Workbook(self.path, load)
        self.__workbook.settings.password = None
        self.__workbook.unprotect(password)
        self.save_workbook()

    def block_list(self, number: int, password: str) -> NoReturn:
        """
        Метод, который блокирует отдельный лист, заданный пользователем
        :param number: позиционный номер нашего листа
        :param password: пароль в строковом виде, удовлетворяющий определенным условиям
        :return: ничего не возвращает, только устанавливает полностью ограничения на определенный лист
        """
        sheet = self.__workbook.worksheets.get(number)
        sheet.protect(ac.ProtectionType.ALL, password, '')
        self.save_workbook()

    def unblock_list(self, number: int, password: str) -> NoReturn:
        """
        Метод, который снимает все ограничения с листа.
        :param number: Любая страница, с которого надо снять защиту.
        :param password: Пароль, который установлен на данный лист
        :return:
        """
        sheet = self.__workbook.worksheets.get(number)
        sheet.unprotect(password)
        self.save_workbook()

    def block_range(self, number_list: int = 0, range_for_block: str = "A1:C3", _lock=True) -> NoReturn:
        """
        Метод для блокировки определенного диапазона у определенного листа
        :param _lock: заглушка, пользователь не должен использовать это
        :param number_list: номер листа, начиная с 0
        :param range_for_block: диапазон для блокировки в виде "A1:C3"
        :return: пересоздает xlsx документ, где есть заблокированный диапазон
        """
        # получаем номер страницы, к которой мы обращаемся
        sheet = self.__workbook.worksheets.get(number_list)
        # разбиваем значение, заданное в виде строки на цифры, чтобы была возможность проходить циклом
        start_letter, start_number, end_letter, end_number = self.__parse_range(range_blocking=range_for_block)
        # здесь проходимся циклом, чтобы получить все буквы
        for letter_number in range(start_letter, end_letter + 1):
            # здесь проходимся циклом, чтобы получить все цифры
            for number in range(start_number, end_number + 1):
                # создаем ячейку, склеивая число и букву
                cell = chr(65 + letter_number) + str(number)
                # получаем все параметры ячейки, устанавливаем свойство того, что у нас ячейка заблокирована
                style = sheet.cells.get(cell).get_style()
                style.is_locked = _lock
                sheet.cells.get(cell).set_style(style)

        self.save_workbook()

    def unblock_range(self, number_list: int, range_for_block: str) -> NoReturn:
        """
        Метод для разблокировки определенного диапазона у определенного листа
        :param number_list: номер листа, начиная с 0
        :param range_for_block: диапазон для разблокировки в виде "A1:C3"
        :return: пересоздает xlsx документ, где есть разблокированный диапазон
        """
        self.block_range(number_list, range_for_block, False)

    @staticmethod
    def __parse_range(range_blocking: str) -> tuple[int, int, int, int]:
        """
        Статический метод, который обрабатывает диапазоны.
        Его нужно улучшить, так как он не сработает с различными ячейками, где рядом более 2 букв
        :param range_blocking: примерно в виде "A1:C3"
        :return: возвращает кортеж для метода блокировки
        """
        # Не продумал для сочетания букв больше > 2. Не будет работать DH16 условный
        start = ascii_letters.find(range_blocking[0].lower())
        start_number = int(range_blocking[1])

        end = ascii_letters.find(range_blocking[3].lower())
        end_number = int(range_blocking[4])

        return start, start_number, end, end_number
