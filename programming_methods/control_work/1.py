"""
22. Быстрый поиск клиента. По номеру счёта мгновенно находите данные клиента.
"""

import uuid
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar('T')

@dataclass
class UserEntity:
    oid: str = field(default_factory=lambda: str(uuid.uuid4()), kw_only=True)
    full_name: str

class Database(Generic[T]):
    def __init__(self) -> None:
        self._data: dict[str, T] = {}

    def get(self, oid: str) -> T | None:
        return self._data.get(oid)

    def append(self, obj: T) -> T:
        self._data[obj.oid] = obj
        return obj

    def pop(self, oid: str) -> T | None:
        if oid in self._data:
            return self._data.pop(oid)

        return None

    def list(self) -> dict[str, str]:
        return self._data


def main() -> None:
    database: Database[UserEntity] = Database()

    while True:

        request_string: str = "Введите номер от 1 до 3:\n1-Добавить пользователя\n2-Просмотреть пользователей\n3-Удалить пользователя\n4-Закончить работу\n"

        input_data: str = input(request_string)

        match input_data:
            case "1":
                full_name: str = input("Введите данные для пользователя имя и фамилия: ")
                new_user: UserEntity = UserEntity(full_name)
                print(f"Новый пользователь: {new_user}")

                database.append(new_user)

            case "2":
                print(database.list())

            case "3":
                oid: str = input("Введите идентификатор: ")
                if database.pop(oid):
                    print("Пользователь удален удачно")
                else:
                    print("Такого идентификатора нет")

            case "4":
                exit(0)

            case _:
                print("Вы ввели неправильные данные")


if __name__ == "__main__":
    main()
