"""
Модуль, который описывает покупателя
"""
from dataclasses import dataclass


@dataclass
class Buyer:
    surname: str
    name: str
    patronymic: str
    address: str
    credit_card_number: int
    bank_account_number: int

    @property
    def full_name(self):
        """
        Метод, который нам возвращает ФИО
        """
        return [self.surname, self.name, self.patronymic]

    def __str__(self):
        """
        Метод, который возвращает всю информацию о человеке
        """
        return (f"ФИО: {' '.join(self.full_name)}\n"
                f"Адрес: {self.address}\n"
                f"Номер кредитной карты: {self.credit_card_number}\n"
                f"Номер банковского счета: {self.bank_account_number}")
