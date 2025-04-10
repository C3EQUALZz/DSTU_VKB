"""
Модуль, который описывает абонента
"""

from dataclasses import dataclass

from arrow import Arrow


@dataclass
class Subscriber:
    identification_number: int
    surname: str
    first_name: str
    patronymic: str
    address: str
    credit_card_number: int
    debit: float
    credit: float
    intercity_call_time: Arrow.time
    local_call_time: Arrow.time

    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.first_name} {self.patronymic}"

    def __str__(self):
        """
        Магический метод для красивого вывода абонента в виде строки.
        """
        return (
            f"Идентификационный номер: {self.identification_number}\n"
            f"Фамилия: {self.surname}\n"
            f"Имя: {self.first_name}\n"
            f"Отчество: {self.patronymic}\n"
            f"Адрес: {self.address}\n"
            f"Номер кредитной карточки: {self.credit_card_number}\n"
            f"Дебет: {self.debit}\n"
            f"Кредит: {self.credit}\n"
            f"Время междугородных переговоров: {self.intercity_call_time}\n"
            f"Время городских переговоров: {self.local_call_time}"
        )
