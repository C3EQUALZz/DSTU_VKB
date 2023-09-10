"""
Является вторичным файлом, где реализуется блокировка всех функций для MS Word
"""
import os
from typing import NoReturn

import aspose.words as aw


class BadPassword(Exception):
    """
    Данный класс создан с целью описания ошибки, понятной пользователю.
    """
    pass


class WordBlock:
    """
    Данный класс создан для взаимодействия с файлами docx
    """

    def __init__(self, path: str, key: str = "full"):
        self.path = path
        self.key = key

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        # проверка на существование пути и корректности расширения файла
        if not os.path.exists(path) or path.split('.')[-1] not in {"xml", "xlsx", "docx", "doc"}:
            raise ValueError("Неправильный путь к файлу, проверьте снова ")
        self._path: str = path

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, key_set: str) -> NoReturn:
        """
        Сеттер, который позволяет рассматривать свойства для определенного файла
        :param key_set:
        :return: функция ничего не возвращает
        """
        keys: set[str] = {"full", "read_only", "allow_only_comments", "allow_only_revisions", "all", "contents",
                          "objects", "scenarios", "structure", "windows"}
        if key_set not in keys:
            raise KeyError("Не подходящий ключ для указания значения ")
        self._key = key_set.upper()

    def block_file(self, password: str) -> NoReturn:
        """
        Метод для блокировки файла с использованием заданного пароля
        :param password: пароль в строковом виде
        :return: ничего не возвращает, только сохраняет документ
        """

        password = self._check_password(password)
        # создаем объект документа
        doc = aw.Document(self._path)

        options = None

        # Логика установки пароля на документ и блокировки отдельных функций разная
        if self._key == "FULL":
            options = aw.saving.OoxmlSaveOptions(eval(f"aw.SaveFormat.{self._path.split('.')[1].upper()}"))
            options.password = password
        else:
            doc.protect(eval(f"aw.ProtectionType.{self._key}"), password)

        doc.save(self._path, options)

    def unblock_file(self, password: str) -> NoReturn:
        """
        Метод, который позволяет разблокировать полностью файл, сняв все поставленные до этого ограничения
        :param password: пароль в строковом виде от документа
        :return: ничего не возвращает. Только сохраняет документ.
        """
        doc = aw.Document(self._path, aw.loading.LoadOptions(password))
        doc.unprotect()
        doc.save(self._path)

    @staticmethod
    def _check_password(password: str) -> str:
        """
        Статический метод, который создан для проверки пароля
        :param password: пароль в строковом виде, содержащий цифры, обязан быть длиной больше 5
        :return: возвращает пароль в случае корректной проверки
        """
        if not (isinstance(password, str) and len(password) > 5 and any(x.isdigit() for x in password)):
            raise BadPassword("В вашем пароле должно быть больше 5 символов, обязательно наличие хотя бы одной цифры ")
        return password
