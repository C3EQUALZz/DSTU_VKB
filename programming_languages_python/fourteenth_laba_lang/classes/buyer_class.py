"""
Модуль, который описывает покупателя
"""
from dataclasses import dataclass


@dataclass
class Buyer:
    """
    Класс, который описывает покупателя
    """
    surname: str
    name: str
    patronymic: str
    address: str
    credit_card_number: int
    bank_account_number: int

    @property
    def full_name(self) -> list[str]:
        """
        Метод, который нам возвращает ФИО в виде списка. Используется для сортировки.
        """
        return [self.surname, self.name, self.patronymic]

    def __str__(self) -> str:
        """
        Метод, который возвращает всю информацию о человеке.
        Данный магический метод показывает как будет обрабатываться класс, если его переведут в строку.
        """
        return (f"ФИО: {' '.join(self.full_name)}\n"
                f"Адрес: {self.address}\n"
                f"Номер кредитной карты: {self.credit_card_number}\n"
                f"Номер банковского счета: {self.bank_account_number}")
