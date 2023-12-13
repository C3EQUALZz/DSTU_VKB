"""
Модуль, который описывает абонента
"""
from dataclasses import dataclass


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
    intercity_call_time: float
    local_call_time: float

    def __str__(self):
        """
        Магический метод для красивого вывода абонента в виде строки.
        """
        return f"""
        Идентификационный номер: {self.identification_number}
        Фамилия: {self.surname}
        Имя: {self.first_name}
        Отчество: {self.patronymic}
        Адрес: {self.address}
        Номер кредитной карточки: {self.credit_card_number}
        Дебет: {self.debit}
        Кредит: {self.credit}
        Время междугородных переговоров: {self.intercity_call_time}
        Время городских переговоров: {self.local_call_time}
        """


