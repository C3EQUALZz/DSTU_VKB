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
