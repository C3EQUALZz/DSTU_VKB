"""Базовый интерфейс кодировки — Encoding (ABC).

Кодировка двунаправленна:

* :meth:`decode` переводит битовую строку, собранную из символов
  docx-контейнера, обратно в исходный текст (ПР «декод»);
* :meth:`encode` переводит секретный текст в битовую строку, которую
  затем встраивают в контейнер (ПР «энкод»).

Если данные не разбираются по правилам кодировки, возвращается ``None``.
"""

from abc import ABC, abstractmethod


class Encoding(ABC):
    """Абстрактная кодировка скрытого сообщения."""

    name: str

    @abstractmethod
    def decode(self, bits: str) -> str | None:
        ...

    @abstractmethod
    def encode(self, text: str) -> str | None:
        ...
