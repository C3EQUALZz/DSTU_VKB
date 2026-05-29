"""Доменные ошибки методов LSB-R / LSB-M / Хемминг."""


class EmbeddingError(Exception):
    """Базовая ошибка встраивания в BMP по методам ПР7."""


class ContainerTooSmallError(EmbeddingError):
    """В контейнере не хватает каналов для размещения сообщения."""

    def __init__(self, required: int, available: int) -> None:
        self.required = required
        self.available = available
        super().__init__(
            f"требуется {required} элементов LSB, доступно {available}",
        )
