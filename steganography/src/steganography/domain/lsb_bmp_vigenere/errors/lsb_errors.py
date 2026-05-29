"""Доменные ошибки встраивания LSB+Виженер."""


class LsbBmpError(Exception):
    """Базовая ошибка процесса встраивания/извлечения через LSB."""


class ContainerTooSmallError(LsbBmpError):
    """В BMP не хватает пикселей для размещения сообщения с метками."""

    def __init__(self, required_bits: int, available_bits: int) -> None:
        self.required_bits = required_bits
        self.available_bits = available_bits
        super().__init__(
            f"BMP-контейнеру нужно минимум {required_bits} LSB-бит, "
            f"доступно {available_bits}",
        )


class MarkersNotFoundError(LsbBmpError):
    """В извлечённом потоке не найдены метки начала и конца."""

    def __init__(self) -> None:
        super().__init__("в потоке не найдены метки начала и конца сообщения")


class EmptyKeyError(LsbBmpError):
    """Ключ Виженера пуст — расшифровка невозможна."""

    def __init__(self) -> None:
        super().__init__("ключ шифра Виженера не может быть пустым")
