"""Доменные ошибки метода Куттера-Джордана-Боссена."""


class KjbError(Exception):
    """Базовая ошибка алгоритма КДБ."""


class ContainerTooSmallError(KjbError):
    """В контейнере недостаточно пикселей для размещения сообщения."""

    def __init__(self, required: int, available: int) -> None:
        self.required = required
        self.available = available
        super().__init__(
            f"требуется {required} пикселей-носителей, доступно {available}",
        )
